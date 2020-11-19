"""
template_dict.py

Takes a dict string and adds a value to the dictionary

Usage:
  template_dict.py [<dictionary>] [-k <key> | --key=<key>] [-v <value> | --value=<value>]
  template_dict.py (-h | --help)

Options:
  -h --help                        Show this screen.
  -k <key> --key=<key>             Key to store in dictionary
  -v <value> | --value=<value>     Value to save against the key in the dictionary
"""
import sys
import json
from docopt import docopt


def main(args):
    try:
        dictionary = json.loads(args["<dictionary>"])
    except json.JSONDecodeError:
        print(args["<dictionary>"])
        dictionary = {}
    dictionary[args["--key"]] = args["--value"]
    print(args["<dictionary>"])
    sys.stdout.write(str(dictionary))
    sys.stdout.close()


if __name__ == "__main__":
    main(docopt(__doc__, version="1"))
