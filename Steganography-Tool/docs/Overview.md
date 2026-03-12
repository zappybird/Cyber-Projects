# Technical Overview

This document explains the core concepts behind LSB steganography and the image-processing
principles required to understand how this project works internally.

---

## Pixels and RGB

Digital images are composed of pixels arranged in a grid. Each pixel contains color information
represented by three channels: **Red**, **Green**, and **Blue**. Each channel is stored as an integer
between 0 and 255. Together, these values determine the final color of the pixel.

---

## Binary, Bits, and Bytes

Computers store all data as binary—sequences of 0s and 1s.  
A single binary digit is a **bit**, and eight bits form a **byte**.

Text must be converted into bytes, and then into individual bits, before it can be embedded into an image.

---

## Least Significant Bit (LSB)

The Least Significant Bit is the rightmost bit in a binary number.  
Changing this bit alters the numeric value by only 1, which is visually imperceptible in an RGB color channel.

This makes the LSB ideal for hiding data inside images without noticeably altering them.

---

## Lossless vs. Lossy Image Formats

Lossless formats such as **PNG** and **BMP** preserve pixel data exactly, making them suitable for
steganography.

Lossy formats like **JPEG** apply compression that modifies pixel values, which destroys any hidden data.

For this reason, JPEG images should never be used for LSB embedding.
