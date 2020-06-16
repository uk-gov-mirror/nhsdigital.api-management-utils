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
	@PROXIES_DIR=$(PROXIES_DIR) SERVICE_BASE_PATH=$(SERVICE_BASE_PATH) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) ansible-playbook -i local template-proxies.yml

build-ecs-proxies: guard-build_label guard-SERVICE_NAME guard-CONTAINER_VARS_FILE
	@API_ACCESS_TOKEN=NOTREQUIRED build_label=$(build_label) SERVICE_NAME=$(SERVICE_NAME) poetry run ansible-playbook -i local build-ecs-proxies.yml

deploy-ecs-proxies: guard-build_label guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT guard-PROXY_VARS_FILE
	@API_ACCESS_TOKEN=NOTREQUIRED @build_label=$(build_label) temp_out_dir=$(temp_out_dir) SERVICE_NAME=$(SERVICE_NAME) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local deploy-ecs-proxies.yml

destroy-ecs-proxies: guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT
	@SERVICE_NAME=$(SERVICE_NAME) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local destroy-ecs-proxies.yml

create-api-deployment-user-access-key: guard-account guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT guard-SERVICE_BASE_PATH
	@account=$(account) SERVICE_BASE_PATH=$(SERVICE_BASE_PATH) SERVICE_NAME=$(SERVICE_NAME) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local create-api-deployment-user-access-key.yml

remove-api-deployment-user-access-key: guard-account guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT
	@account=$(account) SERVICE_NAME=$(SERVICE_NAME) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local remove-api-deployment-user-access-key.yml

create-ecr-build-user: guard-account guard-SERVICE_NAME
	@account=$(account) SERVICE_NAME=$(SERVICE_NAME) poetry run ansible-playbook -i local create-ecr-build-user.yml

remove-ecr-build-user: guard-account guard-SERVICE_NAME
	@account=$(account) SERVICE_NAME=$(SERVICE_NAME) poetry run ansible-playbook -i local remove-ecr-build-user.yml

create-api-deployment-pre-reqs: guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT guard-account
	@API_ACCESS_TOKEN=NOTREQUIRED SERVICE_NAME=$(SERVICE_NAME) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local create-api-deployment-pre-reqs.yml

create-api-deployment-dns-entry: guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT guard-account
	@API_ACCESS_TOKEN=NOTREQUIRED @temp_out_dir=$(temp_out_dir) SERVICE_NAME=$(SERVICE_NAME) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local create-api-deployment-dns-entry.yml
