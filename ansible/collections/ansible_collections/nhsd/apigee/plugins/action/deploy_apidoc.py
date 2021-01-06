from ansible_collections.nhsd.apigee.plugins.module_utils.apigee_action import (
    ApigeeAction,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.models.ansible.deploy_apidoc import (
    DeployApidoc,
)


class ActionModule(ApigeeAction):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        diff_mode = self._play_context.diff
        check_mode = self._play_context.check_mode
        args, errors = self.validate_args(DeployApidoc)
        if errors:
            return errors

        result = {"changed": False, "ansible_facts": {}}
        apidoc = args.portal

        # This will fail if apigee_apidoc is called before apigee_spec
        # as APIGEE_SPEC_RESOURCES will not exist!
        if apidoc.specId != "":
            spec_resources = [
                spec
                for spec in task_vars["APIGEE_SPEC_RESOURCES"]
                if spec["name"] == apidoc.specId
            ]
            if len(spec_resources) != 1:
                return {
                    "failed": True,
                    "msg": f"Unable to find unique spec resource named {apidoc.specId}",
                    "spec_resources": spec_resources,
                }
            apidoc.specContent = str(spec_resources[0]["id"])  # avoid AnsibleUnsafeText type

        PORTALS_BASE_URL = "https://apigee.com/portals/api/sites"
        if not task_vars.get("APIGEE_PORTAL_ID"):
            portal_id_request = self.get(
                f"{PORTALS_BASE_URL}?orgname={args.organization}",
                args.access_token
            )
            if portal_id_request.get("failed"):
                return portal_id_request

            task_vars["APIGEE_PORTAL_ID"] = portal_id_request["response"]["body"]["data"][0]["id"]
            result["ansible_facts"]["APIGEE_PORTAL_ID"] = task_vars["APIGEE_PORTAL_ID"]

        APIGEE_PORTAL_ID = task_vars["APIGEE_PORTAL_ID"]
        APIGEE_APIDOC_URL = f"{PORTALS_BASE_URL}/{APIGEE_PORTAL_ID}/apidocs"
        # Ensure we have the fact APIGEE_APIDOCS
        if not task_vars.get("APIGEE_APIDOCS"):
            apidocs_request = self.get(APIGEE_APIDOC_URL, args.access_token)
            if apidocs_request.get("failed"):
                return apidocs_request

            task_vars["APIGEE_APIDOCS"] = apidocs_request["response"]["body"]["data"]
            result["ansible_facts"]["APIGEE_APIDOCS"] = task_vars["APIGEE_APIDOCS"]

        existing_apidocs = [
            existing_apidoc
            for existing_apidoc in task_vars["APIGEE_APIDOCS"]
            if existing_apidoc["edgeAPIProductName"] == apidoc.edgeAPIProductName
        ]

        if len(existing_apidocs) > 1:
            return {
                "failed": True,
                "msg": f"Found more than one apidoc with name {apidoc.name}, this should not happen",
                "existing_apidocs": existing_apidocs,
            }

        if len(existing_apidocs) == 0:
            method = "POST"
            url = APIGEE_APIDOC_URL
            current_apidoc = {}
            status_code = [200]
        else:
            current_apidoc = existing_apidocs[0]
            method = "PUT"
            status_code = [200]
            url = APIGEE_APIDOC_URL + f"/{current_apidoc['id']}"

        if apidoc.specId:
            # Look up matching specContent
            specs = task_vars["APIGEE_SPEC_RESOURCES"]
            matching_specs = [spec for spec in specs if spec['name'] == apidoc.specId]
            if len(matching_specs) != 1:
                return {
                    "failed": True,
                    "msg": f"Unable to find spec named {apidoc.specId}, this should not happen"
                }
            apidoc.specContent = matching_specs[0]['id']

        result["apidoc"] = apidoc.dict()

        # ignore apigee filesystem junk
        keys_to_ignore = [
            "apiId",
            "id",
            "categoryIds",
            "enrollment",
            "imageUrl",
            "modified",
            "productExists",
            "siteId",
            "snapshotExists",
            "snapshotModified",
            "snapshotOutdated",
            "snapshotSourceMissing",
            "snapshotState",
            "specModified",
            "specTitle",
        ]

        delta = self.delta(
            current_apidoc,
            result["apidoc"],
            keys_to_ignore=keys_to_ignore,
        )
        result["changed"] = bool(delta)

        if diff_mode:
            result["diff"] = [
                {
                    "before_header": current_apidoc["specId"],
                    "before": self.exclude_keys(current_apidoc, keys_to_ignore),
                    "after_header": apidoc.specId,
                    "after": self.exclude_keys(apidoc.dict(), keys_to_ignore),
                }
            ]

        if not delta or check_mode:
            return result

        apidoc_request = self.request(
            method, url, args.access_token, json=apidoc.dict(), status_code=status_code
        )
        if apidoc_request.get("failed"):
            return apidoc_request

        result["apidoc"] = apidoc_request["response"]["body"]["data"]
        if diff_mode:
            result["diff"][0]["after"] = self.exclude_keys(result["apidoc"], keys_to_ignore)

        return result
