# Tamito KAJIYAMA <19 August 2009>

from freestyle import *
from logical_operators import *
from shaders import *
import bpy
import os

_HEADER = """\
<g id="frame%06d" visibility="hidden">
<set attributeName="visibility" to="visible"
     begin="%.2fs" dur="%.2fs" fill="remove" />
"""
_PATH = """\
<path fill="none" stroke="%s" stroke-width="%d" d="M %s" />
"""
_FOOTER = """\
</g>
"""

class SVGWriter(StrokeShader):
	def __init__(self, f, w, h, start_frame, current_frame, frame_step, fps):
		StrokeShader.__init__(self)
		self.width, self.height = w, h
		self.file = f
		begin = float(current_frame - start_frame) / frame_step / fps
		dur = 1.0 / fps
		self.file.write(_HEADER % (current_frame, begin, dur))
	def close(self):
		self.file.write(_FOOTER)
		self.file.close()
	def shade(self, stroke):
		points = []
		for v in stroke:
			x, y = v.point
			points.append("%.3f,%.3f" % (x, self.height - y))
		points = " ".join(points)
		r, g, b = v.attribute.color * 255
		color = "#%02x%02x%02x" % (r, g, b)
		width = v.attribute.thickness
		width = width[0] + width[1]
		self.file.write(_PATH % (color, width, points))

class pyDiffuseColorShader(StrokeShader):
	"""A stroke color shader to use a material diffuse color as it is."""
	def getName(self):
		return "pyDiffuseColorShader"
	def shade(self, stroke):
		it = stroke.strokeVerticesBegin()
		func = MaterialF0D()
		while it.isEnd() == 0:
			mat = func(it.castToInterface0DIterator())
			r = mat.diffuseR()
			g = mat.diffuseG()
			b = mat.diffuseB()
			attr = it.getObject().attribute()
			attr.setColor(r, g, b)
			it.increment()

import freestyle
scene = freestyle.getCurrentScene()
start_frame = scene.frame_start
current_frame = scene.frame_current
frame_step = scene.frame_step
fps = scene.render.fps
output_dir = bpy.path.abspath(scene.render.filepath)
if not os.path.exists(output_dir):
	os.makedirs(output_dir)
path = os.path.join(output_dir, "frame%06d.xml" % current_frame)
f = open(path, "wt")
w = scene.render.resolution_x
h = scene.render.resolution_y

upred = QuantitativeInvisibilityUP1D(0)
Operators.select(upred)
Operators.bidirectional_chain(ChainSilhouetteIterator(), NotUP1D(upred))
writer = SVGWriter(f, w, h, start_frame, current_frame, frame_step, fps)
shaders_list = [
	ConstantThicknessShader(3),
	#pyDepthDiscontinuityThicknessShader(1, 4),
	ConstantColorShader(0, 0, 0),
	#pyMaterialColorShader(0.5),
	#pyDiffuseColorShader(),
	writer,
]
Operators.create(TrueUP1D(), shaders_list)
writer.close()
