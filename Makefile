SHELL := /bin/bash
poetry=source $$HOME/.poetry/env;poetry
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

build-prereqs:
	@if ! hash poetry 2>/dev/null; then \
		sudo apt-get -yq install python3-pip; \
	fi; \
	if ! dpkg -l | grep python3-venv > /dev/null; then \
		sudo apt-get -yq install python3-venv; \
	fi; \
	pip3 install --upgrade pip setuptools; \
	if ! python --version | grep 'Python 3' > /dev/null; then \
		sudo unlink /usr/bin/python; \
		sudo ln -s /usr/bin/python3 /usr/bin/python; \
	fi;
	if ! hash poetry 2>/dev/null; then \
		curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3; \
	fi

install:
	$(poetry) install

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
