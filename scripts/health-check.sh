#!/usr/bin/env bash

set -e

echo "Checking application health..."

kubectl run health-check \
  --rm \
  -i \
  --restart=Never \
  --image=curlimages/curl:8.10.1 \
  -- \
  curl -f http://aws-devops-platform.default.svc.cluster.local/health

echo
echo "Health check passed."
