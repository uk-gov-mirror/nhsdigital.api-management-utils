"""
spec_uploader.py

A tool for uploading apigee specs

Usage:
  spec_uploader.py <apigee_org> --spec-file=<spec_file> --access-token=<apigee_token> [--friendly-name=<friendly_name>] [--pull-request]
  spec_uploader.py (-h | --help)

Options:
  -h --help                        Show this screen
  --access-token=<access_token>    Access Token from apigee
  --spec-file=<spec_file>          Path to specification file
  --friendly-name=<friendly_name>  Friendly (displayable) name for this API
  --pull-request                   Set if Deploying a Pull Request
"""
import os
from typing import List
from glob import glob
from docopt import docopt
from apigee_client import ApigeeClient


# A list of envs that we want to create but not publish specs or products for at all.
PORTAL_BLACKLIST = ["dev"]

# A list of services not to create portal entries for
SERVICE_BLACKLIST = ["identity-service"]

# Map of org name to envs in that org
ENV_NAMES = {
    "pull-request": ["internal-dev"],
    "nhsd-prod": ["sandbox", "dev", "int", "prod"],
    "nhsd-nonprod": ["internal-dev", "internal-qa-sandbox", "internal-qa", "ref"],
}

# Human-readable env names
FRIENDLY_ENV_NAMES = {
    "prod": "(Production)",
    "int": "(Integration Testing)",
    "dev": "(Development)",
    "ref": "(Reference)",
    "internal-qa": "(Internal QA)",
    "internal-dev": "(Internal Development)",
}

# Mapping of services to require callbacks on
# TODO: this is horrible. Let's get this into terraform ASAP.
CALLBACK_REQUIRED = {
    "personal-demographics": True,
    "identity-service": True,
    "hello-world": True,
    "covid-19-testing-channel-availability": False,
}


def to_friendly_name(spec_name: str, env: str, friendly_name: str = None):
    friendly_env = FRIENDLY_ENV_NAMES.get(env, env)

    friendly_api = friendly_name
    if not friendly_api:
        friendly_api = FRIENDLY_ENV_NAMES.get(
            spec_name, spec_name.replace("-", " ").title()
        )

    return f"{friendly_api} {friendly_env}"


def upload_specs(
    envs: List[str], spec_path: str, client: ApigeeClient, friendly_name: str = None, is_pr: bool = False
):
    if "*" in spec_path:
        spec_files = glob(spec_path, recursive=True)

        if not spec_files:
            raise RuntimeError(f"Could not find any files with glob {spec_path}")

        if len(spec_files) > 1:
            raise RuntimeError(
                f"Found too many spec files for {spec_path}: {spec_files}"
            )

        spec_path = spec_files[0]

    # Grab a list of remote specs
    folder = client.list_specs()
    folder_id = folder["id"]
    existing_specs = {v["name"]: v["id"] for v in folder["contents"]}

    # Figure out where the portal is
    portal_id = client.get_portals().json()["data"][0]["id"]
    print(f"portal is {portal_id}")
    portal_specs = {
        i["specId"]: i for i in client.get_apidocs(portal_id).json()["data"]
    }
    print(f"grabbed apidocs")

    spec_name = os.path.splitext(os.path.basename(spec_path))[0]

    if spec_name in existing_specs:
        print(f"{spec_name} exists")
        spec_id = existing_specs[spec_name]
    else:
        print(f"{spec_name} does not exist, creating")
        response = client.create_spec(spec_name, folder_id)
        spec_id = response.json()["id"]

    print(f"{spec_name} id is {spec_id}")

    with open(spec_path, "r") as f:
        response = client.update_spec(spec_id, f.read())
        print(f"{spec_name} updated")

    # Skip blacklisted services, e.g. identity service that do not need a portal entry
    if spec_name not in SERVICE_BLACKLIST:
        # For this, sometimes the product refs change between deploys: instead of updating, delete the old one and recreate.
        for env in envs:
            if env in PORTAL_BLACKLIST:  # we don't want to publish in blacklisted envs
                continue
            if "sandbox" in env:  # we don't want to publish stuff for sandbox
                continue
            print(f"checking if this spec is on the portal in {env}")
            ns_spec_name = spec_name if is_pr else f"{spec_name}-{env}"
            if ns_spec_name in portal_specs:
                print(f"{ns_spec_name} is on the portal, updating")
                apidoc_id = portal_specs[ns_spec_name]["id"]
                client.update_portal_api(
                    apidoc_id,
                    to_friendly_name(spec_name, env, friendly_name),
                    ns_spec_name,
                    spec_id,
                    portal_id,
                    True,
                    CALLBACK_REQUIRED.get(spec_name, False),
                )
                client.update_spec_snapshot(portal_id, apidoc_id)
            else:
                print(f"{ns_spec_name} is not on the portal, adding it")
                client.create_portal_api(
                    to_friendly_name(spec_name, env, friendly_name),
                    ns_spec_name,
                    spec_id,
                    portal_id,
                    True,
                    CALLBACK_REQUIRED.get(spec_name, False),
                )
    print("done.")


if __name__ == "__main__":
    args = docopt(__doc__)
    client = ApigeeClient(args["<apigee_org>"], access_token=args["--access-token"])
    env_names = ENV_NAMES["pull-request"] if args["--pull-request"] else ENV_NAMES[args["<apigee_org>"]]
    upload_specs(
        env_names,
        args["--spec-file"],
        client,
        friendly_name=args["--friendly-name"],
        is_pr=args["--pull-request"]
    )
