# Keylogger (Educational Cybersecurity Demo)

This project is a transparent, non‑stealth keylogging demonstration intended **solely for personal cybersecurity learning, debugging, and defensive research**.  
It records keyboard input, groups characters into words, and logs each word with a single timestamp.  
All logs are stored locally in a file defined in `config.ini`.

This tool is **not** designed for covert use, monitoring others, or any activity that violates privacy or law.  
Use it only on systems you own and control.

<hr />

<h2> Features</h2>

- Groups typed characters into full words
- Adds a **single timestamp per word**
- Starts a new word when:
  - A space is pressed  
  - Typing pauses for more than 1 second  
- Configurable log file path via `config.ini`
- Simple file rotation to prevent unbounded growth
- ESC key cleanly stops the logger and flushes the final word
- Minimal, readable code for educational and defensive research

<hr />

<h2>📁 Project Structure</h2>

<pre><code>
Keylogger/
│
├── main.py               # Entry point; starts listener and handles ESC shutdown
├── logger.py             # Core logging logic (word grouping, timestamps, rotation)
├── config.py             # Loads configuration from config.ini
├── config.ini            # Defines log file path
│
├── tests/
│   └── test_logger.py    # Basic unit tests for logging behavior
│
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
</code></pre>

<hr />

<h2> How It Works</h2>

This keylogger focuses on **clarity and educational value**, not stealth.  
Here’s the high‑level flow:

<h3>1. Keyboard Listener</h3>
A `pynput` listener captures every key press and forwards it to `key_pressed()`.

<h3>2. Word Buffering</h3>
Characters are appended to an in‑memory buffer (`current_word`).  
A word ends when:

- The user presses **space**, or  
- More than **1 second** passes between key presses  

This creates clean, readable word‑level logs.

<h3>3. Timestamping</h3>
When a word is complete, it is written to the log file with a **single timestamp**, e.g.:

<pre><code>2026-02-06 21:04:39 - monkey</code></pre>

<h3>4. File Rotation</h3>
If the log file exceeds 1MB, it is automatically rotated to prevent unbounded growth.

<h3>5. Clean Shutdown</h3>
Pressing **ESC**:

- Flushes any word still in the buffer  
- Stops the listener  
- Exits the program cleanly  

<hr />

<h2> Installation (from source)</h2>

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

<h2> Configuration</h2>

The log file path is defined in <code>config.ini</code>:

<pre><code>[DEFAULT]
keylog_file = keyfile.txt
</code></pre>

You may change this to any writable path.  
The logger will automatically rotate the file once it exceeds 1MB.

<hr />

<h2> Running Tests</h2>

This project includes basic unit tests for logging behavior and word grouping.

Run them with:

<pre><code>python -m unittest
</code></pre>

<hr />

<h2> Legal & Ethical Notice</h2>

This project is provided for **educational and defensive purposes only**.  
You must **never** use it to monitor another person’s device, activity, or keystrokes.

Unauthorized keylogging is illegal in many jurisdictions.

Use responsibly and ethically.

<hr />
