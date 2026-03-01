/**
 * terminal_sfx.js  —  v2.2
 * Ghost in the Shell / Matrix style terminal sound effects + animated intro
 *
 * ─── FLASK USAGE ──────────────────────────────────────────────────────────────
 *
 *  1. Place this file:        /static/terminal_sfx.js
 *  2. Place sound files:      /static/sfx/click1–4.wav  enter.wav  backspace.wav
 *
 *  3. HTML template:
 *
 *       <textarea id="cmdInput"></textarea>
 *       <pre     id="terminalOutput"></pre>
 *
 *       <script src="{{ url_for('static', filename='terminal_sfx.js') }}"></script>
 *       <script>
 *         // Basic init — intro fires automatically on first user gesture
 *         window.TerminalSFX.init();
 *
 *         // Custom intro text (optional override):
 *         window.TerminalSFX.init({
 *           intro: {
 *             enabled: true,
 *             text: "NETWORK SCANNER v1.0\nTARGET : 192.168.1.254\nPORTS  : 1 TO 100\nREADY.\n\n",
 *             charDelay: 38,
 *           }
 *         });
 *
 *         // Trigger typeOut manually at any point after init:
 *         window.TerminalSFX.typeOut("SCANNING...\n", { charDelay: 30 });
 *       </script>
 *
 * ─────────────────────────────────────────────────────────────────────────────
 *
 * ROOT CAUSE FIX (v2.2):
 *   Previous versions created the AudioContext at init() time, before any user
 *   gesture. Chrome/Firefox immediately suspend it and will NOT resume unless
 *   .resume() is called from within a user-gesture call stack.
 *
 *   Fix: AudioContext is NOT created until the first gesture handler fires.
 *   WAV files are pre-fetched as ArrayBuffers at init() (no gesture needed for
 *   fetch), then decoded into AudioBuffers only after the context exists.
 *   This guarantees the context is both created and running when first used.
 */

