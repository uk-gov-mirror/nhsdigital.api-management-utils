import requests
import json
import bisect
import copy

from ansible_collections.nhsd.apigee.plugins.module_utils.models.ansible.add_jwks_resource_url import (
    AddJwksResourceUrlToApp,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.apigee_action import (
    ApigeeAction,
)
from ansible_collections.nhsd.apigee.plugins.module_utils import utils
from ansible_collections.nhsd.apigee.plugins.module_utils import constants

ATTRIBUTE_NAME = "jwks-resource-url"


class LazyDeveloperDetails:
    """
    Gets a list of all developers for an apigee organization.  Lazily
    looks up details based on __getitem__ access.  Since Apigee
    returns the entire list developers sorted by their internal
    'developerId' attribute, this allows us to quickly binary search
    our way to a developer's details when we only know their
    developerId.
    """

    def __init__(self, org, token):
        self._base_url = constants.APIGEE_BASE_URL + f"organizations/{org}/developers/"
        self._token = token
        self._session = requests.Session()

        self.emails = self._get("")
        self.details = [None for email in self.emails]

    def _get(self, email: str):
        """
        Get developer details from email.
        Get all developers if email = ''

        Raises a RuntimeError if the request does not return 200.
        This allows us to bubble the exception up to an ansible
        response.
        """
        resp = utils.get(self._base_url + email, self._token, session=self._session)
        if resp.get("failed"):
            raise RuntimeError(json.dumps(resp))
        return resp["response"]["body"]

    def __getitem__(self, i: int):
        if self.details[i] is None:
            self.details[i] = self._get(self.emails[i])
        return self.details[i]["developerId"]

    def __len__(self):
        return len(self.emails)


class ActionModule(ApigeeAction):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        args, errors = self.validate_args(AddJwksResourceUrlToApp)
        if errors:
            return errors

        diff_mode = self._play_context.diff
        check_mode = self._play_context.check_mode

        before = args._app_data
        after = copy.deepcopy(before)

        jwks_attribute = {"name": ATTRIBUTE_NAME, "value": str(args.jwks_resource_url)}

        # Delete any existing jwks attributes, for now there can only be one.
        after["attributes"] = [
            attr for attr in after["attributes"] if attr["name"] != ATTRIBUTE_NAME
        ]
        # Append the desired jwks attributes and sort
        after["attributes"].append(jwks_attribute)
        after["attributes"] = sorted(after["attributes"], key=lambda attr: attr["name"])

        developer_details = LazyDeveloperDetails(args.organization, args.access_token)
        try:
            i = bisect.bisect_left(developer_details, args._app_data["developerId"])
        except RuntimeError as e:
            return json.loads(str(e))
        developer = developer_details.details[i]

        delta = utils.delta(before, after)
        result = {"changed": bool(delta), "app": after, "developer": developer}
        app_name = args._app_data["name"]
        app_path = f"organizations/{args.organization}/developers/{developer['email']}/apps/{app_name}/attributes"

        if diff_mode:
            result["diff"] = [
                {
                    "before": before,
                    "before_header": app_path,
                    "after": after,
                    "after_header": app_path,
                }
            ]

        if check_mode:
            return result

        app_attribute_url = constants.APIGEE_BASE_URL + app_path

        app_data2 = utils.post(
            app_attribute_url,
            args.access_token,
            json={"attribute": after["attributes"]},
        )
        if app_data2.get("failed"):
            return app_data2

        app_url = (
            constants.APIGEE_BASE_URL
            + f"organizations/{args.organization}/apps/{args.app_id}"
        )
        updated_app_response = utils.get(app_url, args.access_token)
        if updated_app_response.get("failed"):
            return updated_app_response

        after = updated_app_response["response"]["body"]
        if diff_mode:
            result["diff"][-1]["after"] = after

        result["app"] = after
        return result
