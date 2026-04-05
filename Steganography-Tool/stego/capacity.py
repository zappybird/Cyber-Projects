class CapacityError(Exception):
    pass

def calculate_capacity(image):
    """Calculate the maximum number of bits that can be hidden in the image."""
    width, height = image.size
    # Assuming we are using 1 bit per color channel (R, G, B)
    return width * height * 3  # 3 channels (R, G, B)

def required_capacity(message_bytes):
    """Calculate the number of bits required to hide the message.
    
    Args:
        message_bytes (bytes): The message as a bytes object.
    
    Returns:
        int: The number of bits required.
    """
    if not isinstance(message_bytes, bytes):
        raise TypeError("message_bytes must be a bytes object")
    return 32 + len(message_bytes) * 8  # Each byte is 8 bits

def check_fits(image, message_bytes):
    capacity = calculate_capacity(image)
    required = required_capacity(message_bytes)
    if required > capacity:
        raise CapacityError(f"Message requires {required} bits, but image only has {capacity} bits")


if __name__ == "__main__":
    from image_utils import load_image

    img = load_image("path/to/image.png")
    capacity = calculate_capacity(img)
    print(f"Image Capacity: {capacity} bits")
    
    message = "Hello, World!"
    message_bytes = message.encode('utf-8')
    try:
        check_fits(img, message_bytes)
        print("The message can be hidden in the image.")
    except CapacityError as e:
        print(f"Warning: {e}")