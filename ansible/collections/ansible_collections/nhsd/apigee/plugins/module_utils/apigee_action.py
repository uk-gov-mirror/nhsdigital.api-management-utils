import json
import ansible
import pydantic
import deepdiff
import requests


class ApigeeAction(ansible.plugins.action.ActionBase):
    def validate_args(self, Validator: pydantic.BaseModel):
        """
        Returns two-length tuple of validated_args and errors dicts.
        """
        try:
            args = Validator(**self._task.args)
        except pydantic.ValidationError as e:
            return (
                None,
                {
                    "failed": True,
                    "message": f"Bad arguments to {self._task.action} in '{self._task.name}'",
                    "args": self._task.args,
                    "validation error": json.loads(e.json()),
                },
            )

        return args, {}

    def delta(self, before, after, keys_to_ignore=None):
        if not keys_to_ignore:
            keys_to_ignore = []
        return json.loads(
            deepdiff.DeepDiff(
                before,
                after,
                ignore_order=True,
                ignore_type_in_groups=[
                    (ansible.utils.unsafe_proxy.AnsibleUnsafeText, str)
                ],
                exclude_paths=[f"root['{key}']" for key in keys_to_ignore],
            ).to_json()
        )

    def request(
        self, method, url, access_token, json=None, headers=None, status_code=None
    ):

        if not status_code:
            status_code = [200]

        if not headers:
            headers = {}

        headers["authorization"] = f"Bearer {access_token}"

        response = requests.request(method, url, json=json, headers=headers)

        response_dict = {
            "response": {
                "status_code": response.status_code,
                "reason": response.reason,
            },
            "allowed_status_codes": status_code,
        }

        if response.status_code not in status_code:
            response_dict["failed"] = True

        content = response.content.decode()
        if len(content) == 0:
            response_dict["response"]["body"] = content
        else:
            try:
                response_dict["response"]["body"] = response.json()

            except json.decoder.JSONDecodeError:
                response_dict["failed"] = True
                response_dict["response"]["body"] = content

        if response_dict.get("failed"):
            response_dict["msg"] = f"Unexpected response from {method} {url}"

        return response_dict

    def get(self, url, access_token, **kwargs):
        return self.request("GET", url, access_token, **kwargs)

    def post(self, url, access_token, **kwargs):
        return self.request("POST", url, access_token, **kwargs)

    def put(self, url, access_token, **kwargs):
        return self.request("PUT", url, access_token, **kwargs)
