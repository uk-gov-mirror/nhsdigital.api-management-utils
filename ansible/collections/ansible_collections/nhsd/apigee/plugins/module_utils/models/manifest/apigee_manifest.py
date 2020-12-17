import typing

import pydantic

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.apigee_environment import ApigeeEnvironment


class ApigeeManifest(pydantic.BaseModel):
    environments: typing.List[ApigeeEnvironment]
