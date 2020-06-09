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


template-proxies: guard-PROXIES_DIR guard-SERVICE_BASE_PATH guard-APIGEE_ENVIRONMENT

	PROXIES_DIR=$(PROXIES_DIR) SERVICE_BASE_PATH=$(SERVICE_BASE_PATH) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) ansible-playbook -i local template-proxies.yml

build-ecs-proxies: guard-build_label guard-SERVICE_NAME
	@build_label=$(build_label) SERVICE_NAME=$(SERVICE_NAME) poetry run ansible-playbook -i local build-ecs-proxies.yml

deploy-ecs-proxies: guard-build_label guard-SERVICE_NAME guard-SERVICE_BASE_PATH guard-APIGEE_ENVIRONMENT
	@build_label=$(build_label) SERVICE_NAME=$(SERVICE_NAME) SERVICE_BASE_PATH=$(SERVICE_BASE_PATH) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local deploy-ecs-proxies.yml
