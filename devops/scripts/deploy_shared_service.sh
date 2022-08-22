#!/bin/bash

set -o errexit
set -o pipefail
# Uncomment this line to see each command for debugging (careful: this will show secrets!)
# set -o xtrace

function usage() {
    cat <<USAGE

    Usage: $0 [--propertyName propertyValue ...]

    Options:

        Additional bundle properties to be passed to the bundle on install can be passed in the format --propertyName propertyValue
USAGE
    exit 1
}

while [ "$1" != "" ]; do
    case $1 in
    --*)
        property_names+=("${1:2}")
        shift
        property_values+=("$1")
        ;;
    esac

    if [[ -z "$2" ]]; then
      # if no more args then stop processing
      break
    fi

    shift # remove the current value for `$1` and use the next
done

# done with processing args and can set this
set -o nounset

template_name=$(yq eval '.name' porter.yaml)
template_version=$(yq eval '.version' porter.yaml)
echo "Deploying shared service ${template_name} of version ${template_version}"

# Get shared services and determine if the given shared service has already been deployed
get_shared_services_result=$(tre shared-services)
last_result=$?
if [[ "$last_result" != 0 ]]; then
  echo "Failed to get shared services ${template_name}"
  echo "${get_shared_services_result}"
  exit 1
fi

deployed_shared_service=$(echo "${get_shared_services_result}" \
  | grep '{' \
  | jq -r ".sharedServices[] | select(.templateName == \"${template_name}\" and .deploymentStatus == \"deployed\")")

if [[ -n "${deployed_shared_service}" ]]; then
  # Get template version of the service already deployed
  deployed_version=$(echo "${deployed_shared_service}" | jq -r ".templateVersion")

  if [[ "${template_version}" == "${deployed_version}" ]]; then
    echo "Shared service ${template_name} of version ${template_version} has already been deployed"
    exit 0
  else
    echo "Resource upgrade isn't currently implemented. See https://github.com/microsoft/AzureTRE/issues/141"
    exit 0
  fi
fi

# Add additional properties to the payload JSON string
additional_props=""
for index in "${!property_names[@]}"; do
  name=${property_names[$index]}
  value=${property_values[$index]}
  additional_props="$additional_props, \"$name\": \"$value\""
done

payload="{ \"templateName\": \"""${template_name}""\", \"properties\": { \"display_name\": \"Shared service ""${template_name}""\", \"description\": \"Automatically deployed ""${template_name}""\"${additional_props} } }"
deploy_result=$(tre shared-services new --definition "$payload" --wait-for-completion)
if [[ "$last_result" != 0 ]]; then
  echo "Failed to deploy shared service:"
  echo "${deploy_result}"
  exit 1
fi
echo "Deployed shared service ""${template_name}"""
