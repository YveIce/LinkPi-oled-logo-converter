"""
MIT License

Copyright (c) 2024 YveIce

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import os
# Check if the lib pillow is installed, as we need it to read and write jiff-graphics
try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Lib PIL is missing! Try to install it using:\n\tpip install pillow")
    sys.exit(1)

# About the used image format:
# The binary format encodes a monochrome image with 1-bit pixels. Pixels are 
# arranged in a fixed-width (128 pixels) and fixed-height (64 pixels) grid. 
# The bytes represent 8 consecutive pixels, ordered left-to-right and 
# top-to-bottom. Within each byte, the bits correspond to pixels in a 
# left-to-right sequence. Visualization follows a top-to-bottom and 
# left-to-right order.

def bin_to_gif(input_file, output_file):
    with open(input_file, 'rb') as file:
        bytes_data = file.read()

    # Create a new image with the fixed size of 128 width and 64 height and mode '1' (black and white)
    logo_image = Image.new('1', (128, 64), color=0)
    drawer = ImageDraw.Draw(logo_image)

    byte_index = 0
    # Iterate through each byte and draw the corresponding bits
    for x in range(0, 128//8):  # Iterate from left to right in steps of 8
        for y in range(0, 64):  # Iterate from top to bottom
            for bi in range(8):
                # Extract the bit value (0 or 1)
                bit_value = (bytes_data[byte_index] >> bi) & 1
                
                # Draw a pixel based on the bit value
                color = 255 if bit_value == 1 else 0
                drawer.point((x*8+bi, 63 - y), fill=color)
            
            byte_index += 1

    # Save the image as a GIF
    logo_image.save(output_file, format="GIF")

def gif_to_bin(input_file, output_file):
    # Open the GIF image
    gif_image = Image.open(input_file)

    # Get the pixel data from the image
    pixel_data = list(gif_image.getdata())

    # Create a list to store the binary data
    binary_data = []

    # Iterate through each pixel and extract the bit value
    for x in range(0, 128//8):  # Iterate from left to right in steps of 8
        for y in range(0, 64):  # Iterate from top to bottom
            byte_value = 0
            # Extract the bit value for each pixel in the current byte
            for bi in range(8):
                pixel_index = x*8 + bi + ((63 - y) * 128)
                bit_value = 1 if pixel_data[pixel_index] == 255 else 0
                byte_value |= (bit_value << bi)

            # Append the byte value to the binary data list
            binary_data.append(byte_value)

    # Convert the list of bytes to bytes
    bytes_data = bytes(binary_data)

    # Write the binary data to the output file
    with open(output_file, 'wb') as file:
        file.write(bytes_data)

def main():
    print("\033[33m\033[22mLinkPi \033[32mOled Logo Converter V1.0\033[0m")
    print("\033[35m(c) 2024 YveIce under MIT licence\033[0m")

    if len(sys.argv) < 2:
        print(f"\nUsage:\n{sys.argv[0]} input.bin output.gif (convert binary to gif file)\n{sys.argv[0]} input.gif output.bin (convert gif to binary file)")
        sys.exit(1)

    input_file = sys.argv[1]
    if len(sys.argv) == 2:
        if input_file.endswith('.bin'):
            output_file = os.path.splitext(input_file)[0] + '.gif'
        else:
            output_file = os.path.splitext(input_file)[0] + '.bin'
    else:
        output_file = sys.argv[2]

    if not os.path.exists(input_file) or not (input_file.endswith('.bin') or input_file.endswith('.gif')):
        print("\033[31mInvalid argument. Please provide 'input.bin' or 'input.gif'\033[0m")
        sys.exit(1)

    if os.path.exists(output_file):
        overwrite = input("The output file already exists! Do you want to overwrite it? (Y/N): ").lower()
        if overwrite != 'y':
            print("\033[31mOperation aborted.\033[0m")
            sys.exit(1)

    if input_file.endswith('.bin'):
        bin_to_gif(input_file, output_file)
    else:
        gif_to_bin(input_file, output_file)
    print(f"\033[32mConversion successful! Output file: \033[33m{output_file}\033[0m")

if __name__ == "__main__":
    main()
