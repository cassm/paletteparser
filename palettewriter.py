import os
import sys
import imageio.v2 as imageio
import numpy as np

if len(sys.argv) != 3:
    print("""ERROR: incorrect usage.
    correct usage: genPalette.py filename outputLength

    filename should be the relative path to an rgb formatted .bmp
    outputLength is an integer, and determines the output length of the palette header
    """)

    exit(1)

bmpFile = sys.argv[1]
paletteLength = int(sys.argv[2])

if not os.path.isfile(bmpFile):
    print("ERROR: the file {} does not exist".format(bmpFile))

image = imageio.imread(bmpFile)
indices = list(int(i * (len(image[0]) - 1) / paletteLength) for i in range(paletteLength))

colours = []

for index in indices:
    colours.append([int(image[0][index][channel]) for channel in range(3)])

filename = bmpFile.split('/')[-1][:-4]
defguard = f"PALETTE_{filename.upper()}_H"
palette_str = str(colours).replace("[","{").replace("]","}")

with open(f"palette_{filename}.h", "w") as f:
    f.write(f"#ifndef {defguard}\n")
    f.write(f"#define {defguard}\n")
    f.write("#include <stdint.h>\n")
    f.write(f"static int palette_len = {paletteLength};\n")
    f.write(f"const uint8_t palette[{paletteLength}][3] = {palette_str};\n")
    f.write("#endif\n")
