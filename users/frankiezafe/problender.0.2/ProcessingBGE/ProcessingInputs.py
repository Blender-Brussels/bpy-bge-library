# replace mouse and keyboard py.
# must be connected to an always actuator!

from ProcessingBGE.ProcessingBGE import ProcessingBGE as pbge

#TODO
if pbge.isconfigured():
	kb = bge.logic.keyboard
	print( kb.events )
