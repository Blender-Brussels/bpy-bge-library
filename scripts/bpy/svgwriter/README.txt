SVGWriter for Blender/Freestyle
===============================
:Author: Tamito KAJIYAMA
:Last modified: April 28, 2013


Introduction
------------

The SVGWriter package provides a set of Python script files for
authoring SVG documents with Blender and Freestyle.  SVG documents to
be generated are either still images or animation clips.

The latest version of the SVGWriter package is available at:

  http://www.geocities.jp/blenderyard/freestyle/svgwriter_b26.zip

Blender 2.67 is required to use the SVGWriter package.  The package
has been tested with a 64-bit Windows build of Blender trunk revision
56331.

The SVGWriter package includes the following files:

* ``svgwriter_image.py``

  A style module for Freestyle to generate a single still SVG image
  from a 3D scene in Blender.

* ``svgwriter_anim.py``

  A style module for Freestyle to generate a series of still frames
  comprising an SVG animation clip.

* ``svgwriter_concat.py``

  An extension file for Blender 2.6 to provide a graphical user
  interface for postprocessing a set of frames.

The first 2 scripts can be stored in an arbitrary directory, e.g. in
``$BLENDER_DIR/2.67/scripts/freestyle/style_modules/``, where
``$BLENDER_DIR`` refers to the top directory of a Blender
installation.  The last script needs to be put into
``$BLENDER_DIR/2.67/scripts/startup/``.


Still image rendering
---------------------

Follow the steps below to render a still image from a 3D scene in
Blender:

1. Enable Freestyle in the Freestyle tab in the Render buttons.

2. In the Freestyle tab in the Render Layers buttons, select the
   Python Script Mode from the Control Mode pull-down menu, and add
   ``svgwriter_image.py`` into the style module stack.

3. Go back to the Render buttons, and specify image resolutions in the
   Dimension tab and an output directory in the Output tab.

4. Start still image rendering, e.g. by selecting Render >> Render
   Image (F12) from the menu in the Info window.

After the rendering has finished, an SVG file named ``output.svg`` is
created in the output directory.

Since Freestyle is a programmable line drawing framework, you have a
considerable amount of freedom in defining new style modules yourself.
At the end of ``svgwriter_image.py``, you may find a list of stroke
shaders like below::

  shaders_list = [
          #ConstantThicknessShader(2),
          pyDepthDiscontinuityThicknessShader(1, 4),
          ConstantColorShader(0, 0, 0),
          #pyMaterialColorShader(0.5),
          writer,
  ]

You can enable/disable a shader by removing/adding ``#`` in front of
the shader name.  You can also control line thickness and line color
by changing the shader parameters using a text editor.  The "writer"
in the above list of shaders is a shader to generate the SVG still
image.  Since shaders are executed one after another in the order in
the list, you need to specify the SVG writer at the end of the shader
list.


Animation rendering
-------------------

Follow the steps below to render an SVG animation clip from a 3D scene
in Blender:

1. Enable Freestyle in the Freestyle tab in the Render buttons.

2. In the Freestyle tab in the Render Layers buttons, select the
   Python Script Mode from the Control Mode pull-down menu, and add
   ``svgwriter_anim.py`` into the style module stack.

3. Go back to the Render buttons, and specify image resolutions, frame
   range, frame rate in the Dimension tab and an output directory in
   the Output tab.

4. Start animation rendering, e.g. by selecting Render >> Render
   Animation (Ctrl F12) from the menu in the Info window.

5. After the rendering has done, choose a horizon color (in the World
   tab in the World buttons).  The horizon color will be the
   background color of the animation clip.

6. Go to the SVGWriter tab in the Render buttons, specify an output
   SVG file name, and press the Concatenate Frames button.  This
   results in an SVG animation clip file stored in the output
   directory.

When the rendering in Step 3 has completed, a series of XML files in a
file name like ``frame000001.xml`` are created in the output
directory.  Each XML file contains an SVG fragment that draws a still
frame comprising the animation clip.  The controls in the SVGWriter
tab (provided by ``svgwriter_concat.py``) allow you to concatenate
these SVG fragment files into a finished, single SVG animation clip
file.

You can change stroke shaders and their parameters by manually editing
``svgwriter_anim.py`` as in the case of still image rendering.


Known issues
------------

* Only constant line thickness and constant line colors are supported
  due to the fact that Freestyle strokes are translated into open SVG
  paths.  Use of variable line thickness/color shaders will lead to
  unexpected results.


License
-------

This is free software; you can freely redistribute it and/or
modify it under the terms of the GNU General Public License
(version 2 or later).

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY.  Use it at your own risk.


Contact
-------

Tamito KAJIYAMA <rd6t-kjym at asahi-net dot or dot jp>

Please, feel free to write to me in case you have comments,
suggestions, and/or patches.  Both English and Japanese are welcome.
