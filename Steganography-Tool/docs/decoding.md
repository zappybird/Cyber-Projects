# Encoding and Decoding Pipeline

This document describes how messages are embedded into and extracted from images using the LSB
technique.

---

## Message Encoding

1. Convert the input text into bytes.
2. Convert each byte into an 8-bit binary string.
3. Store the message length in the first 32 bits.
4. Embed each bit into the LSB of the image's pixel channels.
5. Save the modified image as a PNG or BMP.

---

## Message Decoding

1. Read the first 32 LSBs to determine message length.
2. Extract the required number of bits from the image.
3. Group bits into bytes and convert them back into text.
4. Decrypt the message if a password was used.

---

## Capacity Calculation

Each pixel provides 3 bits of storage (one per RGB channel).  
The total capacity is: capacity_bits = width × height × 3

The message must fit within this limit, including the 32-bit length prefix.

---

## Encryption (Optional)

If a password is provided, the message is encrypted before embedding.  
This ensures that even if someone extracts the hidden bits, they cannot read the message without the correct password.
