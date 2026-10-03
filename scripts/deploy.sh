#!/usr/bin/env bash

set -e

echo "Deploying AWS DevOps Platform..."

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

echo "Waiting for deployment rollout..."

kubectl rollout status deployment/aws-devops-platform --timeout=120s

echo "Deployment rollout completed."

echo "Running application health check..."

./scripts/health-check.sh

echo "Deployment and health check completed successfully."
