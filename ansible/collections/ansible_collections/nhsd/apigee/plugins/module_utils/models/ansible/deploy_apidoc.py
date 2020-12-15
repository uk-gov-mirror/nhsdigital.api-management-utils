import pydantic
from ansible_collections.nhsd.apigee.plugins.module_utils.models.apigee.apidoc import ApigeeApidoc


class DeployApidoc(pydantic.BaseModel):
    portal: ApigeeApidoc
    organization: str
    access_token: str
