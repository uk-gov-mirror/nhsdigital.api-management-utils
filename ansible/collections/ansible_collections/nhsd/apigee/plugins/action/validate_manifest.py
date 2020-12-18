from ansible_collections.nhsd.apigee.plugins.module_utils.models.ansible.validate_manifest import (
    ValidateManifest,
)
from ansible_collections.nhsd.apigee.plugins.module_utils.apigee_action import (
    ApigeeAction,
)


class ActionModule(ApigeeAction):
    def run(self, tmp=None, task_vars=None):
        super(ActionModule, self).run(tmp, task_vars)
        args, errors = self.validate_args(ValidateManifest)
        if errors:
            return errors
        return {"apigee": args.apigee.dict(), "changed": False}
