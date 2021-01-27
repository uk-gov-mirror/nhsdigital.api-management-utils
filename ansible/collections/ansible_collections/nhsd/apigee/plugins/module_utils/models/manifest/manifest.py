import pydantic

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.apigee import ManifestApigee
from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.meta import ManifestMeta


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
                spec_guid_attrs = [attr for attr in product.attributes if attr.name == "spec_guid"]
                if meta.api.spec_guids is None and len(spec_guid_attrs) != 0:
                    raise AssertionError(
                        f"product {product.name} has a spec_guid attribute when spec_guids are not defined in meta.api block"
                    )
                elif meta.api.spec_guids is not None:
                    if len(spec_guid_attrs) != 1:
                        raise AssertionError(
                            f"product {product.name} requires unique attribute spec_guid"
                        )
                    elif spec_guid_attrs[0].value not in meta.api.spec_guids:
                        raise AssertionError(f"product {product.name} attribute spec_guid must match one of meta.api.spec_guids= {[str(g) for g in meta.api.spec_guids]}, supplied value is {spec_guid_attrs[0].value}")
        return meta
