SHELL := /bin/bash

########################################################################################################################
##
## Makefile for managing ansible commands
##
########################################################################################################################

list:
	@grep '^[^#[:space:]].*:' Makefile

guard-%:
	@ if [ "${${*}}" = "" ]; then \
	    echo "Environment variable $* not set"; \
	    exit 1; \
	fi

ansible-lint:
	@# Only swallow checking errors (rc=2), not other problems (rc=1)
	poetry run ansible-lint -c ansible-lint.yml -p ansible/*.yml || test $$? -eq 2


ensure-poetry:
	@if ! hash poetry 2>/dev/null; then \
		pip install --upgrade pip setuptools; \
        curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python; \
	fi


install: ensure-poetry
	@source $$HOME/.poetry/env; \
	poetry install

#########################################################################################################################
###
### Generic sub command running
###
#########################################################################################################################
first_target := $(firstword $(MAKECMDGOALS))
cmd_targets := ansible
run_targets := run run-tag run-host
ifneq ($(filter $(first_target),$(cmd_targets)),)
  cmd := $(wordlist 2, $(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(cmd):;@true)
endif

ansible: guard-cmd
	@account=$(account) poetry run make --no-print-directory -C ansible $(cmd)
