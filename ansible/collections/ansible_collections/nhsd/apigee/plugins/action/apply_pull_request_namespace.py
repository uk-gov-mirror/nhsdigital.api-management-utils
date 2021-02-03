from ansible_collections.nhsd.apigee.plugins.module_utils.apigee_action import (
    ApigeeAction,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.models.ansible.apply_pull_request_namespace import (
    ApplyPullRequestNamespace,
)


class ActionModule(ApigeeAction):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        args, errors = self.validate_args(ApplyPullRequestNamespace)
        if errors:
            return errors
        return {"manifest": args.manifest.dict(), "changed": False}
