import os
import sys
from multiprocessing import Process
from trigger_pipelines import AzureDevOps

UTILS_PR_NUMBER = os.environ["UTILS_PR_NUMBER"]

PULL_REQUEST_PIPELINES = {
    "identity-service": {
        "build": 27,
        "pr": 54,
        "branch": "refs/heads/master"
    },
    "canary-api": {
        "build": 222,
        "pr": 223,
        "branch": "refs/heads/main"
    },
    "personal-demographics-service": {
        "build": 140,
        "pr": 144,
        "branch": "refs/heads/master"
    }
}


def trigger_pipelines(pipeline_ids: dict, service: str):
    azure_dev_ops = AzureDevOps(utils_pr_number=UTILS_PR_NUMBER)
    build_status = azure_dev_ops.run_pipeline(
        service=service,
        pipeline_type="build",
        pipeline_id=pipeline_ids["build"],
        pipeline_branch=pipeline_ids["branch"],
        wait_for_completion=True
    )
    if build_status != "succeeded":
        return
    azure_dev_ops.run_pipeline(
        service=service,
        pipeline_type="pr",
        pipeline_id=pipeline_ids["pr"],
        pipeline_branch=pipeline_ids["branch"],
        wait_for_completion=True
    )


def main():
    jobs = []
    for service, pipeline_ids in PULL_REQUEST_PIPELINES.items():
        process = Process(target=trigger_pipelines, args=(pipeline_ids, service,))
        process.start()
        jobs.append(process)
    for process in jobs:
        process.join()
    sys.exit(0)


if __name__ == "__main__":
    main()
