import typing
import pydantic
from ansible_collections.nhsd.apigee.plugins.module_utils.models.apigee.apidoc import (
    ApigeeApidoc,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.models.apigee.spec import (
    ApigeeSpec,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.models.apigee.product import (
    ApigeeProduct,
)


class ManifestApigeeEnvironment(pydantic.BaseModel):
    name: typing.Literal[
        "internal-dev",
        "internal-dev-sandbox",
        "internal-qa",
        "internal-qa-sandbox",
        "ref",
        "dev",
        "sandbox",
        "int",
        "prod",
    ]
    products: typing.List[ApigeeProduct]
    specs: typing.List[ApigeeSpec]
    portals: typing.List[ApigeeApidoc]

    @pydantic.validator("products", "specs")
    def names_unique(cls, values):
        names = [v.name for v in values]
        if len(names) != len(set(names)):
            raise ValueError("Names are not unique")
        return values

    @pydantic.validator("portals")
    def portal_references(cls, apidocs, values):
        spec_names = [spec.name for spec in values.get("specs", [])]
        product_names = [product.name for product in values.get("products", [])]

        for apidoc in apidocs:
            if apidoc.edgeAPIProductName not in product_names:
                raise ValueError(
                    f"edgeAPIProductName {apidoc.edgeAPIProductName} not in list of products in this environment"
                )
            if apidoc.specId and apidoc.specId not in spec_names:
                raise ValueError(
                    f"specId {apidoc.specId} not in list of specs in this environment"
                )
        return apidocs
