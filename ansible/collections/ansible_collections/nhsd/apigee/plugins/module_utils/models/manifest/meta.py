import pydantic

SCHEMA_VERSION = "1.0.0"


class ManifestMetaApi(pydantic.BaseModel):
    name: pydantic.constr(regex=r"^[a-z]+(-[a-z]+)*$")
    id: pydantic.UUID4

    def dict(self, **kwargs):
        native = super().dict(**kwargs)
        native.update({"id": str(native["id"])})
        return native


class ManifestMeta(pydantic.BaseModel):
    schema_version: pydantic.constr(regex=r"[0-9]+(\.[0-9]+){0,2}")
    api: ManifestMetaApi

    @pydantic.validator("schema_version")
    def validate_schema_version(cls, schema_version):
        semantic_parts = schema_version.split(".")

        MAJOR, MINOR, PATCH = [int(x) for x in SCHEMA_VERSION.split(".")]
        major = int(semantic_parts[0])
        # minor = int(MAJOR) if len(semantic_parts) < 2 else int(semantic_parts[1])
        # patch = int(PATCH) if len(semantic_parts) < 3 else int(semantic_parts[2])

        if major != MAJOR:
            raise ValueError(
                f"Current schema version is {SCHEMA_VERSION}. All minor and patch changes are backwards compatible."
            )

        return schema_version
