#!/bin/bash

# If Blender is in your PATH
blender -b -P lookback.py

# If blender is not in your path
# /absolute/path/to/blender/folder/./blender -b -P lookback.py

# You need to have imagemageck installed
convert output/* lookback.gif 
