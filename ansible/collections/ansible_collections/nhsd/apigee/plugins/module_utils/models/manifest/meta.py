import pydantic
import typing

SCHEMA_VERSION = "1.1.0"

# Maps unique API IDS to API names and Spec guids.  One day this will
# be a proper microservice. But for now, this will do.
REGISTERED_META = [
    {
        "id": "b3d5c83f-98f2-429c-ba1d-646dccd139a3",
        "name": "hello-world",
        "spec_guids": {"e8663c19-725f-4883-b272-a9da868d5541", },
    },
    # {
    #     "id": "a3213966-9b13-400c-8fdd-e239e56a2742",
    #     "name": "mesh-api",
    #     "spec_guids": {"73a3d6dd-912b-4793-bf4c-bf80c4bc34d1", },
    # },
    {
        "id": "eef32850-52ae-46da-9dbd-d9f3df818846",
        "name": "personal-demographics",
        "spec_guids": {"a343a204-f2d2-4287-a2e5-b5cb367e35bb", },
    },
    {
        "id": "9c644a26-c926-4fae-9564-5a9c49ab332d",
        "name": "electronic-prescription-service-api",
        "spec_guids": {"5ead5713-9d2b-46eb-8626-def5fd2a2350", },
    },
    {
        "id": "13cfc3dd-38c3-4692-9cfb-50d540e8cfe3",
        "name": "reasonable-adjustments",
        "spec_guids": {"9f2d5659-ef7d-4815-ac25-d11f4ce75c25", },
    },
    {
        "id": "090e12f4-6f3c-4ea7-b7eb-d70687d22cea",
        "name": "ambulance-analytics",
        "spec_guids": {"538699e8-d039-4473-9e35-e3b79eb92d1e", },
    },
    {
        "id": "fa1c780f-6fb6-4c8e-a73c-eb2c306ca4f1",
        "name": "spine-directory-service",
        "spec_guids": {"88a3ec29-7ab1-4ac4-ae32-e367767b3ed8", },
    },
    {
        "id": "7541eb6b-3416-4aee-bd66-8766c1f90cfb",
        "name": "nhs-app",
        "spec_guids": {"f5b9779e-d343-4a0a-8410-6dcae48bc55e", },
    },
    # {
    #     "id": "b26b0249-488d-44f9-93ed-9d2f08f3859c",
    #     "name": "signing-service-api",
    #     "spec_guids": {"a062e39c-b843-4833-8d24-8fc1434900a0",},
    # },
]


class ManifestMetaApi(pydantic.BaseModel):
    name: pydantic.constr(regex=r"^[a-z]+(-[a-z]+)*$")
    id: pydantic.UUID4
    spec_guids: typing.Optional[typing.Set[pydantic.UUID4]] = None

    def dict(self, **kwargs):
        native = super().dict(**kwargs)
        spec_guids = native.get("spec_guids")
        if spec_guids is None:
            spec_guids = []
        native.update(
            {"id": str(native["id"]), "spec_guids": [str(_id) for _id in spec_guids]}
        )
        return native

    @pydantic.root_validator
    def validate_meta_api(cls, values):
        supplied_id = str(values.get("id"))

        try:
            registered_meta = next(
                filter(lambda meta: meta["id"] == supplied_id, REGISTERED_META)
            )
        except StopIteration:
            raise ValueError(
                f"Supplied meta.api.id: '{supplied_id}' does not match any registered API id."
            )

        registered_name = registered_meta["name"]
        supplied_name = values.get("name")
        if supplied_name != registered_name:
            raise ValueError(
                f"Supplied meta.api.name '{supplied_name}' does not match registered name {registered_name} for API id {supplied_id}."
            )

        supplied_spec_guids = values.get("spec_guids")
        registered_spec_guids = registered_meta["spec_guids"]
        for supplied_spec_guid in supplied_spec_guids:
            if str(supplied_spec_guid) not in registered_spec_guids:
                raise ValueError(
                    f"Supplied meta.api.spec_guids entry '{supplied_spec_guid}' is not in list of registered spec_guids {registered_spec_guids} for API id '{supplied_id}'"
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
                f"Current schema version is {SCHEMA_VERSION}. All minor and patch changes are backwards compatible."
            )

        return schema_version
