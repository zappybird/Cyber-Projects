# LSB Steganography Tool

An educational Python tool for hiding secret messages inside images using the **Least Significant Bit (LSB)** technique. Built to demonstrate core concepts in cybersecurity, image processing, and Python software architecture.

---

## What Is Steganography?

Think about cryptography for a second — encrypting a message in plain sight. Even if everyone knows the message has been sent, they can't figure out what it means.

Steganography is a step further. We're not just scrambling the message — we're **hiding the fact that it's even there in the first place.**

Like writing a message with invisible ink. Only the person receiving it would know to look. Anyone else reading it might find it interesting, but only the recipient can read the secret message hidden inside.

---

## How LSB Works

The most simple form of steganography is **LSB — Least Significant Bit**.

It refers to the rightmost bit in a binary number. It holds the lowest value, so it's the bit with the least amount of weight. That means we can change it to contain our encoded message and have a near imperceptible change on the actual image — visually, nothing looks different.

We change the last bit (or last two bits) of every byte in the image. Every byte has 8 bits — so if we change the last two, the remaining six still come from the legitimate image. Those two changed bits carry our secret message.

**Example:** The color value `11001010` becomes `11001011` after embedding one bit. The color shifts by 1 out of 255 — completely invisible to the human eye.

> **Why PNG and BMP only?** Formats like JPEG use lossy compression, which modifies pixel values during saving and destroys any hidden data. PNG and BMP are lossless — what you write is exactly what gets saved.

---

## Features

- Hide a text message inside a PNG or BMP image
- Extract a hidden message from an encoded image
- Optional password-based encryption before embedding
- Capacity validation — warns if the message is too large for the image
- Clean command-line interface

---

## Project Status

This project is currently **in active development**. The architecture and module structure are complete. Core logic (LSB embedding, encoding/decoding pipeline, encryption) is being implemented.

| Module | Status |
|---|---|
| `image_utils.py` | ✅ Complete |
| `capacity.py` | ✅ Complete |
| `exceptions.py` | ✅ Complete |
| `lsb.py` | 🔧 In progress |
| `encoder.py` | 🔧 In progress |
| `decoder.py` | 🔧 In progress |
| `crypto.py` | 🔧 In progress |
| `cli.py` | 🔧 In progress |

---

## Installation

**Requirements:** Python 3.8+

1. Clone the repository:
```bash
git clone https://github.com/your-username/lsb-steganography.git
cd lsb-steganography
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify Pillow is installed:
```bash
python -c "from PIL import Image; print('Pillow installed successfully')"
```

---

## Usage

> **Note:** CLI commands below reflect the intended interface. Full dispatch is being wired in.

### Encode a message into an image
```bash
python cli.py encode input.png output.png "Your secret message"
```

### Encode with password protection
```bash
python cli.py encode input.png output.png "Your secret message" --password mypassword
```

### Decode a message from an image
```bash
python cli.py decode output.png
```

### Decode a password-protected message
```bash
python cli.py decode output.png --password mypassword
```

**Arguments:**

| Argument | Description |
|---|---|
| `input.png` | Path to the original image (PNG or BMP) |
| `output.png` | Path to save the encoded image |
| `"message"` | The text to hide |
| `--password` | Optional. Encrypts the message before embedding |

---

## Project Structure

```
lsb-steganography/
│
├── cli.py           # Command-line interface — parses args, dispatches to encoder/decoder
├── encoder.py       # Encoding pipeline — converts message to bits and embeds into image
├── decoder.py       # Decoding pipeline — extracts bits from image and reconstructs message
├── lsb.py           # Core LSB logic — bit embedding and extraction at the pixel level
├── crypto.py        # Optional encryption/decryption using a password
├── capacity.py      # Calculates whether a message fits within a given image
├── image_utils.py   # Image I/O utilities using Pillow (load, get/set pixel, save)
├── exceptions.py    # Custom exception hierarchy (StegoError, CapacityError, DecryptionError)
└── requirements.txt # Project dependencies
```

### How the modules connect

```
cli.py
  └── encoder.py / decoder.py      ← orchestrates the pipeline
        ├── capacity.py             ← validates message fits before embedding
        ├── crypto.py               ← encrypts/decrypts if password provided
        ├── lsb.py                  ← reads/writes bits at the pixel level
        └── image_utils.py          ← loads and saves images via Pillow
```

---

## How the Pipeline Works Internally

**Encoding:**
1. Convert the message string to bytes (`UTF-8`)
2. Optionally encrypt the bytes using the provided password
3. Convert bytes to a flat stream of bits
4. Prepend a 32-bit header encoding the message length
5. Iterate pixels left-to-right, top-to-bottom, writing one bit per channel (R, G, B)
6. Save the modified image as PNG or BMP

**Decoding:**
1. Read the first 32 bits from the image to determine message length
2. Extract that many bits from the subsequent pixels
3. Reassemble bits into bytes, then decode back to a string
4. Optionally decrypt using the provided password

**Capacity formula:**
```
max_bits  = width × height × 3
required  = 32 + (message_length_in_bytes × 8)
```

---

## Contributing

This is an educational project and contributions are welcome. If you'd like to help:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes with clear, commented code
4. Open a pull request with a description of what you changed and why

When contributing, please keep the educational intent in mind — clarity and readability are prioritized over cleverness.

---

## Learning Resources

If you're exploring this project to learn, these resources cover the core concepts:

- [Pillow documentation](https://pillow.readthedocs.io/en/stable/) — image processing in Python
- [Python bitwise operators](https://realpython.com/python-bitwise-operators/) — essential for LSB manipulation
- [Unicode and UTF-8 explained](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/) — why encoding matters
- [Python argparse tutorial](https://docs.python.org/3/howto/argparse.html) — building CLIs
- [Python custom exceptions](https://realpython.com/python-exceptions/) — clean error handling

---

## License

MIT License. See `LICENSE` for details.
