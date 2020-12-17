import os
import typing

import pydantic

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.apigee_manifest import (
    ApigeeManifest,
)


def correct_namespace(name, service_name, env_name) -> bool:
    """
    Checks that a name in Apigee has the correct namespaceing.

    e.g. for service_name="my-service" and env_name="internal-dev"
    |--------------------------------------------------+--------|
    | name                                             | result |
    |--------------------------------------------------+--------|
    | "my-service-internal-dev"                        | True   |
    | "my-service-with-an-extra-suffix-internal-dev"   | True   |
    | "my-serviceinternal-dev"                         | False  |
    | "my-service-internal-dev-application-restricted" | True   |
    |--------------------------------------------------+--------|

    :param name: The name of a thing in Apigee we wish to check is
        namespaced.
    :param service_name: The service-name item from your
        manifest.ApigeeManifest
    :param env_name: The environment name (e.g. 'internal-dev', 'int')
    """
    if not name.startswith(service_name):
        return False
    remaining_name = name.replace(service_name, "", 1)
    if remaining_name.endswith(f"-{env_name}"):
        return True
    elif f"-{env_name}-" in remaining_name:
        return True
    return False


class ValidateManifest(pydantic.BaseModel):
    service_name: str
    version: pydantic.constr(regex=r"[0-9]+")
    pipeline_service_name: typing.Optional[str] = None
    dist_dir: typing.Optional[pydantic.DirectoryPath] = None
    apigee: ApigeeManifest

    @pydantic.validator("version")
    def validate_version(cls, version):
        if version != "0":
            raise ValueError("Currently only version 0 is supported.")
        return version

    @pydantic.validator("apigee", pre=True)
    def prepend_dist_dir_to_spec_paths(cls, apigee, values):
        dist_dir = values.get("dist_dir")
        if dist_dir:
            for env_dict in apigee["environments"]:
                for spec_dict in env_dict["specs"]:
                    path = spec_dict.get("path")
                    if path is not None:
                        spec_dict["path"] = os.path.join(dist_dir, path)
        return apigee

    @pydantic.validator("pipeline_service_name")
    def check_pipeline_service_name(cls, pipeline_service_name, values):
        manifest_service_name = values.get("service_name", "")
        if (
            pipeline_service_name != manifest_service_name
            and not pipeline_service_name.startswith(manifest_service_name + "-")
        ):
            raise ValueError(
                f"pipeline defined service_name ('{pipeline_service_name}') does not begin with manifest defined service_name: '{manifest_service_name}'"
            )

    @pydantic.validator("apigee")
    def check_namespacing(cls, apigee, values):
        service_name = values.get("service_name")

        for env in apigee.environments:
            if env is None:
                continue
            for product in env.products:
                if not correct_namespace(product.name, service_name, env.name):
                    raise ValueError(
                        f"{product.name} does not conform to namespace {service_name}-*{env.name}"
                    )
            for spec in env.specs:
                if not correct_namespace(spec.name, service_name, env.name):
                    raise ValueError(
                        f"{spec.name} does not conform to namespace for {service_name}-*{env.name}"
                    )
        return apigee
