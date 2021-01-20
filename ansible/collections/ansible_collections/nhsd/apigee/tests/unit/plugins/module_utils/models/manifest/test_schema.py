import os
import json
import pathlib
import yaml
import re

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.manifest import (
    Manifest,
    SCHEMA_VERSION,
)


DIR = pathlib.Path(__file__).parent.absolute()

MAJOR, MINOR, PATCH = [int(x) for x in SCHEMA_VERSION.split(".")]


def test_schema_version():
    """
    Check that the current version of the schema matches the snapshot
    made at the last version change.
    """

    live_schema = Manifest.schema()
    with open(str(DIR) + f'/schema_versions/v{SCHEMA_VERSION}.json') as f:
        recorded_schema = json.load(f)
    assert live_schema == recorded_schema


def test_all_example_schemas_can_be_loaded(tmp_path):
    """
    Validate all example manifests on the current major version of the
    SCHEMA_VERSION
    """

    # Setup a tmpdir containing dummy spec files as their existance is validated.
    for spec_name in ["personal-demographics.json", "canary-api.json"]:
        file_name = str(tmp_path) + f"/{spec_name}"
        with open(file_name, "w") as f:
            f.write("{}")
    os.chdir(tmp_path)

    # i.e. something like: pds-v1.2.3.yml
    version_pattern = re.compile(r"v([0-9]+)\.([0-9]+)\.([0-9]+)\.yml$")
    for path in DIR.glob("test_manifests/*"):
        match = re.search(version_pattern, path.name)
        if match:
            major, minor, patch = [int(match.group(x)) for x in range(1, 4)]
            # If same major version and ahead all patches...
            if MAJOR == major and MINOR >= minor and PATCH >= patch:
                with open(str(path)) as f:
                    manifest = yaml.load(f, yaml.SafeLoader)
                    # Will error if schema invalid
                    Manifest(**manifest, dist_dir=str(tmp_path))
