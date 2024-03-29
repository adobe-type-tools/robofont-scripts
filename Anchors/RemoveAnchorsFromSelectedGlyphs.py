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
Remove Anchors From Selected Glyphs v1.0 - Feb 21 2013

Removes all the anchors from the selected glyphs.

==================================================
Versions:
v1.0 - Feb 21 2013 - Initial release
"""

def run(font):
	anchorFound = False

	for glyphName in font.selection:
		glyph = font[glyphName]
		if len(glyph.anchors) > 0:
			glyph.clearAnchors()
			glyph.glyphChangedUpdate()
			anchorFound = True

	if anchorFound:
		print('Anchors were removed.')
	else:
		print('The selected glyphs had no anchors.')


if __name__ == "__main__":
	font = CurrentFont()
	if font == None:
		print('Open a font first.')
	else:
		if not len(font):
			print("The font has no glyphs.")
		elif not len(font.selection):
			print("Select the glyphs.")
		else:
			run(font)
