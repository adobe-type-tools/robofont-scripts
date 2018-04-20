__copyright__ = __license__ =  """
Copyright (c) 2013 Adobe Systems Incorporated. All rights reserved.

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

Sets the glyphs' Unicode values according to a GOADB file.

"""

import re
from robofab.interface.all.dialogs import GetFile
from fontTools.agl import AGL2UV as standardGlyphNamesDict

re_gUniName = re.compile(r'^uni[A-F0-9]{4}$')
re_gUName = re.compile(r'^u[A-F0-9]{5}$')


def readFile(filePath):
	file = open(filePath, 'r')
	fileContent = file.read().splitlines()
	file.close()
	return fileContent


font = CurrentFont()

path = GetFile("Open GOADB file...")

if path:
	fileContent = readFile(path)
	unicodeMappingsDict = {} # key is friendly glyph name; value is Unicode value

	# Reads the GOADB file and fills-in the dictionary
	lineNumber = 1
	for line in fileContent:
		entries = line.split()
		if len(entries) >= 2:
			if (entries[0][0] not in ['%','#']):
				finalGlyphName, prodGlyphName = entries[0], entries[1]
				if len(entries) == 3:
					uniOverride = entries[2]
				else:
					uniOverride = None

				# the final name is uniXXXX
				if re_gUniName.match(finalGlyphName):
					unicodeMappingsDict[prodGlyphName] = int(finalGlyphName[-4:], 16)
				# the final name is uXXXXX
				elif re_gUName.match(finalGlyphName):
					unicodeMappingsDict[prodGlyphName] = int(finalGlyphName[-5:], 16)
				# the GOADB line has a Unicode override
				elif uniOverride:
					unicodeMappingsDict[prodGlyphName] = int(uniOverride[-4:], 16)
				# the final name is standard
				elif finalGlyphName in standardGlyphNamesDict:
					unicodeMappingsDict[prodGlyphName] = standardGlyphNamesDict[finalGlyphName]
		else:
			print "Skipped line number %d: %s" % (lineNumber, line)
		lineNumber += 1

	# Assign the Unicode values
	for glyph in font:
		if glyph.name in unicodeMappingsDict:
			glyph.unicode = unicodeMappingsDict[glyph.name]

	print "Done!"
