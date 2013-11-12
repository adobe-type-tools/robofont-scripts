# load encoding file as UFO glyph order

import os
import re
from robofab.interface.all import dialogs_mac_vanilla
from robofab.interface.all.dialogs_mac_vanilla import GetFile

f = CurrentFont()
encPath = os.path.dirname(f.path)
encodingFiles = [fileName for fileName in os.listdir(encPath) if fileName.endswith('.enc')]

if len(encodingFiles) == 1:
	encodingFile = os.sep.join((encPath, encodingFiles[0]))
else:
    encodingFile = GetFile(message='Pick Encoding File', title=None, directory=encPath, fileName=None, allowsMultipleSelection=False, fileTypes=None)

if encodingFile:
    encF = open(encodingFile, 'r')
    encData = encF.read().splitlines()
    encF.close()

    enc = []
    for line in encData:
    	if not re.match(r'^#|%', line) and not line =='' and not line in enc:
    		line = line.split()[0]
    		enc.append(line)

    f.lib['com.typemytype.robofont.sort'] = enc
    f.glyphOrder = enc
    f.update()

else:
    print 'Cancelled'