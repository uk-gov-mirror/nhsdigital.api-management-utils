account            = "{{ account }}"
profile            = "{{ aws_profile }}"
workspace          = "{{ workspace }}"
service_name       = "{{ service_name }}"
apigee_environment = "{{ apigee_environment }}"
namespace          = "{{ 'pr-' + PR_NUMBER if PR_NUMBER else '' }}"
state_bucket       = "nhsd-apm-management-{{ account }}-terraform"
build_label        = "{{ build_label }}"
