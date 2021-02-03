import pydantic
from ansible_collections.nhsd.apigee.plugins.module_utils.models.apigee.product import ApigeeProduct


class DeployProduct(pydantic.BaseModel):
    organization: str
    access_token: str
    product: ApigeeProduct
