import bpy
import xml.etree.ElementTree as ET

xml_file = bpy.path.abspath( '//' + 'presentation.xml' )
xml_tree = ET.parse(xml_file)

print( xml_tree )

page = ET.parse( bpy.path.abspath( '//' + 'presentation.xml' ) )
for p in page.getiterator():
    if p.tag == "img":
        print( "IMAGE", p )
        print( p.tag )
        print( p.attrib )
    if p.tag == "text":
        print( "TEXT", p )
        print( p.tag )
        print( p.attrib )
    if p.tag == "video":
        print( "VIDEO", p )
        print( p.tag )
        print( p.attrib )
    '''
    print ("ppp", p.tag, repr(p.text) )
    for c in p:
        print ( "ccc", c.tag, repr(c.text), p.tag )
    '''