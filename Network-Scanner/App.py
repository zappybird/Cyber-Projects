"""
app.py  —  Flask web GUI for Network Scanner  (v2.2)
Run:   python app.py
Open:  http://127.0.0.1:5000
"""

from flask import Flask, render_template_string, request, Response
import socket
import nmap
import json
import queue
import threading
from datetime import datetime

app = Flask(__name__)

# ──────────────────────────────────────────────────────────────────────────────
# Scanner logic
# ──────────────────────────────────────────────────────────────────────────────

def port_scan(target, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        if sock.connect_ex((target, port)) == 0:
            open_ports.append(port)
        sock.close()
    return open_ports


def banner_grab(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((target, port))
            return s.recv(1024).decode('utf-8', errors='ignore').strip()
    except Exception:
        return None


def vulnerability_scan(target):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=target, arguments="-O -sV --script=vuln")
        return nm[target]
    except Exception as e:
        return {"error": str(e)}


def run_scan(target, start_port, end_port, q):
    def emit(msg, kind="log"):
        q.put(json.dumps({"type": kind, "text": msg}))

    start_time = datetime.now()
    emit(f"NETWORK SCANNER v1.0  \u2014  {start_time.strftime('%Y-%m-%d %H:%M:%S')}", "header")
    emit(f"TARGET  : {target}")
    emit(f"PORTS   : {start_port} TO {end_port}")
    emit("", "blank")
    emit("READY.", "ready")
    emit("", "blank")

    emit("[*] INITIATING PORT SCAN...", "phase")
    open_ports = port_scan(target, start_port, end_port)
    if open_ports:
        emit(f"    OPEN PORTS FOUND: {', '.join(str(p) for p in open_ports)}", "found")
    else:
        emit("    NO OPEN PORTS DETECTED.", "warn")
    emit("", "blank")

    emit("[*] GRABBING SERVICE BANNERS...", "phase")
    banners = {}
    for port in open_ports:
        b = banner_grab(target, port)
        banners[port] = b
        emit(f"    PORT {port:>5}  \u2192  {b[:60] if b else 'NO BANNER'}", "found" if b else "dim")
    if not open_ports:
        emit("    SKIPPED \u2014 NO OPEN PORTS.", "dim")
    emit("", "blank")

    emit("[*] RUNNING VULNERABILITY SCAN \u2014 THIS MAY TAKE SEVERAL MINUTES...", "phase")
    emit("    PLEASE STAND BY...", "dim")
    vuln_info = vulnerability_scan(target)
    emit("", "blank")

    if vuln_info and "error" not in vuln_info:
        emit("\u2500" * 50, "section")
        emit("    HOST INFORMATION", "section")
        emit("\u2500" * 50, "section")
        hostnames = vuln_info.get('hostnames', [])
        if hostnames:
            names = ", ".join(h['name'] for h in hostnames if h.get('name'))
            emit(f"    HOSTNAME(S)  : {names}", "info")
        os_matches = vuln_info.get('osmatch', [])
        if os_matches:
            emit("    OS DETECTION :", "info")
            for i, m in enumerate(os_matches[:3], 1):
                name = m.get('name', 'UNKNOWN')
                acc  = m.get('accuracy', '?')
                typ  = (m.get('osclass') or [{}])[0].get('type', '\u2014')
                emit(f"      {i}. {name}", "info")
                emit(f"         ACCURACY: {acc}%   TYPE: {typ}", "dim")
        emit("", "blank")

        emit("\u2500" * 50, "section")
        emit("    VULNERABILITY RESULTS", "section")
        emit("\u2500" * 50, "section")
        vulns = vuln_info.get('vulns')
        if vulns:
            for vid, details in vulns.items():
                state = details.get('state', 'UNKNOWN')
                kind  = "vuln" if state == "VULNERABLE" else "warn"
                emit(f"    [{state}]  {vid}", kind)
                if details.get('description'):
                    desc = details['description'].strip().replace('\n', ' ')
                    emit(f"      \u2514\u2500 {desc[:100]}{'...' if len(desc) > 100 else ''}", "dim")
        else:
            emit("    NO KNOWN VULNERABILITIES DETECTED.", "ok")
    else:
        err = vuln_info.get("error", "Unknown error") if vuln_info else "Scan returned no data."
        emit(f"    ERROR: {err}", "vuln")

    end_time = datetime.now()
    elapsed  = str(end_time - start_time).split('.')[0]
    emit("", "blank")
    emit("\u2550" * 52, "div")
    emit(f"SCAN COMPLETE  \u2014  DURATION: {elapsed}", "header")
    emit("\u2550" * 52, "div")
    emit("", "blank")
    q.put(json.dumps({"type": "done"}))


# ──────────────────────────────────────────────────────────────────────────────
# HTML — corrected selectors, terminal_sfx.js integration, GITS intro
# ──────────────────────────────────────────────────────────────────────────────

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>network_scan.py</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');

  /*
   * Linux TTY / phosphor green aesthetic.
   * Three shades of green only — bright, mid, dim.
   * Pure black background. No borders, no bezel, no radius.
   * Feels like ssh'd into a machine at 3am.
   */
  :root {
    --bg:       #000000;
    --bright:   #00ff41;   /* phosphor bright  — headers, found, ready   */
    --mid:      #00c832;   /* phosphor mid     — body text, info, phase   */
    --dim:      #005c1a;   /* phosphor dim     — secondary, dividers      */
    --warn:     #00e028;   /* slightly off     — warnings (still green)   */
    --glow:     0 0 6px #00ff4166;
    --glow-dim: 0 0 3px #00ff4122;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    font-family: 'VT323', monospace;
    font-size: 18px;
    color: var(--mid);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding: 0;
    /* subtle phosphor scanlines */
    background-image: repeating-linear-gradient(
      0deg,
      transparent,
      transparent 3px,
      rgba(0, 255, 65, 0.03) 3px,
      rgba(0, 255, 65, 0.03) 4px
    );
  }

  /* Full-width TTY layout — no bezel, no card, no centering box */
  .bezel {
    width: 100%;
    max-width: 100%;
    padding: 16px 24px 12px;
    background: transparent;
    border: none;
    border-radius: 0;
    box-shadow: none;
  }

  /* Title bar becomes a plain top status line like a tmux bar */
  .title-bar {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    border-bottom: 1px solid var(--dim);
    padding-bottom: 6px;
    margin-bottom: 14px;
  }
  .title-bar h1 {
    font-size: 1.1rem;
    letter-spacing: 0.2em;
    color: var(--bright);
    text-shadow: var(--glow);
    font-weight: normal;
  }
  .title-bar .badge {
    font-size: 0.85rem;
    color: var(--dim);
    letter-spacing: 0.1em;
  }

  /* Input row — inline, minimal, like typing args on a shell prompt */
  .input-panel {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 6px 16px;
    margin-bottom: 12px;
    border-bottom: 1px solid var(--dim);
    padding-bottom: 10px;
  }
  .field-group {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .field-group label {
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    color: var(--dim);
    white-space: nowrap;
  }
  .field-group input {
    background: transparent;
    border: none;
    border-bottom: 1px solid var(--mid);
    color: var(--bright);
    font-family: 'VT323', monospace;
    font-size: 1rem;
    padding: 2px 6px;
    outline: none;
    width: 130px;
    transition: border-color 0.15s, text-shadow 0.15s;
    caret-color: var(--bright);
  }
  .field-group input:focus {
    border-bottom-color: var(--bright);
    text-shadow: var(--glow);
  }
  .field-group input::placeholder { color: var(--dim); }
  /* Remove number spinners */
  .field-group input[type=number]::-webkit-inner-spin-button,
  .field-group input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; }
  .field-group input[type=number] { -moz-appearance: textfield; }

  button#scan-btn {
    background: transparent;
    border: 1px solid var(--mid);
    color: var(--bright);
    cursor: pointer;
    font-family: 'VT323', monospace;
    font-size: 1rem;
    letter-spacing: 0.2em;
    padding: 3px 18px;
    transition: background 0.1s, text-shadow 0.1s, border-color 0.1s;
    white-space: nowrap;
    border-radius: 0;
  }
  button#scan-btn:hover {
    background: var(--bright);
    color: var(--bg);
    border-color: var(--bright);
    text-shadow: none;
  }
  button#scan-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
    background: transparent;
    color: var(--dim);
    border-color: var(--dim);
  }

  /*
   * #terminalOutput — full-width, no border, pure terminal.
   * Height fills remaining viewport. Scrollbar styled to match.
   */
  #terminalOutput {
    background: transparent;
    border: none;
    padding: 4px 0;
    height: calc(100vh - 180px);
    min-height: 320px;
    overflow-y: auto;
    font-family: 'VT323', monospace;
    font-size: 1rem;
    line-height: 1.5;
    white-space: pre-wrap;
    word-break: break-word;
    color: var(--mid);
    text-shadow: var(--glow-dim);
    scrollbar-width: thin;
    scrollbar-color: var(--dim) transparent;
  }
  #terminalOutput::-webkit-scrollbar { width: 4px; }
  #terminalOutput::-webkit-scrollbar-track { background: transparent; }
  #terminalOutput::-webkit-scrollbar-thumb { background: var(--dim); }

  /* All line types use green shades only */
  .line           { display: block; color: var(--mid); }
  .line.header    { color: var(--bright); text-shadow: var(--glow); letter-spacing: 0.06em; }
  .line.phase     { color: var(--bright); }
  .line.section   { color: var(--bright); }
  .line.found     { color: var(--bright); text-shadow: var(--glow); }
  .line.ok        { color: var(--bright); text-shadow: var(--glow); }
  .line.warn      { color: var(--warn); }
  .line.vuln      { color: var(--bright); text-shadow: var(--glow); }   /* bright = danger stands out */
  .line.dim       { color: var(--dim); }
  .line.info      { color: var(--mid); }
  .line.ready     { color: var(--bright); text-shadow: var(--glow); }
  .line.div       { color: var(--dim); }
  .line.blank     { display: block; height: 0.4em; }

  /* Block cursor — classic Linux terminal underscore/block style */
  .cursor {
    display: inline-block;
    width: 0.6em;
    height: 1.05em;
    background: var(--bright);
    box-shadow: var(--glow);
    animation: blink 1.0s step-end infinite;
    vertical-align: text-bottom;
    margin-left: 1px;
  }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }

  /* Status bar — like a shell prompt line at the bottom */
  .status-bar {
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
    padding-top: 6px;
    border-top: 1px solid var(--dim);
    font-size: 0.85rem;
    letter-spacing: 0.1em;
    color: var(--dim);
  }
  #status-text { color: var(--mid); }
