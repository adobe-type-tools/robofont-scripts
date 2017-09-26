"""
Takes in an anchors-like file plus one (or more) UFOs and adds anchors to the
glyphs. One of the big differences from "Anchors Input" is that the latter
deletes all existing anchors before adding. The other difference is that X and Y
values are optional.
"""
from __future__ import print_function, division

import os
import sys

from defcon import Font, Anchor


POS_KEYWORDS = [
'TOP_LEFT',
'TOP_CENTER',
'TOP_RIGHT',
'MID_LEFT',
'MID_CENTER',
'MID_RIGHT',
'BOT_LEFT',
'BOT_CENTER',
'BOT_RIGHT',
]

def readFile(filePath):
    file = open(filePath, 'r')
    fileContent = file.read().splitlines()
    file.close()
    return fileContent


def get_glyph_pos(bounds):
    """bounds is a tuple in the form (xMin, yMin, xMax, yMax).
       This function calculates a few important positions
       defined by the glyph's outlines, and returns them
       as a dict of keywords."""
    xMin, yMin, xMax, yMax = (int(i) for i in bounds)
    xCen = int((xMax+xMin)/2)
    yMid = int((yMax+yMin)/2)

    glyph_pos = {}
    glyph_pos['TOP_LEFT']   = (xMin, yMax)
    glyph_pos['TOP_CENTER'] = (xCen, yMax)
    glyph_pos['TOP_RIGHT']  = (xMax, yMax)
    glyph_pos['MID_LEFT']   = (xMin, yMid)
    glyph_pos['MID_CENTER'] = (xCen, yMid)
    glyph_pos['MID_RIGHT']  = (xMax, yMid)
    glyph_pos['BOT_LEFT']   = (xMin, yMin)
    glyph_pos['BOT_CENTER'] = (xCen, yMin)
    glyph_pos['BOT_RIGHT']  = (xMax, yMin)

    return glyph_pos


def place_anchors(font, anchors):
    """anchors is a dict in the form
       {'glyph_name': {'anchor_name1': 'BOT_LEFT',
                       'anchor_name2': (320, -20)}}"""

    placed_count = 0

    for gname, anchor_names in anchors.items():
        if gname not in font.keys():
            continue
        glyph = font[gname]
        glyph_pos = get_glyph_pos(glyph.bounds)
        glyph_anchors = [anchor.name for anchor in glyph.anchors]

        for anchor_name, anchor_pos in anchor_names.items():
            if isinstance(anchor_pos, tuple):
                pass
            else:
                anchor_pos = glyph_pos[anchor_pos]

            anchor = Anchor()
            anchor.name = anchor_name
            anchor.x, anchor.y = anchor_pos

            if anchor_name not in glyph_anchors:
                glyph.appendAnchor(anchor)
                placed_count += 1

    if placed_count:
        font.save()
        print(os.path.basename(font.path))
        print('  %d anchors placed' % placed_count)


def parse_anchors_file(file_path):
    anchors_data = readFile(file_path)
    anchors_dict = {}

    for index, line in enumerate(anchors_data):
        stripped_line = line.strip()
        # skip comments and blank lines
        if (not stripped_line) or (stripped_line.startswith('#')):
            continue

        anchor_info = stripped_line.split('\t')
        if len(anchor_info) < 2:
            print("ERROR: Line #%d doesn't have at least 2 columns. Skipped." % (index +1))
            continue

        glyph_name, anchor_name = anchor_info[:2]
        anchor_pos = anchor_info[2:]

        if len(anchor_pos) == 0:
            # the position was left blank; use X=Y=0
            anchor_pos = tuple([0,0])
        elif len(anchor_pos) == 1 and anchor_pos[0] in POS_KEYWORDS:
            # the position is defined by a keyword string
            anchor_pos = anchor_pos[0]
        elif len(anchor_pos) == 2:
            # the position is defined by X and Y values
            anchor_pos = tuple([int(eval(pos)) for pos in anchor_pos[:2]])
        else:
            print("WARNING: Not sure how to parse line #%d. Skipped." % (index +1))
            continue

        if glyph_name not in anchors_dict:
            anchors_dict[glyph_name] = {anchor_name: anchor_pos}
        else:
            if anchor_name in anchors_dict[glyph_name]:
                print("ERROR: Duplicate anchor entry found at line #%d. Skipped." % (index +1))
            else:
                anchors_dict[glyph_name].update({anchor_name: anchor_pos})

    return anchors_dict


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args) < 2:
        print('Not enough paths provided')
        return 1

    # first path is the anchors file
    # the remaining paths are fonts
    anchors_file = args[0]
    fonts  = args[1:]

    anchors = parse_anchors_file(anchors_file)

    for path in fonts:
        font = Font(path)
        place_anchors(font, anchors)

    print('Done!')


if __name__ == "__main__":
    sys.exit(main())
