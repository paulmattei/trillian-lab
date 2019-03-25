#!/usr/bin/env bash
# Script assumptions:
# - Cluster has already been created & configured using the create.sh script
# - Go 1.10 is installed

function checkEnv() {
  if [ -z ${PROJECT_ID+x} ] ||
     [ -z ${CLUSTER_NAME+x} ] ||
     [ -z ${REGION+x} ] ||
     [ -z ${NODE_LOCATIONS+x} ] ||
     [ -z ${MASTER_ZONE+x} ] ||
     [ -z ${CONFIGMAP+x} ] ||
     [ -z ${POOLSIZE+x} ] ||
     [ -z ${MACHINE_TYPE+x} ]; then
    echo "You must either pass an argument which is a config file, or set all the required environment variables" >&2
    exit 1
  fi
}

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ $# -eq 1 ]; then
  source $1
else
  checkEnv
fi


export TAG=$(git rev-parse HEAD)

cd $GOPATH/src/github.com/google/trillian

envsubst < examples/deployment/kubernetes/trillian-cloudspanner.yaml | kubectl delete -f -

# Delete log-[service|signer]
envsubst < examples/deployment/kubernetes/trillian-log-deployment.yaml | kubectl delete -f -
envsubst < examples/deployment/kubernetes/trillian-log-service.yaml | kubectl delete -f -
envsubst < examples/deployment/kubernetes/trillian-log-signer-deployment.yaml | kubectl delete -f -
envsubst < examples/deployment/kubernetes/trillian-log-signer-service.yaml | kubectl delete -f -