</style>
</head>
<body>

<div class="bezel">
  <div class="title-bar">
    <h1>root@scanner:~#&nbsp;./network_scan.py</h1>
    <span class="badge">tty1 | pts/0 | v2.2</span>
  </div>

  <div class="input-panel">
    <div class="field-group">
      <label>--target</label>
      <input type="text"   id="target"     placeholder="192.168.1.1">
    </div>
    <div class="field-group">
      <label>--port-start</label>
      <input type="number" id="start-port" placeholder="1"   value="1"   min="1" max="65535">
    </div>
    <div class="field-group">
      <label>--port-end</label>
      <input type="number" id="end-port"   placeholder="100" value="100" min="1" max="65535">
    </div>
    <button id="scan-btn" onclick="startScan()">[ SCAN ]</button>
  </div>

  <!--
    THE ONLY output element. terminal_sfx.js selectors point here.
    appendLine() appends <span> children.
    TerminalSFX.typeOut() appends text nodes (for the intro).
    Both coexist safely because white-space:pre-wrap handles newlines.
  -->
  <pre id="terminalOutput" aria-live="polite"></pre>

  <div class="status-bar">
    <span id="status-text">IDLE</span>
    <span id="elapsed-text"></span>
  </div>
</div>

<!-- Load terminal_sfx.js before the inline script -->
<script src="{{ url_for('static', filename='terminal_sfx.js') }}"></script>

