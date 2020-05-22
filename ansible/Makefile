SHELL := /bin/bash

########################################################################################################################
##
## Makefile for managing ansible commands
##
########################################################################################################################

guard-%:
	@ if [ "${${*}}" = "" ]; then \
	    echo "Environment variable $* not set"; \
	    exit 1; \
	fi


template-proxies: guard-PROXIES_DIR guard-SERVICE_BASE_PATH guard-APIGEE_ENVIRONMENT

	PROXIES_DIR=$(PROXIES_DIR) SERVICE_BASE_PATH=$(SERVICE_BASE_PATH) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) ansible-playbook -i local template-proxies.yml
