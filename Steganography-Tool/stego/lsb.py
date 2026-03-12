
# TODO: Add type annotations to both function signatures before implementing.
# Decide now: is `bitstream` a str of "0"/"1" chars, a list[int], or bytes?
# Whatever you choose, apply it consistently across lsb.py, encoder.py, and decoder.py.
# Ambiguous types here will cause silent integration bugs when the pipeline is wired together.
# Learn about Python type annotations (see recommended resources from earlier analysis).

def embed_bits(image, bitstream):
    # TODO: Document the expected type of `bitstream` in the docstring.
    # The contract between encoder.py and lsb.py depends entirely on this type being consistent.

    # TODO: Add a bounds check — raise CapacityError from exceptions.py if len(bitstream)
    # exceeds the image's capacity. Import and use calculate_capacity() from capacity.py.
    # Without this check, embedding silently fails or corrupts the image.

    # TODO: Define and document the pixel traversal order (e.g., left-to-right, top-to-bottom,
    # R then G then B per pixel). This order MUST match extract_bits exactly, or decoding
    # will return garbage. This is a design decision — make it explicit.

    # TODO: Implement the LSB replacement logic: for each bit in bitstream, clear the LSB
    # of the current channel value and set it to the bit.
    # Learn about bitwise AND (&) and OR (|) operators for LSB manipulation
    # (see recommended resources from earlier analysis).
    """Embed a string of bits into the image's least significant bits."""
    pass

def extract_bits(image, num_bits):
    # TODO: Document the return type in the docstring — must match what embed_bits accepts.

    # TODO: Use the exact same pixel traversal order as embed_bits.
    # If the order differs by even one pixel, all extracted bits will be wrong.

    # TODO: Add a bounds check — raise an appropriate error if num_bits exceeds
    # the total available bits in the image. Prevents reading past image boundaries.

    # TODO: Implement LSB extraction: for each channel, extract its LSB using bitwise AND with 1.
    # Learn about bitwise operations for LSB extraction
    # (see recommended resources from earlier analysis).
    """Extract num_bits from the image's least significant bits."""
    pass