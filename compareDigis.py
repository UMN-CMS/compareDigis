#!/usr/bin/env python

from sys import argv


def process_block(block_lines):
    """ Take a block from the text digi dump and convert it into a digi name
    and a line for each of the values."""
    name = None
    data_lines = []
    for line in block_lines:
        # The name line has has ( and )
        if '(' in line and ')' in line:
            name = line.split('(')[1].split(')')[0]
        else:
            data_lines.append(line.strip())

    # Return a tuple with the name and the data
    return (name, data_lines)


def make_digi_map(file_name):
    """ Take the file name of a text digi dump file and return a dictionary
    mapping the name of the digi to the values of its outputs."""
    digi_map = {}
    with open(file_name, 'r') as f:
        lines = []
        for line in f:
            # Blank lines separate the blocks
            if line == '\n':
                name, data = process_block(lines)
                digi_map[name] = data
                lines = []
            else:
                lines.append(line)

    return digi_map


# Run only if called directly
if __name__ == "__main__":

    header = "========================"
    left = "<<<<<<<<<<<<<<<<<<<<<<<<"
    right = ">>>>>>>>>>>>>>>>>>>>>>>>"
    new_line = "\n"
    indent_level = "\t"

    # Open the two files and make dictionaries
    vme_file = argv[1]
    utca_file = argv[2]
    vme_map = make_digi_map(vme_file)
    utca_map = make_digi_map(utca_file)

    # Find the unique and common digis
    vme_digis = frozenset(vme_map.keys())
    utca_digis = frozenset(utca_map.keys())
    vme_unique = vme_digis.difference(utca_digis)
    utca_unique = utca_digis.difference(vme_digis)
    common_digis = vme_digis.intersection(utca_digis)

    print header, "Digis Unique to VME", header
    for digi in vme_unique:
        print digi

    print new_line, header, "Digis Unique to uTCA", header
    for digi in utca_unique:
        print digi

    # Now check differences in the common digis
    print new_line, header, "Digis with Differences in VME Vs. uTCA", header
    for digi in common_digis:
        vme_list = vme_map[digi]
        utca_list = utca_map[digi]
        if vme_list != utca_list:
            print new_line, "Difference in", digi
            print indent_level, left, "VME"
            for line in vme_list:
                print indent_level, line
            print indent_level, right, "uTCA"
            for line in utca_list:
                print indent_level, line
