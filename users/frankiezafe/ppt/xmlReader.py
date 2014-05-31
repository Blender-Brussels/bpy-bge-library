import bge
import xml.etree.ElementTree as ET
control = bge.logic.getCurrentController()
owner = control.owner
scene = bge.logic.getCurrentScene()
xml_file = bge.logic.expandPath('//' + 'slide.xml')
tree = ET.parse(xml_file)
root = tree.getroot()
owner['currentSlide'] = 0

def nextSlide():
    owner.text = root[owner['currentSlide']][0].text

def updateText():
    if not owner.sensors['Keyboard'].positive:
        return
    
    if owner['currentSlide'] < len(root):
        nextSlide()
        owner['currentSlide'] += 1