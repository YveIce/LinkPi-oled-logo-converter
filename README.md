# LinkPi oled-logo-converter
Converts the 128x64 oled boot logo between binary and gif format. 
Tested with the LinkPi Enc1V3 https://linkpi.cn/archives/2021

## how to use:
### converting the binary logo to an gif file:
python logo_converter.py logo.bin [outputfilename.gif]  
### converting gif logo to an binary file:
python logo_converter.py logo.gif [outputfilename.bin]  

If no output-filename is provided, the script will use the input-filename, swapping the extension. If you create your own logo, make sure the image is 128x64 pixels in black and white. The script use an very simple logic to convert any color to black/white values, with out any dithering.

## requirements 
Python 3 with lib Pillow 

## about the file-format used by LinkPi
The binary format encodes a monochrome image with 1-bit pixels. Pixels are arranged in a fixed-width (128 pixels) and fixed-height (64 pixels) grid. 
The bytes represent 8 consecutive pixels, ordered left-to-right and top-to-bottom. Within each byte, the bits correspond to pixels in a left-to-right sequence. Visualization follows a top-to-bottom and left-to-right order.

## how to flash
check the update.sh file inside of /link/shell inside your device or update_enc1v3_ss524_********.bin file. (you can extract the update-bin-file using 7z or gzip). 
Something like this:
```bash
flash_erase /dev/mtd2 0 0
nandwrite -p /dev/mtd2 /link/update/logo.bin
```
> [!CAUTION]
> Be very careful! Always double check that this is the correct partition on YOUR device with YOUR current firmware! If you use the wrong partition, you can end up with an non booting device. If you messup the u-boot loader, then your device will be bricked. 

# license
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
