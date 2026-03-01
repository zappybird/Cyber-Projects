<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Changelog — Network &amp; Vulnerability Scanner</title>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 16px;
    line-height: 1.6;
    color: #24292e;
    background: #ffffff;
    max-width: 800px;
    margin: 0 auto;
    padding: 32px 24px 64px;
  }

  h1 {
    font-size: 2em;
    font-weight: 600;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
    margin-top: 0;
    margin-bottom: 16px;
  }

  h2 {
    font-size: 1.5em;
    font-weight: 600;
    border-bottom: 1px solid #eaecef;
    padding-bottom: 0.3em;
    margin-top: 32px;
    margin-bottom: 16px;
  }

  p {
    margin-top: 0;
    margin-bottom: 16px;
    color: #586069;
  }

  hr {
    border: none;
    border-top: 1px solid #eaecef;
    margin: 24px 0;
  }

  code {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 85%;
    background-color: rgba(27,31,35,0.05);
    border-radius: 3px;
    padding: 0.2em 0.4em;
  }

  strong { font-weight: 600; color: #24292e; }

  /* Entry list */
  .entry-list {
    list-style: none;
    padding: 0;
    margin: 0 0 16px;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .entry {
    display: flex;
    gap: 12px;
    align-items: baseline;
    padding: 10px 14px;
    border: 1px solid #eaecef;
    border-radius: 6px;
    background: #fafafa;
  }

  .tag {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.7em;
    font-weight: 600;
    letter-spacing: 0.06em;
    padding: 2px 8px;
    border-radius: 3px;
    border: 1px solid;
    white-space: nowrap;
    flex-shrink: 0;
    align-self: flex-start;
    margin-top: 2px;
  }

  .tag.added    { background: #f0fff4; color: #22863a; border-color: #a8d5b5; }
  .tag.improved { background: #f1f8ff; color: #0366d6; border-color: #a8caed; }
  .tag.changed  { background: #fffbf0; color: #b08800; border-color: #e0cc80; }
  .tag.removed  { background: #fff5f5; color: #cb2431; border-color: #f0a8ad; }

  .entry-body {
    font-size: 0.93em;
    color: #24292e;
    line-height: 1.6;
  }
</style>
</head>
<body>

<h1>Changelog</h1>
<p>All notable changes to the Network &amp; Vulnerability Scanner, compiled from v1.0 to present.</p>

<hr />

<h2>v2.2</h2>

<ul class="entry-list">

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Ghost-in-the-Shell intro animation</strong> — on the first user gesture, an animated
      typewriter sequence prints to <code>#terminalOutput</code> before the user types anything.
      Text is character-by-character with randomised timing, newline pauses, and per-character
      sounds. Default intro includes a live timestamp and the scanner header block. Override via
      <code>init({ intro: { text: '...' } })</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong><code>newlinePauseMs</code> option in <code>typeOut()</code></strong> — configurable
      extra delay inserted after each <code>\n</code> character for dramatic pacing. Defaults to
      <code>0</code> in manual calls, <code>160</code>ms in the intro sequence.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong><code>onComplete</code> callback in <code>typeOut()</code></strong> — optional function
      called when the typewriter animation finishes. Used internally by the intro to auto-focus
      <code>#cmdInput</code> after the boot sequence completes.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Live timestamp in default intro text</strong> — intro text is generated at unlock time
      (not at parse time) so the timestamp reflects when the user first interacted, not when the
      page loaded.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>Root cause fix: AudioContext not unlocking</strong> — the <code>AudioContext</code>
      is now created <em>inside</em> the gesture event handler (<code>unlock()</code>), not at
      <code>init()</code> time. Browsers (Chrome, Firefox, Safari) require the context to be created
      or resumed synchronously within a user-gesture call stack. Creating it at init caused an
      immediately-suspended context that <code>.resume()</code> could not reliably wake.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>Two-phase buffer loading</strong> — WAV files are now fetched as raw
      <code>ArrayBuffer</code>s at <code>init()</code> time via <code>fetch()</code> (no gesture
      needed). <code>decodeAudioData()</code> is deferred until <code>onUnlocked()</code>, after the
      <code>AudioContext</code> exists. The <code>.slice(0)</code> clone prevents the
      <code>decodeAudioData</code> detachment bug on the original buffer.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>Unlock listeners moved to <code>window</code></strong> — previously attached to
      <code>document</code>; now attached to <code>window</code> for broadest gesture capture,
      matching the spec requirement. Manual removal of sibling listeners added alongside
      <code>{ once: true }</code> for belt-and-suspenders cleanup.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong><code>playBuffer()</code> guard tightened</strong> — now checks
      <code>audioCtx.state === 'running'</code> explicitly (not just <code>audioUnlocked</code>)
      before attempting <code>source.start()</code>, preventing silent errors during the brief
      window between unlock() being called and the context fully resuming.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong><code>typeOut()</code> now uses <code>observerPaused</code> flag</strong> — instead
      of disconnecting and reconnecting the <code>MutationObserver</code> (which was racey), the
      observer now checks a boolean flag and skips processing while <code>typeOut()</code> is
      animating. Observer stays connected throughout, eliminating any missed mutations.
    </div>
  </li>

  <li class="entry">
    <span class="tag changed">CHANGED</span>
    <div class="entry-body">
      <strong>Intro text is <code>null</code> by default</strong> — the config stores
      <code>intro.text: null</code> rather than a hardcoded string. The live timestamp is built at
      runtime in <code>runIntro()</code> using a local <code>nowTimestamp()</code> helper, ensuring
      it reflects the actual interaction time rather than page-load time.
    </div>
  </li>

</ul>

<h3 style="font-size:1rem; font-weight:600; margin: 20px 0 12px; color:#24292e;">app.py changes (v2.2)</h3>

<ul class="entry-list">

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>GITS intro animation wired into Flask template</strong> — <code>showIntro()</code>
      is triggered from <code>onFirstGesture()</code> in the inline script, 100ms after
      <code>TerminalSFX.unlock()</code> fires, so the unlock keydown sound plays before the
      typewriter sequence begins.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Dual-path sound triggering in <code>appendLine()</code></strong> —
      <code>appendLine()</code> now calls <code>TerminalSFX.playClick()</code> directly on every
      line it appends, in addition to the MutationObserver. This belt-and-suspenders approach
      ensures sounds fire on SSE lines even if the observer fires late or is briefly paused.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>Output element corrected to <code>#terminalOutput</code></strong> — the screen
      container was previously <code>id="screen"</code> (a <code>&lt;div&gt;</code>), which
      mismatched the selectors in <code>terminal_sfx.js</code>. It is now
      <code>&lt;pre id="terminalOutput"&gt;</code>, matching the JS defaults exactly. This was
      the primary reason the MutationObserver never attached correctly.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong><code>appendLine()</code> rewritten to use <code>&lt;span&gt;</code> children</strong>
      — previously used <code>&lt;div&gt;</code> elements, which broke layout inside
      <code>&lt;pre&gt;</code>. Now appends <code>&lt;span class="line ..."&gt;</code> followed by
      an explicit text-node newline, which renders correctly with <code>white-space:pre-wrap</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>Cursor managed as a persistent last child</strong> — <code>ensureCursor()</code>
      removes any existing cursor and appends a fresh one at the end of
      <code>#terminalOutput</code> after every write. <code>removeCursor()</code> strips it before
      each write. This prevents duplicate cursors and keeps the blinking cursor always at the
      bottom of visible output.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong><code>TerminalSFX.init()</code> called with explicit config</strong> — all selectors,
      sound paths, and throttle values are passed explicitly rather than relying on defaults, making
      the integration self-documenting and resilient to future config-default changes.
      <code>intro.enabled: false</code> is set so the built-in intro does not compete with the
      manually-driven <code>showIntro()</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag changed">CHANGED</span>
    <div class="entry-body">
      <strong>First-gesture listeners moved to <code>window</code> in inline script</strong> —
      previously the template had no gesture listeners at all. Now two <code>{ once: true }</code>
      listeners on <code>window</code> (keydown and click) call <code>onFirstGesture()</code>,
      which unlocks audio and schedules the intro. Matches the pattern in
      <code>terminal_sfx.js</code> itself.
    </div>
  </li>

  <li class="entry">
    <span class="tag removed">REMOVED</span>
    <div class="entry-body">
      <strong>Hardcoded static intro HTML removed from template</strong> — the old template
      pre-populated the screen with static <code>&lt;div&gt;</code> lines ("**** NETWORK SCANNER
      V1.0 ****", "READY.", etc.) that were never animated or tied to audio. These are now replaced
      by a single plain-text placeholder that <code>showIntro()</code> wipes and replaces with the
      animated sequence on first gesture.
    </div>
  </li>

</ul>

<hr />

<h2>v2.1</h2>

<ul class="entry-list">

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Terminal sound effects (<code>terminal_sfx.js</code>)</strong> — new standalone JavaScript file
      that adds Ghost in the Shell / Matrix style typewriter audio to the Flask GUI. Place at
      <code>/static/terminal_sfx.js</code> and include via
      <code>{{ url_for('static', filename='terminal_sfx.js') }}</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Web Audio API integration</strong> — single shared <code>AudioContext</code> initialised in
      suspended state to comply with browser autoplay restrictions. Context is resumed only on a real user
      gesture (click, keydown, or touchend) via <code>TerminalSFX.unlock()</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Multi-sample click engine</strong> — loads up to four click samples
      (<code>click1.wav</code>–<code>click4.wav</code>) from <code>/static/sfx/</code> and randomly
      selects one per keystroke. Dedicated sounds for <code>enter.wav</code>, <code>backspace.wav</code>,
      and optional <code>error.wav</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Per-play audio jitter</strong> — each sound is played with randomised volume (±15% of base)
      and playback rate (±3%) for an organic, non-robotic feel that matches the Ghost in the Shell aesthetic.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Throttling and rate limiting</strong> — configurable cooldown between sounds (default 20 ms)
      and a hard cap of 30 sounds per second prevent audio spam on held keys or large output bursts.
      Paste events and bulk appends above the configurable <code>bulkThreshold</code> (default 20 chars)
      collapse to a single sound.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Input typing hooks</strong> — attaches to <code>#cmdInput</code> (configurable) via
      <code>keydown</code>. Plays the appropriate sound per key: printable characters trigger a random
      click, Enter triggers <code>enter.wav</code>, Backspace/Delete trigger <code>backspace.wav</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Output observer mode</strong> — a <code>MutationObserver</code> watches <code>#terminalOutput</code>
      and plays sounds as new text is appended by the SSE stream. Bulk mutations are collapsed to a single
      sound. Configurable via <code>mode: "observer"</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong><code>TerminalSFX.typeOut(text, opts)</code></strong> — public method that appends text to the
      output element character by character with a configurable delay and per-character sounds. Automatically
      disconnects the MutationObserver during playback to prevent double-firing, then reconnects on completion.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Public API on <code>window.TerminalSFX</code></strong> — four methods exposed:
      <code>init(configOverride)</code>, <code>unlock()</code>, <code>typeOut(text, opts)</code>,
      and <code>playClick(kind)</code>. All are safe to call regardless of audio lock state — no errors
      are thrown if audio is unavailable.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Top-level config object</strong> — all selectors, sound paths, volume levels, jitter ranges,
      cooldowns, thresholds, and feature flags are defined in one <code>DEFAULT_CONFIG</code> block at the
      top of the file and overridable at runtime via <code>TerminalSFX.init({ ... })</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Sound file structure</strong> — new <code>/static/sfx/</code> directory convention established.
      Required files: <code>click1–4.wav</code>, <code>enter.wav</code>, <code>backspace.wav</code>.
      Optional: <code>error.wav</code>. All missing files are handled gracefully with no thrown errors.
    </div>
  </li>

</ul>

<hr />

<h2>v2.0</h2>

<ul class="entry-list">

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Browser-based GUI (<code>app.py</code>)</strong> — a new Flask server entry point running on
      <code>http://127.0.0.1:5000</code>. Provides an interactive terminal-style interface in the browser as an
      alternative to the CLI. Accepts the same three inputs as <code>scanner.py</code>: target IP, start port, and end port.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Live streaming output via Server-Sent Events (SSE)</strong> — scan results in the GUI stream
      line-by-line in real time as they are produced. Users no longer wait for the full scan to finish
      before seeing any output.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Live elapsed timer</strong> — the GUI status bar counts up continuously during an active scan,
      making scan duration visible without waiting for the final summary line.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Color-coded terminal output (CLI)</strong> — ANSI color classes applied across all CLI output:
      cyan for active scan phases, green for open ports and clean results, yellow for warnings, and red for
      detected vulnerabilities. Dimmed color for secondary detail lines.
    </div>
  </li>

  <li class="entry">
    <span class="tag added">ADDED</span>
    <div class="entry-body">
      <strong>Structured section headers and dividers (CLI)</strong> — output is now divided into clearly
      labelled sections (Port Scan Results, Host Information, Vulnerability Scan) separated by horizontal
      dividers, replacing the previous flat stream of print statements.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>OS match formatting</strong> — raw nested dictionary output replaced with a clean numbered list
      showing the top three OS matches. Each entry displays name, accuracy percentage, and device type only.
      Previously the full Python dict including <code>line</code>, <code>cpe</code>, and <code>osclass</code>
      arrays was printed verbatim.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>Banner grabbing flow</strong> — banners are now silently collected into a dictionary keyed by
      port number during the scan phase, then displayed in a formatted port table alongside open port and state
      columns. Previously each banner attempt printed its own interleaved status line mid-scan.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>Vulnerability description truncation</strong> — vulnerability descriptions are now capped at
      120 characters with an ellipsis when truncated, preventing long script output from flooding the terminal.
    </div>
  </li>

  <li class="entry">
    <span class="tag improved">IMPROVED</span>
    <div class="entry-body">
      <strong>Scan duration display</strong> — microseconds are stripped from the elapsed time string.
      <code>0:04:37.630867</code> now renders as <code>0:04:37</code>.
    </div>
  </li>

  <li class="entry">
    <span class="tag changed">CHANGED</span>
    <div class="entry-body">
      <strong>Project structure</strong> — project now ships as two runnable entry points rather than one.
      <code>scanner.py</code> remains the CLI entry point. <code>app.py</code> is added as the GUI entry point.
      Both share the same underlying <code>port_scan()</code>, <code>banner_grab()</code>, and
      <code>vulnerability_scan()</code> functions.
    </div>
  </li>

  <li class="entry">
    <span class="tag changed">CHANGED</span>
    <div class="entry-body">
      <strong>Dependencies</strong> — <code>flask</code> added as a required dependency for the GUI mode.
      <code>python-nmap</code> remains required for all scan functions. <code>requests</code> removed as it
      was imported but unused in the original.
    </div>
  </li>

  <li class="entry">
    <span class="tag changed">CHANGED</span>
    <div class="entry-body">
      <strong>Example output in documentation</strong> — updated to reflect the new formatted output structure
      with section headers, the port table, and structured OS detection results, replacing the original
      single-line-per-result format.
    </div>
  </li>

  <li class="entry">
    <span class="tag removed">REMOVED</span>
    <div class="entry-body">
      <strong>Inline progress noise</strong> — status lines such as <em>"Scanning ports from X to Y on target…"</em>,
      <em>"Grabbing banner for target:port…"</em>, and <em>"Scanner target X for vulnerabilities…"</em> no longer
      appear interleaved with result output. Phase progress is now consolidated into labelled headers printed
      before each result block.
    </div>
  </li>

  <li class="entry">
    <span class="tag removed">REMOVED</span>
    <div class="entry-body">
      <strong>Raw hostname and vulnerability dict dumps</strong> — <code>print(f"Hostnames: {vuln_info['hostnames']}")</code>
      and <code>print(f"Vulnerabilities: {vuln_info['vulns']}")</code> replaced entirely with parsed,
      formatted output functions.
    </div>
  </li>

</ul>

<hr />

<h2>v1.0</h2>
<p>Initial release. Single-file CLI scanner (<code>scanner.py</code>) with port scanning, banner grabbing,
and Nmap-based OS and vulnerability detection. Raw dictionary output. No formatting.</p>

</body>
</html>