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
Anchors Input v1.2 - Jun 27 2017

Adds anchors to the glyphs by reading the data from external text file(s) named
'anchors'. If the family has more than one master, append '_X' to the name.
The 'X' must be replaced by the index of the font master, counting from 0.
The simple text file(s) containing the anchor data must have four tab-separated
columns that follow this format:
<glyphName><tab><anchorName><tab><anchorXposition><tab><anchorYposition>

==================================================
Versions:
v1.2 - Jun 27 2017 - Support comments and ignore blank lines
v1.1 - Apr 26 2016 - Use the same file naming logic as the derivedchars files
v1.0 - Feb 21 2013 - Initial release
"""

#----------------------------------------

kAnchorsFileName = "anchors"

#----------------------------------------

import os


class myAnchor:
	def __init__(self, parent, name, x=0, y=0):
		self.parent = parent
		self.name = name
		self.x = x
		self.y = y


def readFile(filePath):
	file = open(filePath, 'r')
	fileContent = file.read().splitlines()
	file.close()
	return fileContent


def run(font, masterNumber):

	if masterNumber:
		filePath = "%s_%s" % (kAnchorsFileName, masterNumber)
	else:
		filePath = kAnchorsFileName

	if not os.path.isfile(filePath):
		print('ERROR: File %s not found.' % filePath)
		return

	print('Reading file %s ...' % filePath)
	anchorsData = readFile(filePath)
	anchorsList = []

	for lineIndex in range(len(anchorsData)):
		stripped_line = anchorsData[lineIndex].strip()

		# skip comments and blank lines
		if (not stripped_line) or (stripped_line.startswith('#')):
			continue

		anchorValuesList = anchorsData[lineIndex].split('\t')
		if len(anchorValuesList) != 4: # Four columns: glyph name, anchor name, anchor X postion, anchor Y postion
			print('ERROR: Line #%d does not have 4 columns. Skipped.' % (lineIndex +1))
			continue

		glyphName = anchorValuesList[0]
		anchorName = anchorValuesList[1]

		if not len(glyphName) or not len(anchorName):
			print('ERROR: Line #%d has no glyph name or no anchor name. Skipped.' % (lineIndex +1))
			continue

		try:
			anchorX = int(anchorValuesList[2])
			anchorY = int(anchorValuesList[3])
		except:
			print('ERROR: Line #%d has an invalid anchor position value. Skipped.' % (lineIndex +1))
			continue

		newAnchor = myAnchor(glyphName, anchorName, anchorX, anchorY)
		anchorsList.append(newAnchor)


	if not len(anchorsList):
		print('No valid anchors data was found.')
		return


	# Remove all anchors
	for glyph in font:
		if len(glyph.anchors) > 0:
			glyph.clearAnchors()
			glyph.glyphChangedUpdate()


	# Add all anchors
	for anchor in anchorsList:
		# Make sure that the glyph exists
		if font.has_key(anchor.parent):
			glyph = font[anchor.parent]
		else:
			print('ERROR: Glyph %s not found in the font.' % anchor.parent)
			continue

		glyph.appendAnchor(anchor.name, (anchor.x, anchor.y))
		glyph.glyphChangedUpdate()
# 		glyph.mark = 125

	print('Done!')


if __name__ == "__main__":
	font = CurrentFont()
	if font == None:
		print('Open a font first.')
	else:
		if not font.path:
			print('Save the font first.')
		elif not len(font):
			print('The font has no glyphs.')
		else:
			folderPath, fileName = os.path.split(font.path)
			fileNameNoExtension, fileExtension = os.path.splitext(fileName)
			masterNumber = fileNameNoExtension.split('_')[-1]

			if not masterNumber.isdigit():
				masterNumber = None

			os.chdir(folderPath) # Change current directory to the location of the opened font
			run(font, masterNumber)
