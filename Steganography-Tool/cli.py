import argparse
from encoder import encode_message  # Placeholder import; implement encoder.py first.
from decoder import decode_message  # Placeholder import; implement decoder.py first.

# TODO: Add imports for encoder.py and decoder.py once they are implemented.
# The CLI currently parses arguments but never calls any business logic.
# These imports are what connect the user interface to the rest of the project.

# TODO: Add imports for exceptions.py (CapacityError, DecryptionError, StegoError).
# The CLI is the correct layer to catch these exceptions and print friendly error messages.
# Business logic modules should raise; the CLI should catch and report.

def main():
    """Parse command-line arguments and run encode/decode."""
    parser = argparse.ArgumentParser(description="Steganography Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    # Encode subcommand
    encode_parser = subparsers.add_parser("encode", help="Encode a message into an image")
    encode_parser.add_argument("input_image", help="Path to the input image")
    encode_parser.add_argument("output_image", help="Path to save the output image")
    encode_parser.add_argument("message", help="Message to hide in the image")
    # TODO: Add an optional --password argument to the encode subparser.
    # The README lists password protection as a feature, but the CLI cannot accept one.
    # Use add_argument("--password", default=None, help="...") for an optional flag.
    # Learn about optional argparse arguments (see recommended resources from earlier analysis).

    # Decode subcommand
    decode_parser = subparsers.add_parser("decode", help="Decode a message from an image")
    decode_parser.add_argument("input_image", help="Path to the image to decode")
    # TODO: Add an optional --password argument to the decode subparser as well.
    # Without it, encoded-with-password images cannot be decoded through the CLI.

    args = parser.parse_args()

    # TODO: Add dispatch logic — after parsing args, check args.command and call
    # either encoder.encode_message() or decoder.decode_message() accordingly.
    # `args` is populated but completely unused right now. This is the core missing wiring.

    # TODO: Wrap the dispatch calls in try/except blocks for CapacityError,
    # DecryptionError, IOError, and StegoError. Print a human-readable message
    # for each. Never let a raw traceback reach the end user of a CLI tool.

    # TODO: Add a success message after encoding (e.g., "Message hidden in output.png")
    # and print the decoded message to stdout after decoding.
    # A CLI tool should always give the user visible confirmation of what happened.

if __name__ == "__main__":
    main()
    
    # TODO: Remove this `pass` — it is outside the main() function body and serves no purpose.
    # It is also outside the if __name__ block in terms of logical intent. Delete it.
    pass