import pydantic

from ansible_collections.nhsd.apigee.plugins.module_utils.models.manifest.apigee_manifest import ApigeeManifest


class ApplyPullRequestNamespace(pydantic.BaseModel):
    """
    This Model applies our pull-request namespacing for pipeline
    deployment.

    Once the object has been initialized it contains all the data
    needed for a pull-request deployment of what is in the manifest
    file.

    The validator:

        1. Removes all environments other than 'internal-dev' and
           'interal-dev-sandbox'

        2. Replaces all instances of 'internal-dev' with
           :param:`pull_request` in the name-like fields of the
           :class:`ApigeeApidoc`, :class:`ApigeeProduct`, and
           :class:`ApigeeSpec` objects.

    :param pull_request: A string like 'pr-1234' for pull request
        number 1234.
    :param service_name: The 'service-name' item your manifest.yml.
    :param apigee: The 'apigee' item from your manifest.yml
    """

    pull_request: pydantic.constr(regex=r"^pr-[0-9]+$")  # i.e. 'pr-1234'
    service_name: str
    apigee: ApigeeManifest

    @pydantic.validator("apigee")
    def apply_namespace(cls, apigee, values):
        service_name = values.get("service_name")

        apigee.environments = [
            env for env in apigee.environments if env.name.startswith("internal-dev")
        ]

        # here we want:
        # my-service-internal-dev         -> my-service-pr-1234
        # my-service-internal-dev-sandbox -> my-service-pr-1234-sandbox
        old = "internal-dev"
        new = values["pull_request"]
        for env in apigee.environments:
            for product in env.products:
                product.name = product.name.replace(old, new, 1)
                product.proxies = [
                    proxy.replace(old, new, 1)
                    if proxy.startswith(service_name)
                    else proxy
                    for proxy in product.proxies
                ]

            for spec in env.specs:
                spec.name = spec.name.replace(old, new, 1)
            for portal in env.portals:
                portal.edgeAPIProductName = portal.edgeAPIProductName.replace(
                    old, new, 1
                )
                portal.specId = portal.specId.replace(old, new, 1)

        return apigee
