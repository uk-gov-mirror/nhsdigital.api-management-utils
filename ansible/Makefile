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

build-ecs-proxies: guard-build_label guard-SERVICE_NAME guard-CONTAINER_VARS_FILE
	@build_label=$(build_label) SERVICE_NAME=$(SERVICE_NAME) poetry run ansible-playbook -i local build-ecs-proxies.yml

deploy-ecs-proxies: guard-build_label guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT guard-PROXY_VARS_FILE
	@build_label=$(build_label) temp_out_dir=$(temp_out_dir) SERVICE_NAME=$(SERVICE_NAME) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local deploy-ecs-proxies.yml

destroy-ecs-proxies: guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT
	@SERVICE_NAME=$(SERVICE_NAME) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local destroy-ecs-proxies.yml

