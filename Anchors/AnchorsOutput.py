__copyright__ = __license__ =  """
Copyright (c) 2013-2016 Adobe Systems Incorporated. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

__doc__ = """
Anchors Output v1.1 - Apr 26 2016

Outputs all the anchor data to external text file(s) named 'anchors'.
If the family has more than one master, '_X' is appended to the name,
where 'X' represents the index of the font master, counting from 0.

==================================================
Versions:
v1.1 - Apr 26 2016 - Use the same file naming logic as the derivedchars files
v1.0 - Feb 21 2013 - Initial release
"""

#----------------------------------------

kAnchorsFileName = "anchors"

#----------------------------------------

import os


def run(font, masterNumber):

	anchorsList = []

	glyphOrder = font.lib['public.glyphOrder']
	if len(glyphOrder) != len(font.keys()):
		glyphOrder = font.keys()

	# Collect anchors data
	for glyphName in glyphOrder:
		glyph = font[glyphName]

		for anchorIndex in range(len(glyph.anchors)):
			anchor = glyph.anchors[anchorIndex]

			# Skip nameless anchors
			if not len(anchor.name):
				print "ERROR: Glyph %s has a nameless anchor. Skipped." % glyphName
				continue

			anchorData = "%s\t%s\t%d\t%d\n" % (glyphName, anchor.name, anchor.x, anchor.y)

			anchorsList.append(anchorData)


	if not len(anchorsList):
		print "The font has no anchors."
		return


	# Write file
	if masterNumber:
		filename = "%s_%s" % (kAnchorsFileName, masterNumber)
	else:
		filename = kAnchorsFileName
	print "Writing file %s ..." % filename
	outfile = open(filename, 'w')
	outfile.writelines(anchorsList)
	outfile.close()

	print 'Done!'


if __name__ == "__main__":
	font = CurrentFont()
	if font == None:
		print 'Open a font first.'
	else:
		if not font.path:
			print "Save the font first."
		elif not len(font):
			print "The font has no glyphs."
		else:
			folderPath, fileName = os.path.split(font.path)
			fileNameNoExtension, fileExtension = os.path.splitext(fileName)
			masterNumber = fileNameNoExtension.split('_')[-1]

			if not masterNumber.isdigit():
				masterNumber = None

			os.chdir(folderPath) # Change current directory to the location of the opened font
			run(font, masterNumber)
