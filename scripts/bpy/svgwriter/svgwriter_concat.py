# Tamito KAJIYAMA <24 October 2009>

import os, xml.etree.ElementTree

_HEADER = """\
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" 
  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1"
     width="%d" height="%d">
<rect x="0" y="0" width="%d" height="%d" fill="%s" />
"""
_FOOTER = """\
</svg>
"""

def concat_frames(input_dir, output_path, w, h, bg_color="#000000"):
	frames = [f for f in os.listdir(input_dir) if f.startswith("frame")]
	frames.sort()
	output_file = open(output_path, "wt")
	output_file.write(_HEADER % (w, h, w, h, bg_color))
	for i, frame in enumerate(frames):
		f = open(os.path.join(input_dir, frame))
		root = xml.etree.ElementTree.XML(f.read())
		f.close()
		assert(root.tag == "g")
		child = root.find("set")
		if i < len(frames) - 1:
			child.attrib["fill"] = "remove"
		else:
			child.attrib["fill"] = "freeze"
		s = xml.etree.ElementTree.tostring(root)
		output_file.write(s.decode('us-ascii'))
	output_file.write(_FOOTER)
	output_file.close()
	print("Wrote:", output_path)

##### User interface #####

import bpy

from bpy.props import StringProperty

# define new Scene property
bpy.types.Scene.svgwriter_output_filename = StringProperty(
	name="SVGWriter Output File Name",
	description="Output file name for SVGWriter",
	default="output.svg")

# define new operator
class RENDER_OT_svgwriter_concat_frames(bpy.types.Operator):
	'''Concatenate SVGWriter frames into a single SVG animation clip.'''
	bl_idname = "render.svgwriter_concat_frames"
	bl_label = "Concatenate SVGWriter Frames"

	filename = StringProperty(name="SVGWriter Output File Name",
				  description="Output file name for SVGWriter",
				  maxlen=1024,
				  default="output.svg")
	
	def execute(self, context):
		rd = context.scene.render
		input_dir = bpy.path.abspath(rd.filepath)
		output_path = os.path.join(input_dir, self.properties.filename)
		w = rd.resolution_x
		h = rd.resolution_y
		world = context.scene.world
		bg_color = "#" + "".join("%02x" % (c * 255) for c in world.horizon_color)
		concat_frames(input_dir, output_path, w, h, bg_color)
		return {'FINISHED'}

# define new Render panel
class RENDER_PT_svgwriter(bpy.types.Panel):
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "render"
	bl_label = "SVGWriter Post Processing"
	bl_default_closed = True
	COMPAT_ENGINES = {'BLENDER_RENDER'}

	def draw(self, context):
		scene = context.scene
		layout = self.layout
		layout.prop(scene, "svgwriter_output_filename",
			    text="File Name")
		prop = layout.operator("render.svgwriter_concat_frames",
				       text="Concatenate Frames",
				       icon="FILE_MOVIE")
		prop.filename = scene.svgwriter_output_filename

def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
