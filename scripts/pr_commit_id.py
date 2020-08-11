"""
pr_commit_id.py

Takes pull request number and retrieves the latest pull request commit hash

Can operate with a template file or from stdin. Replacements can be supplied as an argument in JSON format or from env.

Usage:
  template.py REPO_NAME PULL_NUMBER
  template.py (-h | --help)

Options:
  -h --help                                       Show this screen.
"""
import requests
from docopt import docopt


def main(args):
    print(f"https://api.github.com/repos/{args['REPO_NAME']}/pulls/{args['PULL_NUMBER']}/commits")
    response = requests.get(f"https://api.github.com/repos/{args['REPO_NAME']}/pulls/{args['PULL_NUMBER']}/commits").json()
    latest_commit = response[len(response) - 1]
    commit_hash = latest_commit["commit"]["tree"]["sha"]
    print(commit_hash)


if __name__ == "__main__":
    main(docopt(__doc__, version="1"))
