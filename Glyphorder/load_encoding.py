#!/usr/bin/python

# Load GlyphOrderAndAliasDB or encoding file as UFO glyph order.
# The script can either be run from RF, or from the command line.
# In RF, the glyph order will be loaded for the frontmost UFO.
# On the command line, multiple UFO files can be passed as arguments.
# Glyphs not present in sort file will be marked grey.

import os
import sys
from defcon import Font


def findFile(fileName, path, maxDepth=3):
    '''
    Finds file `fileName` starting at `path`; moving up the
    directory tree until `maxDepth` is reached.
    Returns the first file found, or `None` if nothing is found.
    '''

    depth = 0
    path = os.path.abspath(path)
    while fileName not in os.listdir(path) and depth < maxDepth:
        path = os.path.dirname(path)
        depth += 1

    else:
        if depth == maxDepth:
            return None
        else:
            return os.path.join(path, fileName)


def findFileBySuffix(suffix, path, maxDepth=3):
    '''
    Finds file with suffix `suffix` starting at `path`; moving up the
    directory tree until `maxDepth` is reached.
    Returns the first file found, or `None` if nothing is found.
    '''

    depth = 0
    path = os.path.abspath(path)

    # normalize the suffix
    suffix = suffix.lower()
    if not suffix.startswith('.'):
        suffix = '.' + suffix

    fileList = [
        fileName for fileName in os.listdir(path)
        if fileName.lower().endswith(suffix)]

    while not len(fileList) and depth < maxDepth:
        path = os.path.dirname(path)
        fileList = [
            fileName for fileName in os.listdir(path)
            if fileName.lower().endswith(suffix)]
        depth += 1

    else:
        if depth == maxDepth:
            return None
        else:
            return os.path.join(path, fileList[0])


def makeUniList(gList):
    '''
    This function creates a list gName|0123 with associated AGD Unicodes.
    However, RF is unreliable in assigning that glyph order.
    '''
    try:
        import agd
        agdfile = os.path.expanduser(
            "~/adobe/AdobeTypeLibrary/tools/shared/AGD.txt")
        with open(agdfile) as f:
            agdData = agd.dictionary(f.read())
        agdFound = True
    except ImportError:
        agdFound = False

    if agdFound:
        uniList = []
        for gName in gList:
            g = agdData.glyph(gName)
            if g and g.uni:
                line = '%s|%s' % (gName, g.uni)
            else:
                line = gName
            uniList.append(line)
        return uniList


def makeEnc(f, platform):
    fontDir = os.path.dirname(f.path)
    goaFile = findFile('GlyphOrderAndAliasDB', fontDir)
    encFile = findFileBySuffix('.enc', fontDir)

    if goaFile:
        sortFile = goaFile
    elif encFile:
        sortFile = encFile

    else:
        if platform == 'RF':
            from robofab.interface.all.dialogs import GetFile
            sortFile = GetFile(
                message='Pick Encoding File',
                title=None,
                directory=os.path.dirname(f.path),
                fileName=None,
                allowsMultipleSelection=False, fileTypes=None
                )

        else:
            print 'No GlyphOrderAndAliasDB or .enc file found.'
            sys.exit()

    print 'Sorting by %s\n' % sortFile

    if sortFile:
        encF = open(sortFile, 'r')
        raw_encData = encF.read().splitlines()
        encF.close()
        encData = []
        enc = []

        # avoid duplicate & empty lines, comments
        # and unneccessary glyphs:
        for line in raw_encData:
            stripLine = line.strip()
            if stripLine.startswith('%'):
                continue
            if stripLine.startswith('#'):
                continue
            if stripLine.startswith('NULL'):
                continue
            if stripLine.startswith('CR'):
                continue

            if stripLine and line not in encData:
                encData.append(line)

        if '\t' in encData[0]:
            # GOADB
            enc = [line.split()[1] for line in encData]
        else:
            # list
            enc = [line.split()[0] for line in encData]
    return enc


platform = None
enc = None

try:
    # in Robofont
    import mojo
    robofontFont = CurrentFont()
    if robofontFont.path != None:
        fontPaths = [robofontFont.path]
    else:
        fontPaths = []
    platform = 'RF'

except ImportError:
    # on command line
    fontPaths = sys.argv[1:]
    platform = 'CL'


if len(fontPaths):

    for fontPath in fontPaths:
        f = Font(fontPath)
        if not enc:
            # only necessary once for multiple UFOs
            enc = makeEnc(f, platform)

        remainingGlyphs = sorted(list(set(f.keys()) - set(enc)))

        f.lib['com.typemytype.robofont.sort'] = {
            'ascending': enc+remainingGlyphs,
            'type': 'glyphList'}
        f.lib['public.glyphOrder'] = enc+remainingGlyphs

        grey = [0.5, 0.5, 0.5, 0.5]
        for gName in remainingGlyphs:
            if gName in f:
                f[gName].lib['com.typemytype.robofont.mark'] = grey

        if platform == 'CL':
            f.save()
            print 'sorted', f.path

        if platform == 'RF':
            # uniList = makeUniList(enc+remainingGlyphs)
            # print uniList
            robofontFont.glyphOrder = enc+remainingGlyphs
            robofontFont.update()
            robofontFont.save()

        if len(remainingGlyphs):
            print 'Unencoded glyphs: %s\n' % ' '.join(remainingGlyphs)

else:
    if platform == 'CL':
        print 'Please specify one or more UFO files.'
    if platform == 'RF':
        print 'Please save your font first.'
