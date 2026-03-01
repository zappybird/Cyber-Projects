/**
 * terminal_sfx.js
 * Ghost in the Shell / Matrix style typewriter/terminal sound effects
 *
 * ─── USAGE (Flask) ────────────────────────────────────────────────────────────
 *
 *  1. Place this file at:  /static/terminal_sfx.js
 *  2. Place sound files at: /static/sfx/
 *       click1.wav, click2.wav, click3.wav, click4.wav
 *       enter.wav, backspace.wav, error.wav (optional)
 *
 *  3. In your HTML template:
 *
 *     <textarea id="cmdInput"></textarea>
 *     <pre id="terminalOutput"></pre>
 *
 *     <script src="{{ url_for('static', filename='terminal_sfx.js') }}"></script>
 *     <script>
 *       window.TerminalSFX.init();
 *
 *       // To append text with typewriter effect:
 *       window.TerminalSFX.typeOut("SCANNING TARGET...\n");
 *
 *       // To play a sound manually:
 *       window.TerminalSFX.playClick("enter");
 *
 *       // To unlock audio early (e.g. on a "connect" button click):
 *       window.TerminalSFX.unlock();
 *     </script>
 *
 * ─────────────────────────────────────────────────────────────────────────────
 */

(function (global) {
  'use strict';

  // ─── DEFAULT CONFIG ──────────────────────────────────────────────────────────

  const DEFAULT_CONFIG = {
    // DOM selectors
    selectors: {
      input:  '#cmdInput',
      output: '#terminalOutput',
    },

    // Sound file paths (relative to document root)
    sounds: {
      clicks:    [
        '/static/sfx/click1.wav',
        '/static/sfx/click2.wav',
        '/static/sfx/click3.wav',
        '/static/sfx/click4.wav',
      ],
      enter:     '/static/sfx/enter.wav',
      backspace: '/static/sfx/backspace.wav',
      error:     '/static/sfx/error.wav',   // optional — missing file is handled gracefully
    },

    // Volume (0.0 – 1.0) base levels per sound kind
    volume: {
      click:     0.45,
      enter:     0.55,
      backspace: 0.40,
      error:     0.60,
    },

    // Random jitter ranges (applied each play)
    jitter: {
      volumeRange:      0.15,   // ± this fraction of base volume
      playbackRateRange: 0.03,  // ± this fraction around 1.0
    },

    // Throttling
    cooldownMs:       20,    // minimum ms between any two sounds
    bulkThreshold:    20,    // characters — above this, treat as bulk append
    maxRatePerSecond: 30,    // hard cap on sounds per second

    // Feature flags
    enableInput:  true,
    enableOutput: true,

    // Output hook mode: "observer" | "typeOutOnly"
    // "observer"    — MutationObserver watches #terminalOutput automatically
    // "typeOutOnly" — only TerminalSFX.typeOut() triggers sounds; no observer
    mode: 'observer',
  };

  // ─── STATE ───────────────────────────────────────────────────────────────────

  let cfg           = {};
  let audioCtx      = null;
  let audioUnlocked = false;
  let buffers       = {};           // { 'click1': AudioBuffer, 'enter': AudioBuffer, … }
  let lastPlayTime  = 0;            // epoch ms of last sound played
  let soundsThisSec = 0;            // rate-limiter counter
  let rateResetTimer = null;
  let observer      = null;         // MutationObserver instance
  let initialized   = false;

  // ─── HELPERS ─────────────────────────────────────────────────────────────────

  /** Deep-merge two plain objects (one level deep for nested objects). */
  function mergeConfig(defaults, overrides) {
    const out = Object.assign({}, defaults);
    if (!overrides) return out;
    for (const key of Object.keys(overrides)) {
      if (
        overrides[key] !== null &&
        typeof overrides[key] === 'object' &&
        !Array.isArray(overrides[key]) &&
        typeof defaults[key] === 'object' &&
        !Array.isArray(defaults[key])
      ) {
        out[key] = Object.assign({}, defaults[key], overrides[key]);
      } else {
        out[key] = overrides[key];
      }
    }
    return out;
  }

  /** Return a random float between (value - range) and (value + range), clamped to [min, max]. */
  function jitter(value, range, min, max) {
    const result = value + (Math.random() * 2 - 1) * range;
    return Math.min(max, Math.max(min, result));
  }

  /** Check whether the rate limiter allows another sound right now. */
  function withinRateLimit() {
    const now = Date.now();
    // Cooldown gate
    if (now - lastPlayTime < cfg.cooldownMs) return false;
    // Per-second cap
    if (soundsThisSec >= cfg.maxRatePerSecond) return false;
    return true;
  }

  /** Record that a sound just played. */
  function recordPlay() {
    lastPlayTime = Date.now();
    soundsThisSec++;
    if (!rateResetTimer) {
      rateResetTimer = setTimeout(function () {
        soundsThisSec = 0;
        rateResetTimer = null;
      }, 1000);
    }
  }

  // ─── AUDIO CONTEXT ───────────────────────────────────────────────────────────

  function getAudioContext() {
    if (audioCtx) return audioCtx;
    try {
      const AC = global.AudioContext || global.webkitAudioContext;
      if (!AC) return null;
      audioCtx = new AC();
      // Start suspended — must be resumed by a real user gesture
      if (audioCtx.state !== 'suspended') {
        // Already running in some browsers; that's fine
      }
      return audioCtx;
    } catch (e) {
      console.warn('[TerminalSFX] AudioContext unavailable:', e.message);
      return null;
    }
  }

  // ─── BUFFER LOADING ──────────────────────────────────────────────────────────

  /**
   * Fetch and decode a single audio file.
   * Resolves with an AudioBuffer or null on failure.
   */
  function loadBuffer(url) {
    return fetch(url)
      .then(function (res) {
        if (!res.ok) throw new Error('HTTP ' + res.status);
        return res.arrayBuffer();
      })
      .then(function (ab) {
        const ctx = getAudioContext();
        if (!ctx) return null;
        return ctx.decodeAudioData(ab);
      })
      .catch(function () {
        // Missing or malformed file — fail silently
        return null;
      });
  }

  /** Load all configured sound files into the buffers map. */
  function loadAllBuffers() {
    const ctx = getAudioContext();
    if (!ctx) return Promise.resolve();

    const promises = [];

    // Click samples: keyed as 'click0', 'click1', …
    cfg.sounds.clicks.forEach(function (url, i) {
      promises.push(
        loadBuffer(url).then(function (buf) {
          if (buf) buffers['click' + i] = buf;
        })
      );
    });

    // Named sounds
    ['enter', 'backspace', 'error'].forEach(function (kind) {
      const url = cfg.sounds[kind];
      if (!url) return;
      promises.push(
        loadBuffer(url).then(function (buf) {
          if (buf) buffers[kind] = buf;
        })
      );
    });

    return Promise.all(promises);
  }

  // ─── PLAYBACK ────────────────────────────────────────────────────────────────

  /**
   * Play a sound buffer with jitter applied.
   * @param {AudioBuffer} buffer
   * @param {string} kind  - 'click' | 'enter' | 'backspace' | 'error'
   */
  function playBuffer(buffer, kind) {
    const ctx = getAudioContext();
    if (!ctx || !buffer) return;
    if (!audioUnlocked || ctx.state === 'suspended') return;

    try {
      const gainNode = ctx.createGain();
      const baseVol  = (cfg.volume[kind] !== undefined) ? cfg.volume[kind] : cfg.volume.click;
      gainNode.gain.value = jitter(baseVol, cfg.jitter.volumeRange * baseVol, 0.01, 1.0);
      gainNode.connect(ctx.destination);

      const source = ctx.createBufferSource();
      source.buffer = buffer;

      // playbackRate jitter for organic feel
      source.playbackRate.value = jitter(1.0, cfg.jitter.playbackRateRange, 0.85, 1.15);

      source.connect(gainNode);
      source.start(0);
    } catch (e) {
      // Defensive — never throw into caller
    }
  }

  /**
   * Public: play a sound by kind.
   * kind: 'click' | 'enter' | 'backspace' | 'error'
   */
  function playClick(kind) {
    if (!withinRateLimit()) return;

    let buffer = null;

    if (kind === 'click' || kind === undefined) {
      // Pick a random loaded click sample
      const keys = Object.keys(buffers).filter(function (k) { return k.startsWith('click'); });
      if (keys.length === 0) return;
      const key = keys[Math.floor(Math.random() * keys.length)];
      buffer = buffers[key];
    } else {
      buffer = buffers[kind] || null;
      // Fallback to a click if named sound missing
      if (!buffer) {
        const keys = Object.keys(buffers).filter(function (k) { return k.startsWith('click'); });
        if (keys.length > 0) buffer = buffers[keys[0]];
      }
    }

    if (!buffer) return;
    recordPlay();
    playBuffer(buffer, kind === 'click' || !kind ? 'click' : kind);
  }

  // ─── UNLOCK ──────────────────────────────────────────────────────────────────

  /**
   * Public: resume the AudioContext after a user gesture.
   * Safe to call multiple times.
   */
  function unlock() {
    const ctx = getAudioContext();
    if (!ctx) return;
    if (audioUnlocked) return;
    ctx.resume().then(function () {
      audioUnlocked = true;
    }).catch(function () {});
  }

  /** Attach unlock to the first user gesture on the document. */
  function attachUnlockListeners() {
    function onGesture() {
      unlock();
      document.removeEventListener('keydown',  onGesture);
      document.removeEventListener('click',    onGesture);
      document.removeEventListener('touchend', onGesture);
    }
    document.addEventListener('keydown',  onGesture, { once: true, passive: true });
    document.addEventListener('click',    onGesture, { once: true, passive: true });
    document.addEventListener('touchend', onGesture, { once: true, passive: true });
  }

  // ─── INPUT HOOKS ─────────────────────────────────────────────────────────────

  function attachInputHooks() {
    if (!cfg.enableInput) return;
    const el = document.querySelector(cfg.selectors.input);
    if (!el) return;

    el.addEventListener('keydown', function (e) {
      // Unlock on first real keypress
      unlock();

      if (e.key === 'Enter') {
        playClick('enter');
        return;
      }
      if (e.key === 'Backspace' || e.key === 'Delete') {
        playClick('backspace');
        return;
      }
      // Printable characters: single char keys, space included
      if (e.key.length === 1) {
        playClick('click');
      }
    }, { passive: true });
  }

  // ─── OUTPUT HOOKS ────────────────────────────────────────────────────────────

  /**
   * Handle a chunk of newly appended text.
   * Plays one sound for bulk appends, or per-character for small ones.
   */
  function handleOutputChunk(text) {
    if (!text || text.length === 0) return;

    if (text.length > cfg.bulkThreshold) {
      // Bulk append — single sound
      playClick('click');
    } else {
      // Small chunk — one sound per character (throttled)
      for (let i = 0; i < text.length; i++) {
        playClick('click');
      }
    }
  }

  /** Attach a MutationObserver to the output element. */
  function attachObserver() {
    if (!cfg.enableOutput) return;
    if (cfg.mode !== 'observer') return;

    const el = document.querySelector(cfg.selectors.output);
    if (!el) return;

    observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        // Added nodes
        mutation.addedNodes.forEach(function (node) {
          const text = node.textContent || '';
          handleOutputChunk(text);
        });

        // Character data changes (direct text node mutations)
        if (mutation.type === 'characterData') {
          // Only the delta would be ideal; we play one click conservatively
          playClick('click');
        }
      });
    });

    observer.observe(el, {
      childList:     true,
      subtree:       true,
      characterData: true,
    });
  }

  // ─── TYPEOUT ─────────────────────────────────────────────────────────────────

  /**
   * Public: append text to the output element with a typewriter animation.
   * Sounds are played per character here; MutationObserver is intentionally
   * bypassed via a flag to avoid double-playing.
   *
   * @param {string} text
   * @param {object} opts
   * @param {number} opts.charDelay  - ms between characters (default 30)
   * @param {string} opts.selector   - override output selector
   */
  function typeOut(text, opts) {
    if (!text) return;
    const options   = opts || {};
    const charDelay = (options.charDelay !== undefined) ? options.charDelay : 30;
    const selector  = options.selector || cfg.selectors.output;
    const el        = document.querySelector(selector);
    if (!el) return;

    // Temporarily disconnect observer to prevent double sounds
    if (observer) observer.disconnect();

    let i = 0;
    function typeNext() {
      if (i >= text.length) {
        // Reconnect observer after typeOut completes
        if (observer && cfg.mode === 'observer') {
          attachObserver();
        }
        return;
      }

      const char = text[i++];
      el.textContent += char;

      // Play sound for this character
      if (char === '\n') {
        // Newlines: subtle click, no enter sound (enter was already played on input)
        playClick('click');
      } else if (char !== ' ') {
        playClick('click');
      } else {
        // Space: play at lower frequency — every other space
        if (i % 2 === 0) playClick('click');
      }

      setTimeout(typeNext, charDelay);
    }

    typeNext();
  }

  // ─── INIT ─────────────────────────────────────────────────────────────────────

  /**
   * Public: initialize TerminalSFX.
   * @param {object} configOverride  - partial config to override defaults
   */
  function init(configOverride) {
    if (initialized) return;
    initialized = true;

    cfg = mergeConfig(DEFAULT_CONFIG, configOverride);

    // Boot AudioContext and load buffers
    const ctx = getAudioContext();
    if (ctx) {
      loadAllBuffers().catch(function () {});
    }

    // Attach gesture-based unlock
    attachUnlockListeners();

    // Wait for DOM ready before attaching hooks
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () {
        attachInputHooks();
        attachObserver();
      });
    } else {
      attachInputHooks();
      attachObserver();
    }
  }

  // ─── PUBLIC API ──────────────────────────────────────────────────────────────

  global.TerminalSFX = {
    /**
     * Initialize the system. Call once after including the script.
     * @param {object} [configOverride]
     */
    init: init,

    /**
     * Resume the AudioContext. Called automatically on first user gesture,
     * but can be called explicitly (e.g. on a button click).
     */
    unlock: unlock,

    /**
     * Append text to the output element with typewriter animation and sounds.
     * @param {string} text
     * @param {object} [opts]  { charDelay: number, selector: string }
     */
    typeOut: typeOut,

    /**
     * Play a sound manually.
     * @param {'click'|'enter'|'backspace'|'error'} [kind]  defaults to 'click'
     */
    playClick: playClick,
  };

})(window);