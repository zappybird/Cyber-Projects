from PIL import Image

"""
To load and save images using the Pillow library in Python, you use the Image.open() function and the Image.save() method, respectively. 
"""

def load_image(image_path, convert_to_rgb=True):
    """Load an image from the specified path."""
    try:
        img = Image.open(image_path)
        return img.convert('RGB') if convert_to_rgb else img
    except Exception as e:
        raise IOError(f"Error loading image: {e}")
    
def get_pixel(img, x, y):
    """Get the RGB values of a pixel at (x, y)."""
    return img.load()[x,y]

def set_pixel(img, x, y, value):
    """Set the RGB values of a pixel at (x, y)."""
    img.load()[x,y] = value

img = load_image("path/to/image.png")
print("Width:", img.width)
print("Height:", img.height)
print("Mode:", img.mode)
img.save("test_output.png")

print("Before:", get_pixel(img, 50, 50))
set_pixel(img, 50, 50, (255, 0, 0))  # Set pixel to red
print("After:", get_pixel(img, 50, 50))
