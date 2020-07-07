SHELL := /bin/bash
########################################################################################################################
##
## Makefile for managing apm terraform
##
########################################################################################################################
dirname := $(notdir $(patsubst %/,%,$(CURDIR)))
backend ="-backend-config=backend.conf"
vars ="-var-file=vars.tfvars"
workspace :="{{ workspace }}"

args =
tf-command = apply
.DEFAULT_GOAL := apply

init=1
extra_args =


guard-%:
	@ if [ "${${*}}" = "" ]; then \
        echo "Environment variable $* not set"; \
        exit 1; \
    fi

.ONESHELL:

run:
	@ if [ "$(tf-command)" != "output" ]; then \
		terraform $(tf-command) $(vars) $(extra_args) $(args); \
	else \
		terraform $(tf-command) $(extra_args) $(args); \
	fi

init: guard-workspace
	@ if [ $(init) -eq 1 ]; then \
		TF_PLUGIN_CACHE_DIR="$$HOME/.terraform.d/plugin-cache" terraform init $(vars) $(backend); \
		if terraform workspace list | grep -e $(workspace)$$; then terraform workspace select $(workspace); else terraform workspace new $(workspace); fi; \
	fi

clean:
	rm .terraform.plan 2>/dev/null | true
	rm -r .terraform 2>/dev/null | true
	rm -r terraform.tfstate.d 2>/dev/null | true
	rm errored.tfstate 2>/dev/null | true

echo: vars
	@echo account: $(account)
	@echo workspace: $(workspace)

no-init: init=0
no-init: run

apply: tf-command=apply
apply: init no-init

output: tf-command=output
output: init run

plan: tf-command=plan
plan: extra_args = -detailed-exitcode
plan: init run

plan-no-init: init=0
plan-no-init: plan

apply-plan: init=0
apply-plan: vars=
apply-plan: guard-args no-init

refresh: tf-command=refresh
refresh: init run
