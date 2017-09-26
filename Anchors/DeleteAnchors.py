"""
Takes in an anchors file plus one (or more) UFOs and deletes
the anchors that match the 'glyph_name<tab>anchor_name' lines.
The anchors' coordinates are ignored.
"""
from __future__ import print_function

import os
import sys

from defcon import Font


def readFile(filePath):
    file = open(filePath, 'r')
    fileContent = file.read().splitlines()
    file.close()
    return fileContent


def delete_anchors(font, anchors):
    """anchors is a dict in the form
       {'glyph_name': ['anchor_name_1', 'anchor_name_2']}"""

    deleted_count = 0

    for gname, anchor_names in anchors.items():
        if gname not in font.keys():
            continue
        glyph = font[gname]
        for anchor in glyph.anchors:
            if anchor.name in anchor_names:
                glyph.removeAnchor(anchor)
                deleted_count += 1

    if deleted_count:
        font.save()
        print(os.path.basename(font.path))
        print('  %d anchors deleted' % deleted_count)


def parse_anchors_file(file_path):
    anchors_data = readFile(file_path)
    anchors_dict = {}

    for index, line in enumerate(anchors_data):
        stripped_line = line.strip()
        # skip comments and blank lines
        if (not stripped_line) or (stripped_line.startswith('#')):
            continue

        anchor_info = line.split('\t')
        if len(anchor_info) < 2: # Four columns: glyph name, anchor name, anchor X postion, anchor Y postion
            print("ERROR: Line #%d doesn't have at least 2 columns. Skipped." % (index +1))
            continue

        glyph_name, anchor_name = anchor_info[:2]

        if glyph_name not in anchors_dict:
            anchors_dict[glyph_name] = [anchor_name]
        else:
            anchors_dict[glyph_name] += [anchor_name]

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
        delete_anchors(font, anchors)

    print('Done!')


if __name__ == "__main__":
    sys.exit(main())
