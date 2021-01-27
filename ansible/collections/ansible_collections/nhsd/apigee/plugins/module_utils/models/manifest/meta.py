import pydantic
import typing

SCHEMA_VERSION = "1.1.0"


class ManifestMetaApi(pydantic.BaseModel):
    name: pydantic.constr(regex=r"^[a-z]+(-[a-z]+)*$")
    id: pydantic.UUID4
    spec_guids: typing.Optional[typing.List[pydantic.UUID4]] = None

    def dict(self, **kwargs):
        native = super().dict(**kwargs)
        spec_guids = native.get("spec_guids")
        if spec_guids is None:
            spec_guids = []
        native.update(
            {
                "id": str(native["id"]),
                "spec_guids": [str(_id) for _id in spec_guids],
            }
        )
        return native

    @pydantic.validator("spec_guids")
    def validate_spec_guids(cls, spec_guids):
        if len(spec_guids) != len(set(spec_guids)):
            raise ValueError("All spec_guids must be unique.")
        return spec_guids


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
                f"Current schema version is {SCHEMA_VERSION}. All minor and patch changes are backwards compatible."
            )

        return schema_version
