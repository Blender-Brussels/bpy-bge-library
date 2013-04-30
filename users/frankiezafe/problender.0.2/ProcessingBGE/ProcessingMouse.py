from ProcessingBGE.ProcessingBGE import ProcessingBGE as pbge

if pbge.isconfigured():
	co = bge.logic.getCurrentController()
	mouse = co.sensors["Mouse"]
	
	# position	
	pbge.mouseX = mouse.position[0] / bge.render.getWindowWidth()
	pbge.mouseY = mouse.position[1] / bge.render.getWindowHeight()

	# buttons
	lb = mouse.getButtonStatus( bge.events.LEFTMOUSE )
	mb = mouse.getButtonStatus( bge.events.MIDDLEMOUSE )
	rb = mouse.getButtonStatus( bge.events.RIGHTMOUSE )
	if lb == bge.logic.KX_INPUT_NONE or lb == bge.logic.KX_INPUT_JUST_RELEASED: 
		pbge.mouseLeft = False
	else:
		pbge.mouseLeft = True
	
	if mb == bge.logic.KX_INPUT_NONE or mb == bge.logic.KX_INPUT_JUST_RELEASED:
		pbge.mouseMiddle = False
	else:
		pbge.mouseMiddle = True
	
	if rb == bge.logic.KX_INPUT_NONE or rb == bge.logic.KX_INPUT_JUST_RELEASED:
		pbge.mouseRight = False
	else:
		pbge.mouseRight = True
