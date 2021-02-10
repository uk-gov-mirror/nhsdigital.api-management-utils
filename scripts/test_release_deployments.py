import os
import sys
from multiprocessing import Process
from trigger_pipelines import AzureDevOps

RELEASE_PIPELINES = {
    "canary-api": {
        "build": 222,
        "release": 224,
    }
}


def get_repo_tag(service: str):
    stream = os.popen(f"git -c 'versionsort.suffix=-' ls-remote --tags "
                      f"--sort='v:refname' https://github.com/NHSDigital/{service} | tail -n1 | sed 's/.*\///;'")
    tag = stream.read().strip()
    return f"refs/tags/{tag}"


def trigger_pipelines(pipeline_ids: dict, service: str, tag: str):
    azure_dev_ops = AzureDevOps()
    build_status = azure_dev_ops.run_pipeline(
        service=service,
        pipeline_type="build",
        pipeline_id=pipeline_ids["build"],
        pipeline_branch=tag,
        wait_for_completion=True
    )
    if build_status != "succeeded":
        return
    azure_dev_ops.run_pipeline(
        service=service,
        pipeline_type="release",
        pipeline_id=pipeline_ids["release"],
        pipeline_branch=tag,
        wait_for_completion=True
    )


def main():
    jobs = []
    for service, pipeline_ids in RELEASE_PIPELINES.items():
        tag = get_repo_tag(service)
        print(tag)
        process = Process(target=trigger_pipelines, args=(pipeline_ids, service, tag))
        process.start()
        jobs.append(process)
    for process in jobs:
        process.join()
    sys.exit(0)


if __name__ == "__main__":
    main()
