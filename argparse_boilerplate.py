"""
Some boilerplate for argparse.

Accept 2 strings and print them.

"""
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Provide an input file and an output file.")
    parser.add_argument('-i', type=str, required=True, help="Input file")
    parser.add_argument('-o', type=str, required=True, help="Output file")

    args = parser.parse_args()

    print args

