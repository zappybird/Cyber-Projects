# Keylogger (Educational Cybersecurity Demo)

This project is a transparent, non‑stealth keylogging demonstration intended **solely for personal cybersecurity learning, debugging, and defensive research**.  
It records keyboard input with timestamps and saves it to a local log file defined in `config.ini`.

This tool is **not** designed for covert use, monitoring others, or any activity that violates privacy or law.  
Use it only on systems you own and control.

<hr />

<h2>✨ Features</h2>

- Logs character keys and special keys
- Includes timestamps for every entry
- Configurable log file path via `config.ini`
- Simple file rotation to prevent unbounded growth
- ESC key cleanly stops the logger
- Minimal, readable code for educational purposes

<hr />

<h2>📦 Installation (from source)</h2>

<h3>1. Clone the repository</h3>
<pre><code>git clone https://github.com/zappybird/Keylogger.git
cd Keylogger
</code></pre>

<h3>2. Create a virtual environment</h3>
<pre><code>python -m venv .venv
</code></pre>

<h3>3. Activate it (Windows)</h3>
<pre><code>.venv\Scripts\activate
</code></pre>

<h3>4. Install dependencies</h3>
<pre><code>pip install -r requirements.txt
</code></pre>

<h3>5. Run the keylogger</h3>
<pre><code>python main.py
</code></pre>

<p>The console will display:</p>
<pre><code>Keylogger started. Press ESC to stop.
</code></pre>

<hr />

<h2>⚙️ Configuration</h2>

The log file path is defined in <code>config.ini</code>:

<pre><code>[DEFAULT]
keylog_file = keyfile.txt
</code></pre>

You may change this to any writable path.

<hr />

<h2>🧪 Running Tests</h2>

This project includes basic unit tests for logging behavior.

Run them with:

<pre><code>python -m unittest
</code></pre>

<hr />

<h2>🔒 Legal & Ethical Notice</h2>

This project is provided for **educational and defensive purposes only**.  
You must **never** use it to monitor another person’s device, activity, or keystrokes.

Unauthorized keylogging is illegal in many jurisdictions.

Use responsibly and ethically.

<hr />

<h2>📄 License</h2>

MIT License (optional)
