"""
This argpase boilerplate is designed to be run
in the top of __main__.
"""
import argparse

parser = argparse.ArgumentParser(description="Provide an input file and an output file.")
parser.add_argument('-i', type=str, required=True, help="Input file")
parser.add_argument('-o', type=str, required=True, help="Output file")
args = parser.parse_args()

# User reviews input filename.
answer = None
while answer not in ('y', 'n', 'q'):
    answer = raw_input("Is the INPUT filename correct: {} (y/n/q)".format(args.i,))
if answer in ('n', 'q'):
    exit("Aborted.")

# User reviews output filename.
answer = None
while answer not in ('y', 'n', 'q'):
    answer = raw_input("Is the OUTPUT filename correct: {} (y/n/q)".format(args.o,))
if answer in ('n', 'q'):
    exit("Aborted.")
