#!/bin/bash

# If Blender is in your PATH
#blender -b -P lookback.py

# If blender is NOT in your path
# /absolute/path/to/blender/folder/./blender -b -P lookback.py
# Example
/home/juego/blender-2.68a-linux-glibc211-i686/./blender -b -P lookback.py


# You need to have imagemagick installed
convert output/* lookback.gif

# Removes temporary output folder
rm -R output/

echo "Done. Have a look at lookback.gif"
