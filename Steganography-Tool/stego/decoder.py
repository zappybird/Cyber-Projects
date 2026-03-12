# TODO: Add imports for lsb.py, crypto.py, and exceptions.py.
# decode_message is the pipeline orchestrator for extraction — it needs all three.

def decode_message(image, password=None):
    # TODO: Add type annotations to the signature.
    # `image` should be the same type as in encoder.py — decide and be consistent.

    # TODO: Add step 1 — extract the first 32 bits using lsb.extract_bits(image, 32).
    # These bits encode the message length. Without this step the decoder cannot proceed.
    # See decoding.md for the full pipeline specification.

    # TODO: Add step 2 — convert those 32 bits to an integer to get message_length.
    # Learn about int.from_bytes() for reconstructing integers from binary data
    # (see recommended resources from earlier analysis).

    # TODO: Add a guard: if message_length is 0 or larger than image capacity, the image
    # was likely never encoded. Raise a meaningful StegoError instead of crashing
    # or returning garbage. This is the "no hidden message" edge case.

    # TODO: Add step 3 — extract message_length * 8 bits using lsb.extract_bits().

    # TODO: Add step 4 — convert extracted bits back to bytes, then decode to a string.
    # Learn about bytes.decode() for reconstructing text from bytes
    # (see recommended resources from earlier analysis).

    # TODO: Add step 5 — if password is not None, call crypto.decrypt_message().
    # Wrap this call in a try/except and raise DecryptionError from exceptions.py
    # if decryption fails (e.g., wrong password). Never let a raw crypto exception
    # bubble up to the user.
    """Extract bits from the image and reconstruct the message."""
    pass