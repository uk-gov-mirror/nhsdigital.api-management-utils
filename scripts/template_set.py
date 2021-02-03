"""
template_set.py

Takes a comma delimted string and adds a value to the set

Usage:
  template_set.py [<set>] [-v <value> | --value=<value>]
  template_set.py (-h | --help)

Options:
  -h --help                        Show this screen.
  -v <value> | --value=<value>     Value to add to the set
"""
import sys
from docopt import docopt


def main(args):
    input_value = str(args["--value"])
    if args["<set>"]:
        input_set = str(args["<set>"]).split(',')
        input_set.append(args["--value"])
    else:
        input_set = [input_value]
    input_set = set(input_set)
    sys.stdout.write(",".join(input_set))
    sys.stdout.close()


if __name__ == "__main__":
    main(docopt(__doc__, version="1"))
