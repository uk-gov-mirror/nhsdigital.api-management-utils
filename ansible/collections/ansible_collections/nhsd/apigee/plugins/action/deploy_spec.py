from ansible_collections.nhsd.apigee.plugins.module_utils.models.ansible.deploy_spec import (
    DeploySpec,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.apigee_action import (
    ApigeeAction,
)

APIGEE_DAPI_URL = "https://apigee.com/dapi/api/"


class ActionModule(ApigeeAction):
    def run(self, tmp=None, task_vars=None):

        super(ActionModule, self).run(tmp, task_vars)
        args, errors = self.validate_args(DeploySpec)
        if errors:
            return errors

        diff_mode = self._play_context.diff
        check_mode = self._play_context.check_mode

        result = {"changed": False}

        # Ensure we have the facts APIGEE_SPEC_RESOURCES and APIGEE_SPEC_FOLDER_ID
        if not task_vars.get("APIGEE_SPEC_RESOURCES") or not task_vars.get(
            "APIGEE_SPEC_FOLDER_ID"
        ):
            specs_list_uri = (
                APIGEE_DAPI_URL
                + f"/organizations/{args.organization}/specs/folder/home"
            )

            all_specs_response = self.get(specs_list_uri, args.access_token)

            all_specs = all_specs_response["response"]["body"]
            if all_specs.get("failed"):
                return all_specs

            task_vars["APIGEE_SPEC_RESOURCES"] = all_specs["contents"]
            task_vars["APIGEE_SPEC_FOLDER_ID"] = all_specs["id"]

            # Set them as facts for future calls in the same playbook
            result["ansible_facts"] = {
                "APIGEE_SPEC_RESOURCES": task_vars["APIGEE_SPEC_RESOURCES"],
                "APIGEE_SPEC_FOLDER_ID": task_vars["APIGEE_SPEC_FOLDER_ID"],
            }

        existing_resources = [
            existing_resource
            for existing_resource in task_vars["APIGEE_SPEC_RESOURCES"]
            if existing_resource["name"] == args.spec.name
        ]

        if len(existing_resources) > 1:
            return {
                "failed": True,
                "msg": f"Found more than one spec with name {args.spec.name}, this should not happen",
                "existing_resources": existing_resources,
            }

        if len(existing_resources) == 0:
            spec_resource = {
                "folder": task_vars["APIGEE_SPEC_FOLDER_ID"],
                "name": args.spec.name,
                "kind": "Doc",
            }

            response_dict = self.post(
                APIGEE_DAPI_URL + f"organizations/{args.organization}/specs/doc",
                args.access_token,
                json=spec_resource,
            )
            if response_dict.get("failed"):
                return response_dict

            result["changed"] = True

            # Add new spec to locally copy of all spec_resources
            task_vars["APIGEE_SPEC_RESOURCES"].insert(0, spec_resource)
            result["ansible_facts"]["APIGEE_SPEC_RESOURCES"] = task_vars[
                "APIGEE_SPEC_RESOURCES"
            ]
        else:
            spec_resource = existing_resources[0]

        result["spec_resource"] = spec_resource

        # Get current spec content
        spec_content_url = (
            APIGEE_DAPI_URL
            + f"organizations/{args.organization}/specs/doc/{spec_resource['id']}/content"
        )
        current_spec_request = self.get(
            spec_content_url, args.access_token, status_code=[200, 204]
        )  # returns 204 for no content
        if current_spec_request.get("failed"):
            return current_spec_request

        spec_content = current_spec_request["response"]["body"]
        new_spec_content = args.spec.content

        delta = self.delta(spec_content, new_spec_content)

        if diff_mode:
            result["diff"] = {
                "before": spec_content,
                "after": new_spec_content,
                "delta": delta,
            }

        if not delta or check_mode:
            result["spec_content"] = args.spec.content
            return result

        new_spec_content_request = self.put(
            spec_content_url, args.access_token, json=new_spec_content
        )
        if new_spec_content_request.get("failed"):
            return new_spec_content_request
        self.put(spec_content_url + "/snapshot", args.access_token)

        result["changed"] = True
        result["spec_content"] = new_spec_content_request["response"]["body"]

        return result
