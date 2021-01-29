import pydantic

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.apigee import (
    ManifestApigee,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.meta import (
    ManifestMeta,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.models.apigee.product import (
    ApigeeProductAttributeApiSpecGuid,
    ApigeeProductAttributeApiGuid,
)


def get_attrs(product, cls):
    return [
        attr
        for attr in product.attributes
        if isinstance(attr, cls)
    ]


class Manifest(pydantic.BaseModel):
    apigee: ManifestApigee
    meta: ManifestMeta

    @pydantic.validator("meta")
    def validate_apigee_spec_guids(cls, meta, values):
        apigee = values.get("apigee")
        # we have other issues
        if not apigee:
            return meta

        for env in apigee.environments:
            for product in env.products:
                guid_attrs = get_attrs(product, ApigeeProductAttributeApiGuid)
                if len(guid_attrs) > 1 or (
                    len(guid_attrs) == 1 and guid_attrs[0].value != meta.api.guid
                ):
                    raise AssertionError(
                        f"product '{product.name}' attributes must "
                        + f"contain api_guid = '{meta.api.guid}'"
                    )
                elif len(guid_attrs) == 0:
                    product.attributes.append(
                        ApigeeProductAttributeApiGuid(
                            name="api_guid",
                            value=meta.api.guid
                        )
                    )

                # Check spec_guids match meta block
                spec_guid_attrs = get_attrs(product, ApigeeProductAttributeApiSpecGuid)
                if meta.api.spec_guids is None and len(spec_guid_attrs) != 0:
                    msg = (
                        f"product {product.name} has a spec_guid "
                        + "attribute when spec_guids are not defined "
                        + "in meta.api block"
                    )
                    raise AssertionError(msg)
                elif meta.api.spec_guids is not None:
                    if len(spec_guid_attrs) != 1:
                        msg = (
                            f"product {product.name} requires "
                            + "unique attribute spec_guid"
                        )
                        raise AssertionError(msg)
                    elif spec_guid_attrs[0].value not in meta.api.spec_guids:
                        msg = (
                            f"product {product.name} attribute spec_guid must "
                            + "match one of meta.api.spec_guids= "
                            + f"{[str(g) for g in meta.api.spec_guids]}, "
                            + "supplied value is {spec_guid_attrs[0].value}"
                        )
                        raise AssertionError(msg)

        return meta
