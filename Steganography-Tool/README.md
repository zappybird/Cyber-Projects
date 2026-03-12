<h2>Project Overview</h2>

<p>
This project is an educational steganography tool that demonstrates how secret messages can be
hidden inside digital images using the Least Significant Bit (LSB) technique. Steganography is the
practice of concealing information within other seemingly harmless data—in this case, embedding
binary message data inside the pixel values of an image. LSB steganography works by modifying only
the lowest-value bit of each color channel (R, G, B), which results in changes so small that they
are visually undetectable to the human eye.
</p>

<hr />

<h2>Features</h2>

<ul>
  <li><strong>Encode:</strong> Hide a text message inside a PNG or BMP image.</li>
  <li><strong>Decode:</strong> Extract a hidden message from a steganographic image.</li>
  <li><strong>Password Protection:</strong> Optionally encrypt the message before embedding.</li>
  <li><strong>PNG/BMP Support:</strong> Uses lossless formats to preserve hidden data.</li>
  <li><strong>Command-Line Interface:</strong> Clean CLI for encoding and decoding operations.</li>
</ul>

<hr />

<h2>Image Processing with Pillow</h2>

<p>
This project demonstrates how to perform basic image processing in Python using the Pillow library.
By loading, inspecting, modifying, and saving images through a set of simple utility functions,
this serves as a practical foundation for understanding pixel manipulation and image I/O in Python.
</p>

<hr />

<h2>Objective</h2>

<ul>
  <li>Install and import the Pillow imaging library.</li>
  <li>Load an image from a file path and convert it to RGB.</li>
  <li>Inspect image properties such as width, height, and mode.</li>
  <li>Read and write individual pixel values.</li>
  <li>Save a modified copy of the image to disk.</li>
</ul>

<hr />

<h2>Installing Pillow</h2>

<h3>1. Install via pip</h3>
<pre><code>pip install Pillow
</code></pre>

<h3>2. Verify installation</h3>
<pre><code>python -c "from PIL import Image; print('Pillow installed successfully')"
</code></pre>

<hr />

<h2>Importing the Library</h2>

<pre><code>from PIL import Image
</code></pre>

<p>Pillow exposes its functionality through the <code>PIL</code> namespace. The <code>Image</code> module is the core component used for opening, manipulating, and saving images.</p>

<hr />

<h2>Functions</h2>

<h3>load_image(image_path, convert_to_rgb=True)</h3>
<p>Loads an image from the specified file path. Optionally converts it to RGB mode, which is enabled by default. Raises an <code>IOError</code> if the image cannot be loaded.</p>

<pre><code>def load_image(image_path, convert_to_rgb=True):
    try:
        img = Image.open(image_path)
        return img.convert('RGB') if convert_to_rgb else img
    except Exception as e:
        raise IOError(f"Error loading image: {e}")
</code></pre>

<h3>get_pixel(img, x, y)</h3>
<p>Returns the RGB tuple of a pixel at coordinates <code>(x, y)</code> within the image.</p>

<pre><code>def get_pixel(img, x, y):
    return img.load()[x, y]
</code></pre>

<h3>set_pixel(img, x, y, value)</h3>
<p>Sets the pixel at coordinates <code>(x, y)</code> to the specified RGB value.</p>

<pre><code>def set_pixel(img, x, y, value):
    img.load()[x, y] = value
</code></pre>

<hr />

<h2>Usage</h2>

<pre><code>img = load_image("path/to/image.png")

print("Width:", img.width)
print("Height:", img.height)
print("Mode:", img.mode)

img.save("test_output.png")

print("Before:", get_pixel(img, 50, 50))
set_pixel(img, 50, 50, (255, 0, 0))
print("After:", get_pixel(img, 50, 50))
</code></pre>

<p><strong>Parameter breakdown:</strong></p>
<ul>
  <li><strong>img.width</strong>: Pixel width of the loaded image</li>
  <li><strong>img.height</strong>: Pixel height of the loaded image</li>
  <li><strong>img.mode</strong>: Color mode of the image (e.g. <code>RGB</code>)</li>
  <li><strong>test_output.png</strong>: Output filename the modified image is saved as</li>
</ul>

<p><strong>Note:</strong> <code>set_pixel</code> modifies the image in memory. Call <code>img.save()</code> afterward to persist any pixel changes to disk.</p>