<script>
  'use strict';

  // ─── References ────────────────────────────────────────────────────────────
  const output   = document.getElementById('terminalOutput');
  const statusEl = document.getElementById('status-text');
  const elapsedEl = document.getElementById('elapsed-text');

  let eventSource = null;
  let startTs     = null;
  let timerHandle = null;
  let introShown  = false;

  // ─── Cursor helpers ────────────────────────────────────────────────────────

  function ensureCursor() {
    // Remove any existing cursor first, then append a fresh one at the end
    const old = output.querySelector('.cursor');
    if (old) old.remove();
    const cur = document.createElement('span');
    cur.className = 'cursor';
    output.appendChild(cur);
  }

  function removeCursor() {
    const cur = output.querySelector('.cursor');
    if (cur) cur.remove();
  }

  // ─── appendLine ────────────────────────────────────────────────────────────
  // Appends a styled <span> line to #terminalOutput and plays a sound.
  // Called by the SSE message handler for every line the scanner emits.

  function appendLine(text, cls) {
    removeCursor();

    if (cls === 'blank') {
      const gap = document.createElement('span');
      gap.className = 'line blank';
      output.appendChild(gap);
    } else {
      const span = document.createElement('span');
      span.className = 'line ' + (cls || '');
      span.textContent = text;
      output.appendChild(span);

      // Direct sound call — more reliable than waiting for MutationObserver
      if (window.TerminalSFX) {
        window.TerminalSFX.playClick(cls === 'vuln' ? 'error' : 'click');
      }
    }

    // Explicit newline so the pre renders lines correctly
    output.appendChild(document.createTextNode('\n'));
    ensureCursor();
    output.scrollTop = output.scrollHeight;
  }

  // ─── Status & timer ────────────────────────────────────────────────────────

  function setStatus(msg) { statusEl.textContent = msg; }

  function startTimer() {
    startTs = Date.now();
    timerHandle = setInterval(function () {
      const s  = Math.floor((Date.now() - startTs) / 1000);
      const m  = Math.floor(s / 60);
      const ss = String(s % 60).padStart(2, '0');
      elapsedEl.textContent = m + ':' + ss + ' ELAPSED';
    }, 1000);
  }

  function stopTimer() { clearInterval(timerHandle); }

  // ─── GITS intro animation ──────────────────────────────────────────────────
  // Runs exactly once, on the first user gesture, after audio is unlocked.
  // TerminalSFX.typeOut() handles character-by-character animation + sounds.

  function showIntro() {
    if (introShown) return;
    introShown = true;

    const now  = new Date();
    const pad  = n => String(n).padStart(2, '0');
    const ts   = now.getFullYear()        + '-' +
                 pad(now.getMonth() + 1)  + '-' +
                 pad(now.getDate())       + ' ' +
                 pad(now.getHours())      + ':' +
                 pad(now.getMinutes())    + ':' +
                 pad(now.getSeconds());

    const text = (
      'Linux 6.8.0-generic #36-Ubuntu SMP\n'  +
      'network_scan.py  --  port scanner / vuln audit\n\n' +
      '[  0.000] Initialising network interfaces...\n'  +
      '[  0.012] Loading nmap engine...\n'              +
      '[  0.031] Binding raw socket...\n'               +
      '[  0.044] System ready.\n\n'                    +
      'Usage: enter target IP and port range,\n'       +
      'then press [ SCAN ] to begin.\n\n'
    );

    // Wipe placeholder text, then animate the intro
    output.textContent = '';

    window.TerminalSFX.typeOut(text, {
      charDelay:      55,
      jitterMs:       20,
      newlinePauseMs: 280,
      onComplete: function () {
        ensureCursor();
        setStatus('ready.');
        document.getElementById('target').focus();
      }
    });
  }

  // ─── TerminalSFX init ──────────────────────────────────────────────────────
  //
  // Key points:
  //   - intro.enabled:false  →  we drive the intro from onFirstGesture()
  //                             so we control exact timing after unlock.
  //   - selectors.input      →  '#target' (the IP field, the most-typed input)
  //   - selectors.output     →  '#terminalOutput' (MutationObserver target)
  //   - mode:'observer'      →  observer watches for SSE-appended spans;
  //                             appendLine() also calls playClick() directly
  //                             as a belt-and-suspenders approach.

  window.TerminalSFX.init({
    selectors: {
      input:  '#target',
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
    },
    intro: { enabled: false },   // managed manually below
    cooldownMs:       18,
    maxRatePerSecond: 30,
    mode: 'observer',
  });

  // ─── First gesture handler ─────────────────────────────────────────────────
  // Audio unlock must happen inside a user gesture (browser rule).
  // The visual intro starts immediately on page load — sounds will be silent
  // until the user first clicks or presses a key, then play normally after that.

  function onFirstGesture() {
    window.TerminalSFX.unlock();
    // listeners are { once:true } so they auto-remove after firing
  }

  window.addEventListener('keydown', onFirstGesture, { once: true, passive: true });
  window.addEventListener('click',   onFirstGesture, { once: true, passive: true });

  // Start the intro animation immediately — no gesture needed for visuals.
  // Audio kicks in silently until the first interaction unlocks it.
  document.addEventListener('DOMContentLoaded', function () {
    setTimeout(showIntro, 400);  // brief pause so the page finishes rendering first
  });

  // ─── Scan ──────────────────────────────────────────────────────────────────

  function startScan() {
    const target    = document.getElementById('target').value.trim();
    const startPort = document.getElementById('start-port').value.trim();
    const endPort   = document.getElementById('end-port').value.trim();

    if (!target || !startPort || !endPort) {
      appendLine('?SYNTAX ERROR \u2014 ALL FIELDS REQUIRED.', 'vuln');
      return;
    }

    if (eventSource) eventSource.close();

    output.textContent = '';
    ensureCursor();

    document.getElementById('scan-btn').disabled = true;
    setStatus('scanning...');
    startTimer();

    const url = '/scan?target=' + encodeURIComponent(target)
              + '&start='       + encodeURIComponent(startPort)
              + '&end='         + encodeURIComponent(endPort);

    eventSource = new EventSource(url);

    eventSource.onmessage = function (e) {
      const data = JSON.parse(e.data);
      if (data.type === 'done') {
        eventSource.close();
        document.getElementById('scan-btn').disabled = false;
        setStatus('done.');
        stopTimer();
        return;
      }
      appendLine(data.text, data.type);
    };

    eventSource.onerror = function () {
      appendLine('?CONNECTION ERROR \u2014 SCAN ABORTED.', 'vuln');
      eventSource.close();
      document.getElementById('scan-btn').disabled = false;
      setStatus('error');
      stopTimer();
    };
  }

  // Enter key in any input starts the scan
  document.addEventListener('DOMContentLoaded', function () {
    ['target', 'start-port', 'end-port'].forEach(function (id) {
      document.getElementById(id).addEventListener('keydown', function (e) {
        if (e.key === 'Enter') startScan();
      });
    });
  });

  // Brief placeholder shown for ~400ms before the intro animation begins
  output.textContent = 'root@scanner:~# ./network_scan.py\n\nINITIALISING...';
  ensureCursor();
</script>
</body>
</html>"""


# ──────────────────────────────────────────────────────────────────────────────
# Routes
# ──────────────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template_string(HTML)


@app.route('/scan')
def scan():
    target     = request.args.get('target', '').strip()
    start_port = int(request.args.get('start', 1))
    end_port   = int(request.args.get('end',   100))

    q = queue.Queue()

    def background():
        try:
            run_scan(target, start_port, end_port, q)
        except Exception as ex:
            q.put(json.dumps({"type": "vuln", "text": f"FATAL ERROR: {ex}"}))
            q.put(json.dumps({"type": "done"}))

    threading.Thread(target=background, daemon=True).start()

    def stream():
        while True:
            item = q.get()
            yield f"data: {item}\n\n"
            if json.loads(item).get("type") == "done":
                break

    return Response(
        stream(),
        mimetype='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
    )


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n  ■ NETWORK SCANNER GUI  v2.2")
    print("  Open your browser \u2192 http://127.0.0.1:5000\n")
    app.run(host='127.0.0.1', port=5000, debug=False)