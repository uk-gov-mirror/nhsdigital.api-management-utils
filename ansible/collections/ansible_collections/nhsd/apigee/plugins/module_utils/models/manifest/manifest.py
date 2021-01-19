import pydantic

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.apigee import ManifestApigee
from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.meta import ManifestMeta


class Manifest(pydantic.BaseModel):
    apigee: ManifestApigee
    meta: ManifestMeta