(function (global) {
  'use strict';

  // ─── CONFIG ──────────────────────────────────────────────────────────────────

  var DEFAULT_CONFIG = {

    selectors: {
      input:  '#cmdInput',
      output: '#terminalOutput',
    },

    sounds: {
      clicks: [
        '/static/sfx/click1.wav',
        '/static/sfx/click2.wav',
        '/static/sfx/click3.wav',
        '/static/sfx/click4.wav',
      ],
      enter:     '/static/sfx/enter.wav',
      backspace: '/static/sfx/backspace.wav',
      // error: '/static/sfx/error.wav',  // uncomment if you have this file
    },

    // Base volume per kind (0.0 – 1.0)
    volume: {
      click:     0.5,
      enter:     0.6,
      backspace: 0.45,
      error:     0.65,
    },

    // Per-play randomness (keeps it organic)
    jitter: {
      volumeFraction:       0.18,  // ± 18% of base volume
      playbackRateFraction: 0.04,  // ± 4% around 1.0 playback rate
    },

    // Throttling
    cooldownMs:       18,
    bulkThreshold:    20,   // chars — mutations above this = one sound
    maxRatePerSecond: 30,

    enableInput:  true,
    enableOutput: true,

    // 'observer'    — MutationObserver watches #terminalOutput
    // 'typeOutOnly' — only typeOut() triggers output sounds
    mode: 'observer',

    // Ghost-in-the-Shell intro sequence
    intro: {
      enabled: true,
      // Printed character-by-character on the first user gesture.
      // Uses a live timestamp. Override in init({ intro: { text: '...' } }).
      text: null,   // null = auto-generated at unlock time (see runIntro)
      charDelay:       38,   // base ms per character
      jitterMs:        16,   // ± random ms per character
      newlinePauseMs: 160,   // extra pause after each \n
    },
  };

  // ─── STATE ───────────────────────────────────────────────────────────────────

  var cfg            = {};
  var audioCtx       = null;
  var audioUnlocked  = false;
  var rawBuffers     = {};      // url  → ArrayBuffer  (fetched early)
  var decodedBuffers = {};      // key  → AudioBuffer  (decoded after unlock)
  var buffersDecoded = false;

  var lastPlayTime   = 0;
  var soundsThisSec  = 0;
  var rateTimer      = null;

  var observer       = null;
  var observerPaused = false;

  var initialized    = false;
  var introPlayed    = false;
  var introQueued    = false;

  // ─── UTILITIES ───────────────────────────────────────────────────────────────

  function mergeConfig(defaults, overrides) {
    var out = Object.assign({}, defaults);
    if (!overrides) return out;
    Object.keys(overrides).forEach(function (key) {
      var ov = overrides[key];
      var dv = defaults[key];
      if (ov !== null && typeof ov === 'object' && !Array.isArray(ov) &&
          dv !== null && typeof dv === 'object' && !Array.isArray(dv)) {
        out[key] = Object.assign({}, dv, ov);
      } else {
        out[key] = ov;
      }
    });
    return out;
  }

  function rand(min, max) {
    return min + Math.random() * (max - min);
  }

  function clamp(v, lo, hi) {
    return Math.min(hi, Math.max(lo, v));
  }

  function padTwo(n) {
    return n < 10 ? '0' + n : '' + n;
  }

  function nowTimestamp() {
    var d = new Date();
    return (
      d.getFullYear() + '-' +
      padTwo(d.getMonth() + 1) + '-' +
      padTwo(d.getDate())       + ' ' +
      padTwo(d.getHours())      + ':' +
      padTwo(d.getMinutes())    + ':' +
      padTwo(d.getSeconds())
    );
  }

  // ─── RATE LIMITING ───────────────────────────────────────────────────────────

  function canPlay() {
    if (Date.now() - lastPlayTime < cfg.cooldownMs) return false;
    if (soundsThisSec >= cfg.maxRatePerSecond) return false;
    return true;
  }

  function recordPlay() {
    lastPlayTime = Date.now();
    soundsThisSec++;
    if (!rateTimer) {
      rateTimer = setTimeout(function () {
        soundsThisSec = 0;
        rateTimer = null;
      }, 1000);
    }
  }

  // ─── AUDIO CONTEXT ───────────────────────────────────────────────────────────
  //
  // KEY FIX: createAudioContext() is called ONLY from within a user gesture
  // handler (unlock()). This is the only way to guarantee the context starts
  // in 'running' state on Chrome and Firefox.

  function createAudioContext() {
    if (audioCtx) return audioCtx;
    try {
      var AC = global.AudioContext || global.webkitAudioContext;
      if (!AC) {
        console.warn('[TerminalSFX] Web Audio API not supported in this browser.');
        return null;
      }
      audioCtx = new AC();
      return audioCtx;
    } catch (e) {
      console.warn('[TerminalSFX] AudioContext creation failed:', e.message);
      return null;
    }
  }

  // ─── BUFFER LOADING — TWO PHASES ─────────────────────────────────────────────

  // Phase 1 — fetch(): runs at init(), no gesture needed.
  // Stores raw ArrayBuffer per URL so decoding can happen once context exists.
  function fetchAllRaw() {
    var urls = cfg.sounds.clicks.slice();
    ['enter', 'backspace', 'error'].forEach(function (k) {
      if (cfg.sounds[k]) urls.push(cfg.sounds[k]);
    });

    urls.forEach(function (url) {
      fetch(url)
        .then(function (res) {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.arrayBuffer();
        })
        .then(function (ab) {
          rawBuffers[url] = ab;
        })
        .catch(function (err) {
          console.warn('[TerminalSFX] Failed to fetch sound file:', url, '—', err.message);
        });
    });
  }

  // Phase 2 — decodeAudioData(): runs inside onUnlocked(), after context exists.
  function decodeAllBuffers() {
    if (buffersDecoded) return Promise.resolve();
    var ctx = audioCtx;
    if (!ctx) return Promise.resolve();

    var promises = [];

    cfg.sounds.clicks.forEach(function (url, i) {
      var ab = rawBuffers[url];
      if (!ab) return;
      // .slice(0) because decodeAudioData detaches the original ArrayBuffer
      promises.push(
        ctx.decodeAudioData(ab.slice(0))
          .then(function (buf) {
            decodedBuffers['click' + i] = buf;
          })
          .catch(function (e) {
            console.warn('[TerminalSFX] Decode failed:', url, e.message);
          })
      );
    });

    ['enter', 'backspace', 'error'].forEach(function (kind) {
      var url = cfg.sounds[kind];
      if (!url) return;
      var ab = rawBuffers[url];
      if (!ab) return;
      promises.push(
        ctx.decodeAudioData(ab.slice(0))
          .then(function (buf) {
            decodedBuffers[kind] = buf;
          })
          .catch(function (e) {
            console.warn('[TerminalSFX] Decode failed:', url, e.message);
          })
      );
    });

    return Promise.all(promises).then(function () {
      buffersDecoded = true;
    });
  }

  // ─── PLAYBACK ────────────────────────────────────────────────────────────────

  function playBuffer(buffer, kind) {
    if (!audioCtx || !buffer) return;
    // Guard: only play when context is confirmed running
    if (!audioUnlocked || audioCtx.state !== 'running') return;

    try {
      var gain    = audioCtx.createGain();
      var base    = cfg.volume[kind] !== undefined ? cfg.volume[kind] : cfg.volume.click;
      var vf      = cfg.jitter.volumeFraction;
      gain.gain.value = clamp(rand(base * (1 - vf), base * (1 + vf)), 0.01, 1.0);
      gain.connect(audioCtx.destination);

      var src = audioCtx.createBufferSource();
      src.buffer = buffer;
      var rf = cfg.jitter.playbackRateFraction;
      src.playbackRate.value = clamp(rand(1.0 - rf, 1.0 + rf), 0.75, 1.25);
      src.connect(gain);
      src.start(0);
    } catch (e) {
      // Silently swallow — never throw into caller
    }
  }

  // Public playClick — silently no-ops if audio is unavailable
  function playClick(kind) {
    if (!canPlay()) return;

    var buffer      = null;
    var resolvedKind = kind || 'click';

    if (resolvedKind === 'click') {
      var keys = Object.keys(decodedBuffers).filter(function (k) {
        return k.indexOf('click') === 0;
      });
      if (!keys.length) return;
      buffer = decodedBuffers[keys[Math.floor(Math.random() * keys.length)]];
    } else {
      buffer = decodedBuffers[resolvedKind] || null;
      if (!buffer) {
        // Graceful fallback to any available click
        var fb = Object.keys(decodedBuffers).filter(function (k) {
          return k.indexOf('click') === 0;
        });
        if (fb.length) buffer = decodedBuffers[fb[0]];
      }
    }

    if (!buffer) return;
    recordPlay();
    playBuffer(buffer, resolvedKind);
  }

  // ─── UNLOCK ──────────────────────────────────────────────────────────────────

  function unlock() {
    if (audioUnlocked) return;

    // Create AND start the AudioContext here, inside the gesture stack
    var ctx = createAudioContext();
    if (!ctx) return;

    if (ctx.state === 'running') {
      audioUnlocked = true;
      onUnlocked();
      return;
    }

    // Suspended — resume now while we're still in the gesture handler
    ctx.resume().then(function () {
      if (ctx.state === 'running') {
        audioUnlocked = true;
        onUnlocked();
      }
    }).catch(function (e) {
      console.warn('[TerminalSFX] resume() failed:', e.message);
    });
  }

  function onUnlocked() {
    decodeAllBuffers().then(function () {
      if (cfg.intro.enabled && !introPlayed && !introQueued) {
        introQueued = true;
        // Brief delay so the triggering keydown sound plays first
        setTimeout(runIntro, 80);
      }
    });
  }

  // ─── UNLOCK LISTENERS ────────────────────────────────────────────────────────

  function attachUnlockListeners() {
    function onGesture() {
      unlock();
      // { once: true } on addEventListener handles removal automatically,
      // but belt-and-suspenders removal for the others:
      window.removeEventListener('keydown',  onGesture);
      window.removeEventListener('click',    onGesture);
      window.removeEventListener('touchend', onGesture);
    }
    // Attach on WINDOW (not document) for broadest gesture capture
    window.addEventListener('keydown',  onGesture, { once: true, passive: true });
    window.addEventListener('click',    onGesture, { once: true, passive: true });
    window.addEventListener('touchend', onGesture, { once: true, passive: true });
  }

  // ─── INPUT HOOKS ─────────────────────────────────────────────────────────────

  function attachInputHooks() {
    if (!cfg.enableInput) return;
    var el = document.querySelector(cfg.selectors.input);
    if (!el) {
      console.warn('[TerminalSFX] Input element not found:', cfg.selectors.input);
      return;
    }

    el.addEventListener('keydown', function (e) {
      // keydown on the input IS a user gesture — call unlock() here too so
      // typing into the field unlocks audio even if they never clicked elsewhere
      unlock();

      if (e.key === 'Enter')                      { playClick('enter');     return; }
      if (e.key === 'Backspace' || e.key === 'Delete') { playClick('backspace'); return; }
      if (e.key.length === 1)                     { playClick('click');     }
    }, { passive: true });
  }

  // ─── MUTATION OBSERVER ───────────────────────────────────────────────────────

  function handleChunk(text) {
    if (!text || !text.length) return;
    if (text.length > cfg.bulkThreshold) {
      playClick('click');  // one sound for the whole bulk chunk
    } else {
      for (var i = 0; i < text.length; i++) {
        playClick('click');
      }
    }
  }

  function startObserver() {
    if (!cfg.enableOutput || cfg.mode !== 'observer') return;
    var el = document.querySelector(cfg.selectors.output);
    if (!el) {
      console.warn('[TerminalSFX] Output element not found:', cfg.selectors.output);
      return;
    }
    if (observer) { observer.disconnect(); observer = null; }

    observer = new MutationObserver(function (mutations) {
      if (observerPaused) return;  // typeOut() is running — skip to avoid double sounds
      mutations.forEach(function (m) {
        m.addedNodes.forEach(function (node) {
          handleChunk(node.textContent || '');
        });
        if (m.type === 'characterData') {
          playClick('click');
        }
      });
    });

    observer.observe(el, { childList: true, subtree: true, characterData: true });
  }

  function pauseObserver()  { observerPaused = true;  }
  function resumeObserver() { observerPaused = false; }

  // ─── TYPEOUT ─────────────────────────────────────────────────────────────────

  /**
   * Append text to the output element, character by character, with sounds.
   *
   * @param {string} text
   * @param {object} [opts]
   * @param {number}   [opts.charDelay=30]        base ms between characters
   * @param {number}   [opts.jitterMs=10]         ± random ms per character
   * @param {number}   [opts.newlinePauseMs=0]    extra pause after each newline
   * @param {string}   [opts.selector]            override output selector
   * @param {function} [opts.onComplete]          called when animation finishes
   */
  function typeOut(text, opts) {
    if (!text) return;
    var o           = opts || {};
    var charDelay   = o.charDelay        !== undefined ? o.charDelay        : 30;
    var jitterMs    = o.jitterMs         !== undefined ? o.jitterMs         : 10;
    var nlPause     = o.newlinePauseMs   !== undefined ? o.newlinePauseMs   : 0;
    var onComplete  = typeof o.onComplete === 'function' ? o.onComplete : null;
    var el          = document.querySelector(o.selector || cfg.selectors.output);
    if (!el) return;

    // Pause observer for the duration so sounds don't double-fire
    pauseObserver();

    var i = 0;

    function next() {
      if (i >= text.length) {
        resumeObserver();
        if (onComplete) onComplete();
        return;
      }

      var ch = text[i++];
      el.textContent += ch;
      el.scrollTop = el.scrollHeight;

      // Sound per character
      if      (ch === '\n')  { playClick('click'); }
      else if (ch === ' ')   { if (i % 2 === 0) playClick('click'); }
      else                   { playClick('click'); }

      // Random timing for organic feel
      var delay = charDelay + rand(-jitterMs, jitterMs);
      if (ch === '\n' && nlPause > 0) delay += nlPause;
      setTimeout(next, Math.max(0, delay));
    }

    next();
  }

  // ─── INTRO ───────────────────────────────────────────────────────────────────

  function runIntro() {
    if (introPlayed) return;
    introPlayed = true;

    var el = document.querySelector(cfg.selectors.output);
    if (!el) return;

    // Build default intro text with a live timestamp if none was provided
    var text = cfg.intro.text;
    if (!text) {
      text = (
        'NETWORK SCANNER v1.0 \u2014 ' + nowTimestamp() + '\n' +
        'TARGET : 192.168.1.254\n'                               +
        'PORTS  : 1 TO 100\n'                                    +
        'READY.\n\n'
      );
    }

    // Clear the output so the intro is the first thing printed.
    // Remove this line if you want to preserve existing content.
    el.textContent = '';

    typeOut(text, {
      charDelay:      cfg.intro.charDelay,
      jitterMs:       cfg.intro.jitterMs,
      newlinePauseMs: cfg.intro.newlinePauseMs,
      onComplete: function () {
        var input = document.querySelector(cfg.selectors.input);
        if (input) input.focus();
      },
    });
  }

  // ─── INIT ────────────────────────────────────────────────────────────────────

  function init(configOverride) {
    if (initialized) return;
    initialized = true;

    cfg = mergeConfig(DEFAULT_CONFIG, configOverride);

    // Phase 1: pre-fetch WAV files (no gesture needed)
    fetchAllRaw();

    // Gesture listeners on window — unlock + intro on first interaction
    attachUnlockListeners();

    // Attach DOM hooks after DOM is ready
    function domReady() {
      attachInputHooks();
      startObserver();
    }

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', domReady);
    } else {
      domReady();
    }
  }

  // ─── PUBLIC API ──────────────────────────────────────────────────────────────

  global.TerminalSFX = {
    /**
     * Initialize. Call once after including the script.
     * @param {object} [configOverride]
     */
    init: init,

    /**
     * Unlock audio. Called automatically on first keydown/click/touchend.
     * Can be called manually from a button's onclick handler.
     */
    unlock: unlock,

    /**
     * Animate text into the output element with typewriter effect + sounds.
     * @param {string} text
     * @param {{ charDelay?, jitterMs?, newlinePauseMs?, selector?, onComplete? }} [opts]
     */
    typeOut: typeOut,

    /**
     * Play a sound immediately (silently no-ops if audio not ready).
     * @param {'click'|'enter'|'backspace'|'error'} [kind]
     */
    playClick: playClick,
  };

})(window);