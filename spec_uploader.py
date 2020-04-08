"""
spec_uploader.py

A tool for uploading apigee specs

Usage:
  spec_uploader.py <apigee_org> --spec-file=<spec_file> --access-token=<apigee_token> [--friendly-name=<friendly_name>]
  spec_uploader.py (-h | --help)

Options:
  -h --help        Show this screen
  --access-token   Access Token from apigee
  --spec-file      Path to specification file
  --friendly-name  Friendly (displayable) name for this API
"""
import os
from docopt import docopt
from apigee_client import ApigeeClient


ENV_NAMES = {
    'nhsd-prod': ['sandbox', 'dev', 'int', 'prod'],
    'nhsd-nonprod': ['internal-dev', 'internal-qa-sandbox', 'internal-qa', 'ref']
}


FRIENDLY_ENV_NAMES = {
    'prod': '(Production)',
    'int': '(Integration Testing)',
    'dev': '(Development)',
    'ref': '(Reference)',
    'internal-qa': '(Internal QA)',
    'internal-dev': '(Internal Development)'
}


def to_friendly_name(spec_name, env, friendly_name=None):
    friendly_env = FRIENDLY_ENV_NAMES.get(env, env)

    friendly_api = friendly_name
    if not friendly_api:
        friendly_api = FRIENDLY_ENV_NAMES.get(spec_name, spec_name.replace('-', ' ').title())

    return f'{friendly_api} {friendly_env}'


def upload_specs(envs, spec, client, friendly_name=None):
    # Grab a list of remote specs
    folder = client.list_specs()
    folder_id = folder['id']
    existing_specs = {v['name']: v['id'] for v in folder['contents']}

    # Figure out where the portal is
    portal_id = client.get_portals().json()['data'][0]['id']
    print(f'portal is {portal_id}')
    portal_specs = {i['specId']: i for i in client.get_apidocs(portal_id).json()['data']}
    print(f'grabbed apidocs')

    spec_name = os.path.splitext(spec)[0]

    if spec_name in existing_specs:
        print(f'{spec} exists')
        spec_id = existing_specs[spec_name]
    else:
        print(f'{spec} does not exist, creating')
        response = client.create_spec(spec_name, folder_id)
        spec_id = response.json()['id']

    print(f'{spec} id is {spec_id}')

    with open(os.path.join(specs_dir, spec), 'r') as f:
        response = client.update_spec(spec_id, f.read())
        print(f'{spec} updated')

    # For this, sometimes the product refs change between deploys: instead of updating, delete the old one and recreate.
    for env in envs:
        if 'sandbox' in env: # we don't want to publish stuff for sandbox
            continue
        print(f'checking if this spec is on the portal in {env}')
        ns_spec_name = f'{spec_name}-{env}'
        if ns_spec_name in portal_specs:
            print(f'{ns_spec_name} is on the portal, updating')
            apidoc_id = portal_specs[ns_spec_name]['id']
            client.update_portal_api(
                apidoc_id,
                to_friendly_name(spec_name, env, friendly_name),
                ns_spec_name,
                spec_id,
                portal_id
            )
            client.update_spec_snapshot(portal_id, apidoc_id)
        else:
            print(f'{ns_spec_name} is not on the portal, adding it')
            client.create_portal_api(
                to_friendly_name(spec_name, env, friendly_name),
                ns_spec_name,
                spec_id,
                portal_id
            )

    print('done.')


if __name__ == "__main__":
    args = docopt(__doc__)
    client = ApigeeClient(args['<apigee_org>'], access_token=args['<access_token>'])
    upload_specs(ENV_NAMES[args['<apigee_org>']], args['<spec_file>'], client, friendly_name=args['<friendly_name>'])
