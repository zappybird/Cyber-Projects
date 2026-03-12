
# TODO: No major issues found in earlier analysis.
# However, consider whether a FormatError subclass is needed for when a user
# provides a JPEG output path — this is a distinct failure mode from CapacityError
# and DecryptionError, and would benefit from its own exception type.
# Also consider an ExtractionError for when decode_message reads an image with no
# hidden data (the 32-bit header is zero or nonsensical).

class StegoError(Exception):
    """Base class for steganography-related errors."""
    pass


class CapacityError(StegoError):
    """Raised when the message does not fit inside the image."""
    pass


class DecryptionError(StegoError):
    """Raised when password decryption fails."""
    pass