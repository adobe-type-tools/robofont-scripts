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

Clears the contents of the layer named 'mask'.

"""

#----------------------------------------

kMaskLayerName = 'mask'

from AppKit import NSApp

def glyphWindowHasFocus():
	window = NSApp.orderedWindows()[0]
	if hasattr(window, "windowName"):
		if window.windowName() == "GlyphWindow":
			return True
	return False


def clearGlyphMask(g):
	maskGlyph = g.getLayer(kMaskLayerName, clear=False)
	if len(maskGlyph) or maskGlyph.components:
		g.getLayer(kMaskLayerName, clear=True)
		g.update()


if glyphWindowHasFocus():
	g = CurrentGlyph()
	clearGlyphMask(g)	
else:
	f = CurrentFont()
	for gName in f.selection:
		g = f[gName]
		clearGlyphMask(g)	
