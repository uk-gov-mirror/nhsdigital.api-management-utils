"""
env_cleaner.py

A tool for cleaning up apigee-envs

Usage:
  env_cleaner.py <apigee_org> <apigee_env> --access-token=<access_token> [--specs] [--proxies] [--products] [--sandbox-only] [--dry-run] [--min-age=<min_age>] [--undeploy-only]
  env_cleaner.py (-h | --help)

Options:
  -h --help                      Show this screen
  --access-token=<access_token>  Apigee access token to authorise requests
  --specs                        Prune specs
  --proxies                      Prune proxies
  --products                     Prune products
  --sandbox-only                 Only delete sandbox proxies
  --dry-run                      Print a listing of what will be deleted, but don't delete it.
  --undeploy-only                Don't delete any proxies, just undeploy them
  --min-age=<min_age>            Minimum age in seconds
"""
import re
import requests
from typing import Optional
from docopt import docopt
from apigee_client import ApigeeClient


SPEC_MATCHER = re.compile("(personal-demographics|identity-service|hello-world)-.+")
PROXY_MATCHER = re.compile(
    "(personal-demographics|identity-service|hello-world)-internal-dev-.+"
)
PRODUCT_MATCHER = PROXY_MATCHER
SANDBOX_MATCHER = re.compile(".+-sandbox$")
SANDBOX_ANTIMATCHER = re.compile(".+-internal-qa-sandbox")


def clean_specs(client: ApigeeClient, env: str, dry_run: bool = False):
    specs = client.list_specs()
    spec_names = [spec["name"] for spec in specs["contents"]]

    # Use the spec matcher to find specs that look like something we'd want to clean
    pr_specs = [spec for spec in spec_names if SPEC_MATCHER.match(spec)]

    for spec in pr_specs:
        print(f"DELETE SPEC {spec}")
        if not dry_run:
            client.delete_spec(spec)
            print(f"DELETED SPEC {spec}")


def clean_proxies(
        client: ApigeeClient, env: str, dry_run: bool = False, sandboxes_only: bool = False, min_age: Optional[int] = None, undeploy_only: bool = False
):
    proxies = client.list_proxies()
    pr_proxies = [proxy for proxy in proxies if PROXY_MATCHER.match(proxy)]

    if sandboxes_only:
        pr_proxies = [proxy for proxy in proxies if SANDBOX_MATCHER.match(proxy) and not SANDBOX_ANTIMATCHER.match(proxy)]

    for proxy in pr_proxies:
        proxy_info = client.get_proxy(proxy)
        for revision in proxy_info['revision']:
            print(f"UNDEPLOY {proxy} REVISION {revision}")
            if not dry_run:
                try:
                    client.undeploy_proxy_revision(env, proxy, revision)
                except requests.exceptions.HTTPError as e:
                    print(f"ERROR UNDEPLOYING {proxy} REVISION {revision}: may already be undeployed")

        if not undeploy_only:
            print(f"DELETE PROXY {proxy}")
            if not dry_run:
                client.delete_proxy(proxy)


def clean_products(client: ApigeeClient, env: str, dry_run: bool = False):
    products = client.list_products()
    pr_products = [product for product in products if PRODUCT_MATCHER.match(product)]

    for product in pr_products:
        print(f"DELETE PRODUCT {product}")
        if not dry_run:
            client.delete_product(product)


def clean_env(
    client: ApigeeClient,
    env: str,
    should_clean_specs: bool = False,
    should_clean_proxies: bool = False,
    should_clean_products: bool = False,
    sandboxes_only: bool = False,
    dry_run: bool = False,
    min_age: Optional[int] = None,
    undeploy_only: bool = False
):
    if should_clean_specs:
        clean_specs(client, env, dry_run)

    if should_clean_proxies:
        clean_proxies(client, env, dry_run, sandboxes_only, min_age, undeploy_only)

    if should_clean_products:
        clean_products(client, env, dry_run)


if __name__ == "__main__":
    args = docopt(__doc__)
    client = ApigeeClient(args["<apigee_org>"], access_token=args["--access-token"])
    clean_env(
        client,
        args["<apigee_env>"],
        should_clean_specs=args["--specs"],
        should_clean_proxies=args["--proxies"],
        should_clean_products=args["--products"],
        sandboxes_only=args["--sandbox-only"],
        dry_run=args["--dry-run"],
        min_age=args["--min-age"],
        undeploy_only=args["--undeploy-only"]
    )
