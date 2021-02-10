import os
import json
import time
import requests


class AzureDevOps:

    def __init__(self):
        self.base_url = "https://dev.azure.com/NHSD-APIM/API Platform/_apis/pipelines"
        self.token = os.environ["AZURE_TOKEN"]
        self.auth = requests.auth.HTTPBasicAuth("", self.token)
        self.notify_commit_sha = os.environ["NOTIFY_COMMIT_SHA"]
        self.utils_pr_number = os.environ["UTILS_PR_NUMBER"]
        self.notify_github_repo = "NHSDigital/api-management-utils"
        self.api_params = {"api-version": "6.0-preview.1"}
        self.api_request_delay = 60

    @staticmethod
    def print_response(response: requests.Response, note: str, verbose: bool = True) -> None:
        if verbose:
            print(note)
            try:
                print(json.dumps(response.json(), indent=2))
            except json.decoder.JSONDecodeError:
                print(response.content.decode())

    def run_pipeline(self,
                     service: str,
                     pipeline_type: str,
                     pipeline_id: int,
                     pipeline_branch: str,
                     wait_for_completion: bool = False,
                     is_release: bool = False) -> int:

        run_url = self.base_url + f"/{pipeline_id}/runs"
        body = {
            "resources": {
                "repositories": {
                    "common": {
                        "repository": {
                            "fullName": "NHSDigital/api-management-utils",
                            "type": "gitHub",
                        },
                        "refName": f"refs/pull/{self.utils_pr_number}/merge",
                    },
                    "self": {"refName": f"{pipeline_branch}"},
                }
            },
            "variables": {
                "NOTIFY_GITHUB_REPOSITORY": {
                    "isSecret  ": False,
                    "value": f"{self.notify_github_repo}",
                },
                "NOTIFY_COMMIT_SHA": {
                    "isSecret  ": False,
                    "value": f"{self.notify_commit_sha}"
                },
            },
        }

        if not is_release:
            body["variables"]["UTILS_PR_NUMBER"] = {
                "isSecret  ": False,
                "value": f"{self.utils_pr_number}",
            }

        response = requests.post(run_url, auth=self.auth, params=self.api_params, json=body)
        self.print_response(response, f"Initial request to {run_url}")

        result = "failed"
        if wait_for_completion and response.status_code == 200:
            delay = 0
            state_url = response.json()["_links"]["self"]["href"]
            while response.status_code == 200 and response.json()["state"] == "inProgress":
                time.sleep(self.api_request_delay)
                delay = delay + self.api_request_delay
                response = requests.get(state_url, auth=self.auth, params=self.api_params)
                self.print_response(response, f"Response from {state_url} after {delay} seconds")
            result = response.json()["result"]
            print(f"Result of {service} {pipeline_type} pipeline: {result}")
        elif response.status_code == 203 or response.status_code == 401:
            print(f"{response.status_code}: Invalid or expired PAT (Personal Access Token),"
                  f" please verify or renew token")
        else:
            print(f"Triggering pipeline: {service} {pipeline_type} failed, status code: {response.status_code}")
        return result
