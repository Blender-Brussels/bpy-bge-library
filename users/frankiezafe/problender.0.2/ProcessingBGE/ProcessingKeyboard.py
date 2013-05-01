from ProcessingBGE.ProcessingBGE import ProcessingBGE as pbge

if pbge.isconfigured():
	co = bge.logic.getCurrentController()
	keyboard = co.sensors["Keyboard"]

	for key,status in keyboard.events:
		if status is bge.logic.KX_INPUT_JUST_ACTIVATED:
			if key not in self.keydown:
				self.keydown.append( key )
			# print( key, "pressed" )
		elif status is bge.logic.KX_INPUT_ACTIVE:
			if key in self.keydown:
				self.keydown.remove( key )
			if key not in self.keyactive:
				self.keyactive.append( key )
			# print( key, "active" )
		elif status is bge.logic.KX_INPUT_JUST_RELEASED:
			if key in self.keydown:
				self.keydown.remove( key )
			if key in self.keyactive:
				self.keyactive.remove( key )
			if key not in self.keyup:
				self.keyup.append( key )
			# print( key, "released" )

