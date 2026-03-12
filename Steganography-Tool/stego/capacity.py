def calculate_capacity(image):
    """Calculate the maximum number of bits that can be hidden in the image."""
    width, height = image.size
    # Assuming we are using 1 bit per color channel (R, G, B)
    return width * height * 3  # 3 channels (R, G, B)

def required_capacity(message_bytes):
    # TODO: Enforce in the docstring (and optionally with an assertion) that `message_bytes`
    # must be a bytes object, not a str. len("café") == 4 but len("café".encode('utf-8')) == 5.
    # Passing a raw string silently produces wrong capacity calculations for non-ASCII input.
    # Learn about UTF-8 multi-byte characters and why bytes length != string length
    # (see recommended resources from earlier analysis).
    """Calculate the number of bits required to hide the message."""
    return 32 + len(message_bytes) * 8  # Each byte is 8 bits

# TODO: Consider adding a check_fits(image, message_bytes) convenience function here
# that combines calculate_capacity and required_capacity and raises CapacityError
# from exceptions.py if the message is too large. This would give encoder.py a single
# clean call instead of repeating the comparison logic.

if __name__ == "__main__":
    from image_utils import load_image
    
    # TODO: Replace "path/to/image.png" with a real test image path, or add a comment
    # that this block requires substitution before running. As written, it always crashes.
    img = load_image("path/to/image.png")
    capacity = calculate_capacity(img)
    print(f"Image Capacity: {capacity} bits")
    
    message = "Hello, World!"
    message_bytes = message.encode('utf-8')
    required_bits = required_capacity(message_bytes)
    print(f"Required Capacity for message: {required_bits} bits")
    
    if required_bits > capacity:
        print("Warning: The message is too large to fit in the image!")
    else:
        print("The message can be hidden in the image.")