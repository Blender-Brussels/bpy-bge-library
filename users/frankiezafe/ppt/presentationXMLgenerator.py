import os

def get_filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.

# Run the above function and store its results in a variable.   
filepaths = get_filepaths("assets")
filepaths.sort()

target = open( "assets.xml", 'w' )
target.write( '<?xml version="1.0"?>\n' )
target.write( '<presentation>\n' )

for fp in filepaths:
	target.write( '\t<slide>\n' )
	if fp[-4:] == ".jpg" or fp[-4:] == ".png" or fp[-4:] == ".tif" or fp[-5:] == ".tiff":
		target.write( '\t\t<img src="' + fp + '" />\n' )
	if fp[-4:] == ".mov" or fp[-4:] == ".avi" or fp[-4:] == ".mp4":
		target.write( '\t\t<video src="' + fp + '" />\n' )
	target.write( '\t</slide>\n' )

target.write( '</presentation>' )
target.close()

print( filepaths )
