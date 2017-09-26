"""
Takes in a renaming file plus one (or more) UFOs and renames the anchors that
match the names. The anchor coordinates are ignored.

Format of the renaming file:
glyph_name<tab>current_anchor_name<tab>new_anchor_name
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


def rename_anchors(font, anchors):
    """anchors is a dict in the form
       {'glyph_name': {'current_anchor_name1': 'new_anchor_name1',
                       'current_anchor_name2': 'new_anchor_name2'}}"""

    renamed_count = 0

    for gname, anchor_names in anchors.items():
        if gname not in font.keys():
            continue
        glyph = font[gname]
        for anchor in glyph.anchors:
            if anchor.name in anchor_names:
                anchor.name = anchor_names[anchor.name]
                renamed_count += 1

    if renamed_count:
        font.save()
        print(os.path.basename(font.path))
        print('  %d anchors renamed' % renamed_count)


def parse_anchors_file(file_path):
    anchors_data = readFile(file_path)
    anchors_dict = {}

    for index, line in enumerate(anchors_data):
        stripped_line = line.strip()
        # skip comments and blank lines
        if (not stripped_line) or (stripped_line.startswith('#')):
            continue

        anchor_info = line.split('\t')
        if len(anchor_info) < 3:
            print("ERROR: Line #%d doesn't have at least 3 columns. Skipped." % (index +1))
            continue

        glyph_name, current_anchor_name, new_anchor_name = anchor_info[:3]

        if glyph_name not in anchors_dict:
            anchors_dict[glyph_name] = {current_anchor_name: new_anchor_name}
        else:
            if current_anchor_name in anchors_dict[glyph_name]:
                print("ERROR: Duplicate anchor renaming entry found at line #%d. Skipped." % (index +1))
            else:
                anchors_dict[glyph_name].update({current_anchor_name: new_anchor_name})

    return anchors_dict


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    if len(args) < 2:
        print('Not enough paths provided')
        sys.exit(1)

    # first path is the anchors file
    # the remaining paths are fonts
    anchors_file = args[0]
    fonts  = args[1:]

    anchors = parse_anchors_file(anchors_file)

    for path in fonts:
        font = Font(path)
        rename_anchors(font, anchors)

    print('Done!')


if __name__ == "__main__":
    sys.exit(main())
