<h1>Hashing Utility (Educational Cybersecurity Demo)</h1>

<p>
This project is a clear, minimal hashing demonstration intended 
<strong>solely for personal cybersecurity learning, debugging, and defensive research</strong>.  
It shows how common hashing algorithms work, how to generate digests, and how to verify a guess against a known hash (optionally with a salt).
</p>

<p>
This tool is <strong>not</strong> designed for password cracking, unauthorized access, or any activity that violates privacy or law.  
Use it only on systems and data you own and control.
</p>

<hr />

<h2>Features</h2>

<ul>
  <li>Simple functions for <strong>MD5</strong>, <strong>SHA‑1</strong>, and <strong>SHA‑256</strong> hashing</li>
  <li>Clean string‑to‑hash workflow using Python’s built‑in <code>hashlib</code></li>
  <li>Optional <strong>salt</strong> support for hash verification</li>
  <li>Unified <code>verify_hash()</code> helper for comparing guesses to known digests</li>
  <li>Readable, minimal code suitable for teaching and experimentation</li>
  <li>Example usage included at the bottom of the script</li>
</ul>

<hr />

<h2>Project Structure</h2>

<pre><code>
HashingDemo/
│
├── hashing.py            # Core hashing functions and verification logic
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
</code></pre>

<hr />

<h2>How It Works</h2>

<p>
This hashing utility focuses on <strong>clarity and educational value</strong>.  
Below is the high‑level flow:
</p>

<h3>1. Hashing Functions</h3>
<p>
Each hashing function (<code>hash_md5</code>, <code>hash_sha1</code>, <code>hash_sha256</code>) follows the same pattern:
</p>

<ul>
  <li>Convert the input string to bytes</li>
  <li>Create a hash object using <code>hashlib</code></li>
  <li>Return the digest in hexadecimal form</li>
</ul>

<p>Example output:</p>

<pre><code>MD5 hash of 'yo momma' is: 3d6f0a5b...</code></pre>

<h3>2. Hash Verification</h3>

<p>
The <code>verify_hash()</code> function checks whether a guessed string matches a known hash.
It:
</p>

<ul>
  <li>Appends an optional salt</li>
  <li>Selects the correct hashing algorithm</li>
  <li>Computes the digest</li>
  <li>Compares it to the target hash</li>
</ul>

<p>
This mirrors how authentication systems validate passwords without storing them in plaintext.
</p>

<h3>3. Demonstration Block</h3>

<p>
At the bottom of the script, a small loop:
</p>

<ul>
  <li>Hashes the string <code>"yo momma"</code> using all three algorithms</li>
  <li>Prints each digest</li>
  <li>Verifies each hash using <code>verify_hash()</code></li>
</ul>

<p>This provides a quick, self‑contained demonstration of the full workflow.</p>

<hr />

<h2>Installation (from source)</h2>

<h3>1. Clone the repository</h3>
<pre><code>git clone https://github.com/yourusername/HashingDemo.git
cd HashingDemo
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

<h3>5. Run the demo</h3>
<pre><code>python hashing.py
</code></pre>

<p>The console will display something like:</p>

<pre><code>MD5 hash of 'yo momma' is: ...
Verification result for MD5: True
</code></pre>

<hr />

<h2>Usage</h2>

<p>You can import the hashing functions into your own scripts:</p>

<pre><code>from hashing import hash_sha256, verify_hash

digest = hash_sha256("hello world")
print(digest)

is_valid = verify_hash("hello world", digest, "sha256")
print(is_valid)
</code></pre>

<p>Salted verification is also supported:</p>

<pre><code>verify_hash("mypassword", stored_hash, "sha1", salt="1234")
</code></pre>

<hr />

<h2>Running Tests</h2>

<p>If you add tests, run them with:</p>

<pre><code>python -m unittest
</code></pre>

<hr />

<h2>Legal & Ethical Notice</h2>

<p>
This project is provided for <strong>educational and defensive purposes only</strong>.  
You must <strong>never</strong> use hashing tools to attack systems, crack credentials, or access data you do not own.
</p>

<p>
Unauthorized access and password cracking are illegal in many jurisdictions.  
Use responsibly and ethically.
</p>

<hr />
