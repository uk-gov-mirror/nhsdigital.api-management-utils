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


template-proxies: guard-PROXIES_DIR guard-SERVICE_BASEPATH guard-APIGEE_ENVIRONMENT

	PROXIES_DIR=$(PROXIES_DIR) SERVICE_BASEPATH=$(SERVICE_BASEPATH) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) ansible-playbook -i local template-proxies.yml
