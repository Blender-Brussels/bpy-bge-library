Blender bpy/bge Brussels Workshop 2013-03-29 : zoom
===================================================
Inspiration for this project comes from ["Zoom from nowhere" by Chris Timms](http://vimeo.com/45550493)
and is a response to [this reddit post](http://www.reddit.com/r/blender/comments/1b794f/how_to_create_stream_of_images/).
This .blend file will help you make something similar.

Credits: Julien Deswaef, Frankie Zafe, Ofersmi, Olivier Meunier

Licence: CC-by

Setup:
------
On layer 1, there is a plane called "particle generator" which throws random planes at the camera.
On layer 2, there is a group of planes called "images" where "particle generator" will fetch the particles.

You first need to activate the "import images as planes" addon in >File>User Preferences>Addons to be able to import your own images.
(Suggestion: use png images with an alpha channel)
Delete the planes in layer 2 and replace them with your own images using the "import images as planes" tool.
Be sure to select "Shadeless", "Use alpha", "Z transparent" when importing images as planes.

Group those planes (ctrl+g) and name the group "whatever-you-like".

Switch to layer 1 and select the "particle generator". In the "Particle System" option window, under the "Render" tab, select the Dupli Group you've just named.

Play with the size, settings, etc... and hit render. :) 



