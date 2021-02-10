import os
import requests
import time
import sys
import json
from multiprocessing import Process, Manager

AZURE_TOKEN = os.environ["AZURE_TOKEN"]
AUTH = requests.auth.HTTPBasicAuth("", AZURE_TOKEN)
BRANCH_NAME = os.environ["BRANCH_NAME"]
NOTIFY_COMMIT_SHA = os.environ["NOTIFY_COMMIT_SHA"]
UTILS_PR_NUMBER = os.environ["UTILS_PR_NUMBER"]
NOTIFY_GITHUB_REPOSITORY = "NHSDigital/api-management-utils"
BASE_URL = "https://dev.azure.com/NHSD-APIM/API Platform/_apis/pipelines"
PARAMS = {"api-version": "6.0-preview.1"}
WAIT_TIME_SECONDS = 60
VERBOSE = True

PIPELINES = {
    "identity-service": {
        "build": 27,
        "pr": 54,
        "branch": "master"
    },
    "canary-api": {
        "build": 222,
        "pr": 223,
        "branch": "main"
    },
    "personal-demographics-service": {
        "build": 140,
        "pr": 144,
        "branch": "master"
    }
}


def print_response(response: requests.Response, note: str) -> None:
    if VERBOSE:
        print(note)
        try:
            print(json.dumps(response.json(), indent=2))
        except json.decoder.JSONDecodeError:
            print(response.content.decode())


def run_pipeline(service: str,
                 pipeline_type: str,
                 pipeline_id: int,
                 pipeline_branch: str,
                 wait_for_completion: bool = False) -> int:

    run_url = BASE_URL + f"/{pipeline_id}/runs"
    body = {
        "resources": {
            "repositories": {
                "common": {
                    "repository": {
                        "fullName": "NHSDigital/api-management-utils",
                        "type": "gitHub",
                    },
                    "refName": f"refs/pull/{UTILS_PR_NUMBER}/merge",
                },
                "self": {"refName": f"refs/heads/{pipeline_branch}"},
            }
        },
        "variables": {
            "NOTIFY_GITHUB_REPOSITORY": {
                "isSecret  ": False,
                "value": f"{NOTIFY_GITHUB_REPOSITORY}",
            },
            "NOTIFY_COMMIT_SHA": {
                "isSecret  ": False,
                "value": f"{NOTIFY_COMMIT_SHA}"
            },
            "UTILS_PR_NUMBER": {
                "isSecret  ": False,
                "value": f"{UTILS_PR_NUMBER}",
            }
        },
    }

    response = requests.post(run_url, auth=AUTH, params=PARAMS, json=body)
    print_response(response, f"Initial request to {run_url}")

    result = "failed"
    if wait_for_completion and response.status_code == 200:
        delay = 0
        state_url = response.json()["_links"]["self"]["href"]
        while response.status_code == 200 and response.json()["state"] == "inProgress":
            time.sleep(WAIT_TIME_SECONDS)
            delay = delay + WAIT_TIME_SECONDS
            response = requests.get(state_url, auth=AUTH, params=PARAMS)
            print_response(response, f"Response from {state_url} after {delay} seconds")
        result = response.json()["result"]
        print(f"Result of {service} {pipeline_type} pipeline: {result}")
    elif response.status_code == 203 or response.status_code == 401:
        print(f"{response.status_code}: Invalid or expired PAT (Personal Access Token), please verify or renew token")
    else:
        print(f"Triggering pipeline: {service} {pipeline_type} failed, status code: {response.status_code}")
    return result


def trigger_pipelines(pipeline_ids: dict, service: str):
    build_status = run_pipeline(
        service=service,
        pipeline_type="build",
        pipeline_id=pipeline_ids["build"],
        pipeline_branch=pipeline_ids["branch"],
        wait_for_completion=True
    )
    if build_status != "succeeded":
        return
    run_pipeline(
        service=service,
        pipeline_type="pr",
        pipeline_id=pipeline_ids["pr"],
        pipeline_branch=pipeline_ids["branch"],
        wait_for_completion=True
    )


def main():
    jobs = []
    for service, pipeline_ids in PIPELINES.items():
        process = Process(target=trigger_pipelines, args=(pipeline_ids, service,))
        process.start()
        jobs.append(process)
    for process in jobs:
        process.join()
    sys.exit(0)


if __name__ == "__main__":
    main()
