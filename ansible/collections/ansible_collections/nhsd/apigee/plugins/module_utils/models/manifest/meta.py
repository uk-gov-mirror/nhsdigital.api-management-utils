import pydantic


class ManifestMetaApi(pydantic.BaseModel):
    name: pydantic.constr(regex=r"^[a-z]+(-[a-z]+)*$")
    id: pydantic.UUID4


class ManifestMeta(pydantic.BaseModel):
    version: pydantic.constr(regex=r"[0-9]+")
    api: ManifestMetaApi

    @pydantic.validator("version")
    def validate_version(cls, version):
        if version != "0":
            raise ValueError("Currently only version 0 is supported.")
        return version
