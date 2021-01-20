import typing
import pydantic


class ManifestMetaApi(pydantic.BaseModel):
    name: pydantic.constr(regex=r"^[a-z]+(-[a-z]+)*$")
    id: pydantic.UUID4


class ManifestMeta(pydantic.BaseModel):
    schema_version: pydantic.constr(regex=r"[0-9]+(\.[0-9]+){0,2}")
    api: ManifestMetaApi

    @pydantic.validator("schema_version")
    def validate_schema_version(cls, schema_version):
        semantic_parts = schema_version.split(".")
        major = int(semantic_parts[0])
        minor = 0 if len(semantic_parts) < 2 else int(semantic_parts[1])
        patch = 0 if len(semantic_parts) < 3 else int(semantic_parts[2])

        if major != 1:
            raise ValueError(f"Invalid major version {major} for schema_version")
        if minor != 0:
            raise ValueError(f"Invalid minor version {minor} for major schema_version {major}")
        if patch != 0:
            raise ValueError(f"Invalid patch version {patch} for major/minor schema_version {major}.{minor}")

        return schema_version
