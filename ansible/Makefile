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

build-ecs-proxies: guard-build_label guard-service_basename guard-CONTAINER_VARS_FILE
	@build_label=$(build_label) service_basename=$(service_basename) poetry run ansible-playbook -i local build-ecs-proxies.yml

deploy-ecs-proxies: guard-build_label guard-service_basename guard-APIGEE_ENVIRONMENT guard-PROXY_VARS_FILE
	@build_label=$(build_label) temp_out_dir=$(temp_out_dir) service_basename=$(service_basename) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local deploy-ecs-proxies.yml

destroy-ecs-proxies: guard-service_basename guard-APIGEE_ENVIRONMENT
	@service_basename=$(service_basename) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local destroy-ecs-proxies.yml

destroy-api-deployment-dns-entry: guard-service_basename guard-APIGEE_ENVIRONMENT
	@service_basename=$(service_basename) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local destroy-api-deployment-dns-entry.yml

remove-ecs-proxy-deployment: guard-service_basename guard-APIGEE_ENVIRONMENT
	@service_basename=$(service_basename) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local remove-ecs-proxy-deployment.yml


create-api-deployment-user-access-key: guard-account guard-service_basename guard-APIGEE_ENVIRONMENT guard-SERVICE_BASE_PATH
	@account=$(account) SERVICE_BASE_PATH=$(SERVICE_BASE_PATH) service_basename=$(service_basename) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local create-api-deployment-user-access-key.yml

remove-api-deployment-user-access-key: guard-account guard-service_basename guard-APIGEE_ENVIRONMENT
	@account=$(account) service_basename=$(service_basename) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local remove-api-deployment-user-access-key.yml

create-ecr-build-user: guard-account guard-service_basename
	@account=$(account) service_basename=$(service_basename) poetry run ansible-playbook -i local create-ecr-build-user.yml

remove-ecr-build-user: guard-account guard-service_basename
	@account=$(account) service_basename=$(service_basename) poetry run ansible-playbook -i local remove-ecr-build-user.yml

create-api-deployment-pre-reqs: guard-service_basename guard-APIGEE_ENVIRONMENT guard-account
	@service_basename=$(service_basename) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local create-api-deployment-pre-reqs.yml

create-api-deployment-dns-entry: guard-service_basename guard-APIGEE_ENVIRONMENT guard-account
	@temp_out_dir=$(temp_out_dir) service_basename=$(service_basename) APIGEE_ENVIRONMENT=$(APIGEE_ENVIRONMENT) poetry run ansible-playbook -i local create-api-deployment-dns-entry.yml
