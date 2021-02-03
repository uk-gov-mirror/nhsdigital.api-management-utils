import os
import requests
import time
import sys
import json

AZURE_TOKEN = os.environ["AZURE_TOKEN"]
AUTH = requests.auth.HTTPBasicAuth("", AZURE_TOKEN)
BRANCH_NAME = os.environ["BRANCH_NAME"]
NOTIFY_COMMIT_SHA = os.environ["NOTIFY_COMMIT_SHA"]
NOTIFY_GITHUB_REPOSITORY = "NHSDigital/api-management-utils"
BASE_URL = "https://dev.azure.com/NHSD-APIM/API Platform/_apis/pipelines"
PARAMS = {"api-version": "6.0-preview.1"}
WAIT_TIME_SECONDS = 60
VERBOSE = True


def print_response(response: requests.Response, note: str) -> None:
    if VERBOSE:
        print(note)
        try:
            print(json.dumps(response.json(), indent=2))
        except json.decoder.JSONDecodeError:
            print(response.content.decode())


def run_pipeline(pipeline_id: int, wait_for_completion: bool = False) -> int:

    run_url = BASE_URL + f"/{pipeline_id}/runs"
    body = {
        "resources": {
            "repositories": {
                "common": {
                    "repository": {
                        "fullName": "NHSDigital/api-management-utils",
                        "type": "gitHub",
                    },
                    "refName": f"refs/heads/{BRANCH_NAME}",
                },
                "self": {"refName": "refs/heads/master"},
            }
        },
        "variables": {
            "NOTIFY_GITHUB_REPOSITORY": {
                "isSecret  ": False,
                "value": f"{NOTIFY_GITHUB_REPOSITORY}",
            },
            "NOTIFY_COMMIT_SHA": {"isSecret  ": False, "value": f"{NOTIFY_COMMIT_SHA}"},
        },
    }

    response = requests.post(run_url, auth=AUTH, params=PARAMS, json=body)
    print_response(response, f"Initial request to {run_url}")

    if wait_for_completion and response.status_code == 200:
        delay = 0
        state_url = response.json()["_links"]["self"]["href"]
        while response.status_code == 200 and response.json()["state"] == "inProgress":
            time.sleep(WAIT_TIME_SECONDS)
            delay = delay + WAIT_TIME_SECONDS
            response = requests.get(state_url, auth=AUTH, params=PARAMS)
            print_response(response, f"Response from {state_url} after {delay} seconds")

    return response.status_code


def main():
    build_status = run_pipeline(27, True)
    if build_status != 200:
        sys.exit(1)
    pr_status = run_pipeline(54, True)
    if pr_status != 200:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
