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




template-manifest: guard-DIST_DIR
	@poetry run ansible-playbook -i local template-manifest.yml

validate-manifest: guard-DIST_DIR
	@poetry run ansible-playbook -i local validate-manifest.yml

deploy-manifest: guard-APIGEE_ENVIRONMENT guard-APIGEE_ORGANIZATION guard-APIGEE_ACCESS_TOKEN
	@poetry run ansible-playbook --diff -i local deploy-manifest.yml

build-ecs-proxies: guard-build_label guard-service_id guard-CONTAINER_VARS_FILE
	@poetry run ansible-playbook -i local build-ecs-proxies.yml

remove-ecs-proxy-deployment: guard-service_id guard-APIGEE_ENVIRONMENT
	@poetry run ansible-playbook -i local remove-ecs-proxy-deployment.yml

create-build-env-vars: guard-build_label guard-out_dir
	@poetry run ansible-playbook -i local create-build-env-vars.yml

deploy-ecs-proxies: guard-account guard-build_label guard-service_id guard-APIGEE_ENVIRONMENT guard-PROXY_VARS_FILE
	@poetry run ansible-playbook -i local deploy-ecs-proxies.yml

deploy-apigee-proxy: guard-SERVICE_NAME guard-SERVICE_BASE_PATH guard-APIGEE_ENVIRONMENT guard-APIGEE_ORGANIZATION guard-APIGEE_ACCESS_TOKEN guard-PROXY_DIR guard-PING
	@poetry run ansible-playbook -i local deploy-apigee-proxy.yml

deploy-apigee-product-and-spec: guard-SERVICE_NAME guard-APIGEE_ENVIRONMENT guard-APIGEE_ORGANIZATION guard-APIGEE_ACCESS_TOKEN guard-FRIENDLY_NAME guard-PRODUCT_DISPLAY_NAME guard-PRODUCT_DESCRIPTION guard-VISIBLE guard-REQUIRE_CALLBACK_URL
	@poetry run ansible-playbook -i local deploy-apigee-product-and-spec.yml

template-proxies: guard-PROXIES_DIR guard-SERVICE_BASE_PATH guard-APIGEE_ENVIRONMENT
	@poetry run ansible-playbook -i local template-proxies.yml

destroy-ecs-proxies: guard-service_id guard-APIGEE_ENVIRONMENT
	@poetry run ansible-playbook -i local destroy-ecs-proxies.yml

destroy-api-deployment-dns-entry: guard-service_id guard-APIGEE_ENVIRONMENT
	@poetry run ansible-playbook -i local destroy-api-deployment-dns-entry.yml

create-api-deployment-user-access-key: guard-account guard-service_id guard-APIGEE_ENVIRONMENT
	@poetry run ansible-playbook -i local create-api-deployment-user-access-key.yml

remove-api-deployment-user-access-key: guard-account guard-service_id guard-APIGEE_ENVIRONMENT
	@poetry run ansible-playbook -i local remove-api-deployment-user-access-key.yml

remove-ecs-proxy-pre-reqs: guard-account guard-service_id guard-APIGEE_ENVIRONMENT
	@poetry run ansible-playbook -i local remove-ecs-proxy-pre-reqs.yml

create-ecr-build-user: guard-account guard-service_id
	@poetry run ansible-playbook -i local create-ecr-build-user.yml

remove-ecr-build-user: guard-account guard-service_id
	@poetry run ansible-playbook -i local remove-ecr-build-user.yml

create-api-deployment-pre-reqs: guard-service_id guard-APIGEE_ENVIRONMENT guard-account
	@poetry run ansible-playbook -i local create-api-deployment-pre-reqs.yml

create-api-deployment-dns-entry: guard-service_id guard-APIGEE_ENVIRONMENT guard-account
	@poetry run ansible-playbook -i local create-api-deployment-dns-entry.yml

remove-old-ecs-pr-deploys:
	@poetry run ansible-playbook -i local remove-old-ecs-pr-deploys.yml

remove-old-pr-portal-apis:
	@poetry run ansible-playbook -i local remove-old-pr-portal-apis.yml

remove-old-pr-specs:
	@poetry run ansible-playbook -i local remove-old-pr-specs.yml
