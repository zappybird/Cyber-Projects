# TODO: Decide on an encryption strategy before implementing either function.
# Option A (educational/simple): XOR cipher — easy to understand but NOT secure.
#   If you use this, add a prominent warning in the docstring and README.
# Option B (secure): Use Python's `cryptography` library with Fernet + PBKDF2 key derivation.
# The choice affects what both functions accept and return.
# Learn about symmetric encryption and why raw passwords must be key-derived
# (see recommended resources from earlier analysis).

# TODO: Add `cryptography` (or chosen library) to requirements.txt once you decide.
# requirements.txt is currently empty — this is a missing dependency declaration.

def encrypt_message(message, password=None):
    # TODO: Clarify in the docstring: what type does `message` come in as?
    # (str? bytes?) And what type does this function return? (str? bytes?)
    # encoder.py depends on the return type to correctly convert to bits.

    # TODO: Remove the `password=None` default if you decide the caller should never
    # invoke this function without a password. Handling None here creates two code paths
    # and masks bugs where password is accidentally omitted.

    # TODO: If using Fernet: derive a proper key from `password` using PBKDF2 or scrypt.
    # Never use a raw password string directly as a cryptographic key.
    # Learn about key derivation functions (see recommended resources from earlier analysis).
    """Encrypt the message if a password is provided."""
    pass

def decrypt_message(data, password=None):
    # TODO: Match the type contract of encrypt_message exactly — same input/output types
    # in reverse. If encrypt returns bytes, this must accept bytes.

    # TODO: Wrap decryption in a try/except and raise DecryptionError from exceptions.py
    # on failure. The caller (decoder.py) should receive DecryptionError, not a raw
    # library exception the user cannot understand.

    # TODO: Same password=None consideration as encrypt_message applies here.
    """Decrypt the message if a password is provided."""
    pass