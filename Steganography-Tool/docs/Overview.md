# Technical Overview

This document explains the core concepts behind LSB steganography and the image-processing
principles required to understand how this project works internally.

If you're new to this topic, read this first — everything in `encoding_and_decoding.md`
and `cli_and_usage_details.md` builds on what's covered here.

---

## Steganography vs. Cryptography

These are two different approaches to protecting a secret, and understanding the distinction
matters before diving into how this project works.

**Cryptography** encrypts a message so that even if everyone knows a message was sent,
they can't figure out what it means. The existence of the message is visible — only its
contents are hidden.

**Steganography** goes a step further. We're not just scrambling the message — we're
**hiding the fact that it's even there in the first place.**

Think of it like writing with invisible ink. Only the person receiving it knows to look.
Anyone else seeing the carrier (an image, a document, an audio file) has no reason to
suspect it contains anything at all.

This project uses **digital image steganography** — specifically, the LSB technique applied
to PNG and BMP image files.

> For maximum security, this project supports combining both approaches: hiding a message
> using steganography *and* encrypting it with a password before embedding. See
> `encoding_and_decoding.md` for how these two layers interact.

---

## Pixels and RGB

Digital images are composed of pixels arranged in a rectangular grid. Each pixel holds
color information represented by three channels: **Red**, **Green**, and **Blue** (RGB).
Each channel is stored as an integer between 0 and 255. Together, those three values
determine the exact color of that pixel.

A pixel with values `(255, 0, 0)` is pure red. `(0, 0, 0)` is black. `(255, 255, 255)` is white.

---

## Binary, Bits, and Bytes

Computers store all data — text, images, everything — as binary: sequences of 0s and 1s.

- A single binary digit is a **bit**
- Eight bits form a **byte**
- One byte can represent 256 different values (0–255)

Before a text message can be embedded into an image, it must be converted to a flat
stream of bits:
```
"A"  →  ASCII 65  →  01000001
"Hi" →  "H" (72) + "i" (105)
     →  01001000  01101001
```

That flat stream of bits is what gets written into image pixels, one bit at a time.

---

## The Least Significant Bit (LSB)

In any binary number, the **least significant bit** is the rightmost bit. It carries the
lowest value — flipping it changes the number by at most 1.
```
11001010  =  202
11001011  =  203  ← only the LSB changed; value shifted by 1
```

In an RGB channel where values range from 0–255, a change of 1 is completely invisible to
the human eye. This is the core property that makes LSB steganography possible — we can
overwrite the rightmost bit of each color channel to carry our hidden data, and the image
looks identical to the original.

---

## Bitmap Images and Color Depth

A **bitmap** is a rectangular grid of pixels. Bitmaps are defined by two parameters:
the **number of pixels** (dimensions) and the **color depth** (how much information each
pixel stores).

### 1-bit (Black & White)

The smallest possible color depth. Each pixel is stored in a single bit:
- `0` = black
- `1` = white

No shades in between — purely monochrome.

### 8-bit Grayscale

Each pixel uses 1 byte (8 bits), giving 256 possible shades of gray.
- `0` = black  
- `127` = 50% gray  
- `255` = white

### 24-bit RGB

The standard for full-color images. Each pixel uses 3 bytes — one per channel (R, G, B).

- Each channel: `0` (no contribution) → `255` (fully saturated)
- Total possible colors: 256 × 256 × 256 = **16,777,216**

![24-bit RGB channel breakdown](./images/rgb_24bit_components.png)

RGB color space can also be visualized as a cube:

![RGB color cube](./images/rgb_color_cube.png)

### 16-bit RGB

Uses 5 bits per color channel with a 1-bit alpha channel.

![16-bit RGB bit layout](./images/rgb_16bit_layout.png)

### 32-bit RGBA

Same as 24-bit RGB, with an extra 8-bit **alpha channel**.

![32-bit RGBA channel layout](./images/rgb_32bit_alpha_channel.png)

> **Note:** Images are loaded and processed in **RGB mode** (24-bit, no alpha).  
> Any alpha channel present in the source file is discarded on load.

---

## How BMP Stores Pixel Data

Understanding BMP's internal structure helps explain why it's compatible with steganography
and how this project interacts with pixel memory.

**BMP file structure (simplified):**
1. File header  
2. DIB header  
3. Optional color table  
4. **Pixel array**

**Pixel array details:**
- Stored as **BGR** (Blue, Green, Red)  
- Often stored **bottom-up**  
- Each channel is 8 bits  

A single 24-bit pixel broken down to its bits:
```
Blue:  b7 b6 b5 b4 b3 b2 b1 [b0]
Green: g7 g6 g5 g4 g3 g2 g1 [g0]
Red:   r7 r6 r5 r4 r3 r2 r1 [r0]
```

The bracketed bits (`b0`, `g0`, `r0`) are the LSBs — the three bits per pixel that carry
our hidden message.

---

## Lossless vs. Lossy Image Formats

### ✅ PNG — Recommended  
### ✅ BMP — Also supported  
### ❌ JPEG — Never use this

JPEG destroys LSBs during compression, corrupting hidden data.

> **Core rule:** BMP and PNG preserve your exact pixel bits. JPEG does not.

---

## Resolution

Resolution determines the physical size of a bitmap. Pixels themselves have no size — resolution
defines how many pixels fit into a physical inch.

![Resolution PPI comparison](./images/resolution_ppi_diagram.png)

Resolution does **not** affect steganographic capacity or hidden data.
