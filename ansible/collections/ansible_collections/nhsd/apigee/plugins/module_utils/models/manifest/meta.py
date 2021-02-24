import pydantic
import typing


from ansible_collections.nhsd.apigee.plugins.module_utils import constants

SCHEMA_VERSION = "1.1.0"



class ManifestMetaApi(pydantic.BaseModel):
    name: pydantic.constr(regex=r"^[a-z]+(-[a-z]+)*$")
    id: typing.Optional[pydantic.UUID4] = pydantic.Field(
        None, description="This field is deprecated, use guid instead."
    )
    guid: pydantic.UUID4 = None
    spec_guids: typing.Optional[typing.Set[pydantic.UUID4]] = None

    def dict(self, **kwargs):
        native = super().dict(**kwargs)
        spec_guids = native.get("spec_guids")
        if spec_guids is None:
            spec_guids = []
        if "id" in native:  # Deprecated, do not export
            native.pop("id")
        native.update(
            {
                "guid": str(native["guid"]),
                "spec_guids": [str(guid) for guid in spec_guids],
             }
        )
        return native

    @pydantic.validator("guid", pre=True, always=True)
    def id_to_guid(cls, guid, values):
        _id = values.get("id")
        if _id and not guid:
            return _id
        return guid

    @pydantic.root_validator
    def validate_meta_api(cls, values):
        supplied_guid = str(values.get("guid"))

        try:
            registered_meta = next(
                filter(lambda meta: meta["guid"] == supplied_guid, constants.REGISTERED_META)
            )
        except StopIteration:
            raise ValueError(
                f"Supplied meta.api.guid: '{supplied_guid}' does not match any registered API guid."
            )

        registered_name = registered_meta["name"]
        supplied_name = values.get("name")
        if supplied_name != registered_name:
            raise ValueError(
                f"Supplied meta.api.name '{supplied_name}' does not match registered name {registered_name} for API guid {supplied_guid}."
            )

        supplied_spec_guids = values.get("spec_guids")
        if supplied_spec_guids is None:  # For backwards compatibility
            return values

        registered_spec_guids = registered_meta["spec_guids"]
        for supplied_spec_guid in supplied_spec_guids:
            if str(supplied_spec_guid) not in registered_spec_guids:
                raise ValueError(
                    f"Supplied meta.api.spec_guids entry '{supplied_spec_guid}' is not in list of registered spec_guids {registered_spec_guids} for API guid '{supplied_guid}'"
                )

        return values


class ManifestMeta(pydantic.BaseModel):
    schema_version: pydantic.constr(regex=r"[1-9][0-9]*(\.[0-9]+){0,2}")
    api: ManifestMetaApi

    @pydantic.validator("schema_version")
    def validate_schema_version(cls, schema_version):
        semantic_parts = schema_version.split(".")

        MAJOR, MINOR, PATCH = [int(x) for x in SCHEMA_VERSION.split(".")]
        major = int(semantic_parts[0])

        # Checking against minor/patch would not allow to us deploy
        # older versions of the manifest, which would be bad.
        if major != MAJOR:
            raise ValueError(
                f"Current schema version is {SCHEMA_VERSION}. "
                + "All minor and patch changes are backwards compatible."
            )

        return schema_version
