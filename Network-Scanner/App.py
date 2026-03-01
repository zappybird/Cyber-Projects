"""
app.py  –  Flask web GUI for Network Scanner
Run:  python app.py
Then open:  http://127.0.0.1:5000
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
# Scanner logic (streaming version – yields lines into a queue)
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
    """Runs the full scan and pushes SSE-formatted strings into queue q."""

    def emit(msg, kind="log"):
        q.put(json.dumps({"type": kind, "text": msg}))

    start_time = datetime.now()
    emit(f"NETWORK SCANNER v1.0  —  {start_time.strftime('%Y-%m-%d %H:%M:%S')}", "header")
    emit(f"TARGET  : {target}")
    emit(f"PORTS   : {start_port} TO {end_port}")
    emit("", "blank")
    emit("READY.", "ready")
    emit("", "blank")

    # Port scan
    emit("[*] INITIATING PORT SCAN...", "phase")
    open_ports = port_scan(target, start_port, end_port)
    if open_ports:
        emit(f"    OPEN PORTS FOUND: {', '.join(str(p) for p in open_ports)}", "found")
    else:
        emit("    NO OPEN PORTS DETECTED.", "warn")
    emit("", "blank")

    # Banner grab
    emit("[*] GRABBING SERVICE BANNERS...", "phase")
    banners = {}
    for port in open_ports:
        b = banner_grab(target, port)
        banners[port] = b
        if b:
            emit(f"    PORT {port:>5}  →  {b[:60]}", "found")
        else:
            emit(f"    PORT {port:>5}  →  NO BANNER", "dim")
    if not open_ports:
        emit("    SKIPPED — NO OPEN PORTS.", "dim")
    emit("", "blank")

    # Vuln scan
    emit("[*] RUNNING VULNERABILITY SCAN — THIS MAY TAKE SEVERAL MINUTES...", "phase")
    emit("    PLEASE STAND BY...", "dim")
    vuln_info = vulnerability_scan(target)
    emit("", "blank")

    if vuln_info and "error" not in vuln_info:
        # Host info
        emit("─── HOST INFORMATION ──────────────────────────────", "section")
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
                typ  = (m.get('osclass') or [{}])[0].get('type', '—')
                emit(f"      {i}. {name}", "info")
                emit(f"         ACCURACY: {acc}%   TYPE: {typ}", "dim")
        emit("", "blank")

        # Vulns
        emit("─── VULNERABILITY RESULTS ─────────────────────────", "section")
        vulns = vuln_info.get('vulns')
        if vulns:
            for vid, details in vulns.items():
                state = details.get('state', 'UNKNOWN')
                kind  = "vuln" if state == "VULNERABLE" else "warn"
                emit(f"    [{state}]  {vid}", kind)
                if details.get('description'):
                    desc = details['description'].strip().replace('\n', ' ')
                    emit(f"      └─ {desc[:100]}{'...' if len(desc) > 100 else ''}", "dim")
        else:
            emit("    NO KNOWN VULNERABILITIES DETECTED.", "ok")
    else:
        err = vuln_info.get("error", "Unknown error") if vuln_info else "Scan returned no data."
        emit(f"    ERROR: {err}", "vuln")

    end_time = datetime.now()
    elapsed  = str(end_time - start_time).split('.')[0]
    emit("", "blank")
    emit("═" * 52, "div")
    emit(f"SCAN COMPLETE  —  DURATION: {elapsed}", "header")
    emit("═" * 52, "div")
    emit("", "blank")
    q.put(json.dumps({"type": "done"}))


# ──────────────────────────────────────────────────────────────────────────────
# HTML template  —  Commodore 64 / BASIC aesthetic
# ──────────────────────────────────────────────────────────────────────────────

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>NETWORK SCANNER</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

  :root {
    --bg:      #1a0a2e;
    --screen:  #0d0d1a;
    --text:    #7b68ee;
    --bright:  #b39ddb;
    --cyan:    #64ffda;
    --green:   #69ff47;
    --yellow:  #ffeb3b;
    --red:     #ff5252;
    --dim:     #4a3f6b;
    --border:  #3d2b6b;
    --glow:    0 0 8px #7b68ee88;
    --glow2:   0 0 14px #b39ddb55;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    font-family: 'Share Tech Mono', monospace;
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 24px 12px;
    /* subtle scanline overlay */
    background-image:
      repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.18) 2px,
        rgba(0,0,0,0.18) 4px
      );
  }

  /* ── Outer bezel ── */
  .bezel {
    width: 100%;
    max-width: 860px;
    background: linear-gradient(145deg, #2a1a4e, #1a0a2e);
    border: 3px solid var(--border);
    border-radius: 12px;
    box-shadow:
      0 0 0 2px #0d0822,
      0 0 40px #7b68ee33,
      inset 0 0 30px rgba(0,0,0,0.5);
    padding: 28px 28px 24px;
  }

  /* ── Title bar ── */
  .title-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
    margin-bottom: 20px;
  }
  .title-bar h1 {
    font-size: 1rem;
    letter-spacing: 0.25em;
    color: var(--bright);
    text-shadow: var(--glow);
  }
  .title-bar .badge {
    font-size: 0.65rem;
    color: var(--dim);
    letter-spacing: 0.15em;
  }

  /* ── Input panel ── */
  .input-panel {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr auto;
    gap: 10px;
    margin-bottom: 16px;
  }
  .field-group {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .field-group label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: var(--dim);
  }
  .field-group input {
    background: var(--screen);
    border: 1px solid var(--border);
    border-radius: 4px;
    color: var(--cyan);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    padding: 7px 10px;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    width: 100%;
  }
  .field-group input:focus {
    border-color: var(--text);
    box-shadow: var(--glow);
  }
  .field-group input::placeholder { color: var(--dim); }

  button#scan-btn {
    align-self: flex-end;
    background: transparent;
    border: 2px solid var(--text);
    border-radius: 4px;
    color: var(--bright);
    cursor: pointer;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.2em;
    padding: 7px 20px;
    transition: background 0.15s, box-shadow 0.15s, color 0.15s;
    white-space: nowrap;
  }
  button#scan-btn:hover {
    background: var(--text);
    color: var(--screen);
    box-shadow: var(--glow);
  }
  button#scan-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    background: transparent;
    color: var(--dim);
    border-color: var(--dim);
  }

  /* ── Screen area ── */
  .screen {
    background: var(--screen);
    border: 2px solid var(--border);
    border-radius: 6px;
    box-shadow: inset 0 0 20px rgba(0,0,0,0.6), var(--glow2);
    padding: 16px 18px;
    height: 480px;
    overflow-y: auto;
    font-size: 0.82rem;
    line-height: 1.65;
    position: relative;
    scrollbar-width: thin;
    scrollbar-color: var(--border) var(--screen);
  }
  .screen::-webkit-scrollbar { width: 6px; }
  .screen::-webkit-scrollbar-track { background: var(--screen); }
  .screen::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

  /* line types */
  .line           { color: var(--text); }
  .line.header    { color: var(--bright); font-size: 0.9rem; letter-spacing: 0.1em; }
  .line.phase     { color: var(--cyan); }
  .line.section   { color: var(--bright); }
  .line.found     { color: var(--green); }
  .line.ok        { color: var(--green); }
  .line.warn      { color: var(--yellow); }
  .line.vuln      { color: var(--red); }
  .line.dim       { color: var(--dim); }
  .line.info      { color: var(--text); }
  .line.ready     { color: var(--green); animation: blink 1s step-end 3; }
  .line.div       { color: var(--border); }
  .line.blank     { height: 0.4em; }

  /* blinking cursor */
  .cursor {
    display: inline-block;
    width: 0.6em;
    height: 1em;
    background: var(--text);
    animation: blink 0.9s step-end infinite;
    vertical-align: text-bottom;
    margin-left: 2px;
  }

  @keyframes blink {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0; }
  }

  /* status bar */
  .status-bar {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
    font-size: 0.62rem;
    letter-spacing: 0.15em;
    color: var(--dim);
    padding: 0 2px;
  }
  #status-text { color: var(--text); }
</style>
</head>
<body>

<div class="bezel">
  <div class="title-bar">
    <h1>■ NETWORK SCANNER</h1>
    <span class="badge">BASIC v2.0  64K RAM SYSTEM</span>
  </div>

  <div class="input-panel">
    <div class="field-group">
      <label>TARGET IP</label>
      <input type="text" id="target" placeholder="192.168.1.1" value="">
    </div>
    <div class="field-group">
      <label>START PORT</label>
      <input type="number" id="start-port" placeholder="1" value="1" min="1" max="65535">
    </div>
    <div class="field-group">
      <label>END PORT</label>
      <input type="number" id="end-port" placeholder="100" value="100" min="1" max="65535">
    </div>
    <button id="scan-btn" onclick="startScan()">RUN</button>
  </div>

  <div class="screen" id="screen">
    <div class="line header">**** NETWORK SCANNER V1.0 ****</div>
    <div class="line dim">64K RAM SYSTEM  38911 BASIC BYTES FREE</div>
    <div class="line blank"></div>
    <div class="line">READY.</div>
    <div class="line blank"></div>
    <div class="line dim">ENTER TARGET IP AND PORT RANGE, THEN PRESS [RUN].</div>
    <div class="line blank"></div>
    <span class="cursor"></span>
  </div>

  <div class="status-bar">
    <span id="status-text">IDLE</span>
    <span id="elapsed-text"></span>
  </div>
</div>

<script>
  let eventSource = null;
  let startTs     = null;
  let timerHandle = null;

  function getScreen() { return document.getElementById('screen'); }

  function clearScreen() {
    getScreen().innerHTML = '';
  }

  function appendLine(text, cls) {
    const screen = getScreen();

    // Remove old cursor if present
    const oldCursor = screen.querySelector('.cursor');
    if (oldCursor) oldCursor.remove();

    if (cls === 'blank') {
      const d = document.createElement('div');
      d.className = 'line blank';
      screen.appendChild(d);
    } else {
      const d = document.createElement('div');
      d.className = 'line ' + (cls || '');
      d.textContent = text;
      screen.appendChild(d);
    }

    // Append cursor at end
    const cur = document.createElement('span');
    cur.className = 'cursor';
    screen.appendChild(cur);

    screen.scrollTop = screen.scrollHeight;
  }

  function setStatus(msg) {
    document.getElementById('status-text').textContent = msg;
  }

  function startTimer() {
    startTs = Date.now();
    timerHandle = setInterval(() => {
      const s = Math.floor((Date.now() - startTs) / 1000);
      const m = Math.floor(s / 60);
      const ss = String(s % 60).padStart(2, '0');
      document.getElementById('elapsed-text').textContent = `${m}:${ss} ELAPSED`;
    }, 1000);
  }

  function stopTimer() {
    clearInterval(timerHandle);
  }

  function startScan() {
    const target    = document.getElementById('target').value.trim();
    const startPort = document.getElementById('start-port').value.trim();
    const endPort   = document.getElementById('end-port').value.trim();

    if (!target || !startPort || !endPort) {
      appendLine('?SYNTAX ERROR — ALL FIELDS REQUIRED.', 'vuln');
      return;
    }

    if (eventSource) { eventSource.close(); }

    clearScreen();
    document.getElementById('scan-btn').disabled = true;
    setStatus('SCANNING...');
    startTimer();

    const url = `/scan?target=${encodeURIComponent(target)}&start=${encodeURIComponent(startPort)}&end=${encodeURIComponent(endPort)}`;
    eventSource = new EventSource(url);

    eventSource.onmessage = (e) => {
      const data = JSON.parse(e.data);
      if (data.type === 'done') {
        eventSource.close();
        document.getElementById('scan-btn').disabled = false;
        setStatus('SCAN COMPLETE');
        stopTimer();
        return;
      }
      appendLine(data.text, data.type);
    };

    eventSource.onerror = () => {
      appendLine('?CONNECTION ERROR — SCAN ABORTED.', 'vuln');
      eventSource.close();
      document.getElementById('scan-btn').disabled = false;
      setStatus('ERROR');
      stopTimer();
    };
  }

  // Allow Enter key in inputs to trigger scan
  document.addEventListener('DOMContentLoaded', () => {
    ['target','start-port','end-port'].forEach(id => {
      document.getElementById(id).addEventListener('keydown', e => {
        if (e.key === 'Enter') startScan();
      });
    });
  });
<script src="{{ url_for('static', filename='terminal_sfx.js') }}"></script>
<script>
  window.TerminalSFX.init();
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
    end_port   = int(request.args.get('end', 100))

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

    return Response(stream(), mimetype='text/event-stream',
                    headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})


# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("\n  ■ NETWORK SCANNER GUI")
    print("  Open your browser → http://127.0.0.1:5000\n")
    app.run(host='127.0.0.1', port=5000, debug=False)
    ## test comment for commit