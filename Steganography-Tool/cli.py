import argparse


def main():
    """Parse command-line arguments and run encode/decode."""
    parser = argparse.ArgumentParser(description="Steganography Tool")
    subparsers = parser.add_subparsers(dest="command", required=True)
    # Encode subcommand
    encode_parser = subparsers.add_parser("encode", help="Encode a message into an image")
    encode_parser.add_argument("input_image", help="Path to the input image")
    encode_parser.add_argument("output_image", help="Path to save the output image")
    encode_parser.add_argument("message", help="Message to hide in the image")
    # Decode subcommand
    decode_parser = subparsers.add_parser("decode", help="Decode a message from an image")
    decode_parser.add_argument("input_image", help="Path to the image to decode")
    args = parser.parse_args()

if __name__ == "__main__":
    main()
    
    pass
