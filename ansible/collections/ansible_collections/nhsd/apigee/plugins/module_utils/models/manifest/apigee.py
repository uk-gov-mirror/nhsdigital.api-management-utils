import typing

import pydantic

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.apigee_environment import ManifestApigeeEnvironment


class ManifestApigee(pydantic.BaseModel):
    environments: typing.List[ManifestApigeeEnvironment]
