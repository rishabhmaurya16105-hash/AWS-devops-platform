# Production-Grade AWS DevOps Platform

An end-to-end DevOps project demonstrating application development, containerization, infrastructure as code, Kubernetes deployment, CI/CD automation, security scanning, monitoring, and production-oriented troubleshooting.

## Project Overview

This project implements a production-oriented DevOps platform for a Python Flask application.

The platform uses Docker for containerization, Kubernetes for orchestration, Terraform for AWS infrastructure provisioning, GitHub Actions for CI/CD automation, Trivy for container security scanning, and Prometheus/Grafana for monitoring and observability.

The Kubernetes environment is implemented using `kind` locally to avoid the cost of managed Kubernetes services such as Amazon EKS.

## Key Features

- Python Flask application with health and metrics endpoints
- Docker containerization
- Kubernetes Deployment and Service
- Kubernetes ConfigMap and Secret integration
- Liveness and readiness probes
- CPU and memory resource requests/limits
- Horizontal Pod Autoscaling
- NGINX Ingress
- Terraform-based AWS infrastructure
- GitHub Actions CI pipeline
- GitHub Actions CD pipeline
- Docker image security scanning with Trivy
- Prometheus metrics collection
- Grafana dashboards
- Controlled failure and incident testing
- Kubernetes troubleshooting and recovery procedures
- Reusable deployment and health-check scripts

## Architecture

```text
Developer
   |
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   +--------------------+
   |                    |
   v                    v
CI Pipeline          CD Pipeline
   |                    |
   +--> Tests           +--> Build Docker Image
   +--> K8s Validation  +--> Create kind Cluster
   +--> Docker Build    +--> Load Image
   +--> Trivy Scan      +--> Deploy to Kubernetes
                        +--> Rollout Verification
                        +--> Health Check
                                 |
                                 v
                         Kubernetes (kind)
                                 |
                 +---------------+---------------+
                 |               |               |
                 v               v               v
             Deployment       Service          HPA
                 |
                 v
          Python Flask App
                 |
          +------+------+
          |             |
          v             v
      Prometheus      Grafana

Terraform
   |
   v
AWS Infrastructure

## Technology Stack

| Category | Technology |
|---|---|
| Application | Python, Flask |
| Version Control | Git, GitHub |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Local Kubernetes | kind |
| Infrastructure as Code | Terraform |
| Cloud | AWS |
| CI/CD | GitHub Actions |
| Security | Trivy |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Ingress | NGINX Ingress |
| Automation | Bash |


## CI/CD Workflow

### Continuous Integration

Every push or pull request to the `main` branch triggers the CI pipeline.

The CI pipeline performs:

1. Checkout source code
2. Set up Python 3.14
3. Install application dependencies
4. Run automated tests with Pytest
5. Validate Kubernetes manifests
6. Build the Docker image
7. Scan the Docker image using Trivy
8. Fail the pipeline when HIGH or CRITICAL vulnerabilities are detected

### Continuous Deployment

After a successful CI run on the `main` branch, the CD workflow is triggered automatically.

The CD pipeline:

1. Checks out the exact commit that passed CI
2. Creates a temporary Kubernetes `kind` cluster
3. Builds the Docker image
4. Loads the image into the Kubernetes cluster
5. Deploys ConfigMap and Secret
6. Deploys the application
7. Creates the Kubernetes Service and HPA
8. Waits for the deployment rollout
9. Performs an application health check

This provides an automated path from source-code change to validated Kubernetes deployment.


## Kubernetes Deployment

The application is deployed on a local Kubernetes cluster created using `kind`.

The Kubernetes configuration includes:

- Deployment with 2 application replicas
- ClusterIP Service
- ConfigMap for application configuration
- Secret for sensitive configuration
- Liveness probe
- Readiness probe
- CPU and memory resource requests and limits
- Horizontal Pod Autoscaler from 2 to 5 replicas
- NGINX Ingress
- Rolling deployment and rollback support

The application exposes:

| Endpoint | Purpose |
|---|---|
| `/` | Application information |
| `/health` | Health check |
| `/info` | Application configuration information |
| `/metrics` | Prometheus metrics |
| `/error` | Controlled HTTP 500 failure for incident testing |

## Monitoring and Observability

Prometheus is used to collect application and Kubernetes metrics, while Grafana provides visualization and dashboards.

The monitoring setup tracks:

- Application request rate
- HTTP status codes
- HTTP 5xx error rate
- Application pod CPU usage
- Application pod memory usage
- Pod restart count
- Kubernetes node CPU usage

A controlled `/error` endpoint was also used to generate HTTP 500 responses and verify that the error rate was visible through Prometheus and Grafana.

## Security

Container images are scanned using Trivy as part of the CI pipeline.

The pipeline checks for HIGH and CRITICAL vulnerabilities and fails when actionable vulnerabilities are detected.

Kubernetes configuration also separates application configuration through ConfigMaps and sensitive values through Kubernetes Secrets.

The Secret used in this project contains only a demonstration value and does not contain production credentials.

## Troubleshooting and Incident Response

The project includes documented failure scenarios to demonstrate practical troubleshooting skills.

### Incident 1 — HTTP 500 Application Error

A controlled `/error` endpoint was used to generate HTTP 500 responses.

Prometheus detected the increase in 5xx traffic and Grafana displayed the corresponding error spike.

### Incident 2 — ImagePullBackOff

A deployment was intentionally configured with an unavailable Docker image tag.

The resulting `ImagePullBackOff` condition was investigated using Kubernetes pod status, events, and rollout information.

The deployment was then restored to a known-good image and successfully rolled out again.

These exercises demonstrate monitoring, diagnosis, recovery, and rollback-oriented troubleshooting.

## Automation Scripts

The repository includes reusable Bash scripts for common deployment operations.

### Deployment Script

`scripts/deploy.sh`

The script:

- Applies Kubernetes manifests
- Waits for deployment rollout
- Runs the application health check

### Health Check Script

`scripts/health-check.sh`

The script runs an in-cluster HTTP health check against the application Service and verifies that the `/health` endpoint responds successfully.


## AWS and Terraform

Terraform is used to demonstrate Infrastructure as Code and AWS resource provisioning.

The Terraform configuration:

- Configures the AWS provider
- Uses the selected AWS region
- Retrieves the AWS account identity
- Creates an S3 bucket using a generated bucket prefix
- Applies project and environment tags
- Exposes Terraform outputs for account ID, region, and bucket name

The AWS infrastructure is intentionally kept minimal and cost-controlled for a student project.

Temporary AWS resources can be removed using:

```bash
cd terraform
terraform destroy

#structure

aws-devops-platform/
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── tests/
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── hpa.yaml
│   └── servicemonitor.yaml
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   └── versions.tf
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── monitoring/
├── scripts/
│   ├── deploy.sh
│   ├── health-check.sh
│   └── cleanup.sh
├── docs/
│   ├── architecture.md
│   ├── deployment.md
│   ├── troubleshooting.md
│   └── incidents/
├── Dockerfile
├── .gitignore
└── README.md



Local Development
Prerequisites

The following tools are required:

Git
Python 3.14+
Docker
kubectl
kind
Terraform
AWS CLI

Clone the Repository
git clone https://github.com/rishabhmaurya16105-hash/AWS-devops-platform.git
cd AWS-devops-platform

Create Python Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

Install Dependencies
pip install -r app/requirements.txt

Run Tests
pytest -q

Build Docker Image
docker build -t aws-devops-platform:latest .

Create Kubernetes Cluster
kind create cluster --name aws-devops

Deploy Application
./scripts/deploy.sh

The deployment script waits for the Kubernetes rollout and performs an application health check.

Validation

The project has been validated through:

Automated Python unit tests
Docker image builds
Trivy security scanning
Kubernetes manifest validation
Successful Kubernetes rollouts
Kubernetes health checks
Horizontal Pod Autoscaler testing
Prometheus metric collection
Grafana dashboard validation
Controlled HTTP 500 incident testing
ImagePullBackOff troubleshooting and recovery
Successful GitHub Actions CI execution
Successful GitHub Actions CD execution

Future Improvements

Potential future improvements include:

Deployment to Amazon EKS
Container image publishing to Amazon ECR
HTTPS/TLS configuration
Centralized logging
Alertmanager integration
GitOps deployment using Argo CD
Remote Terraform state management
Production-grade secrets management using AWS Secrets Manager
Project Notes

This project is designed as a student portfolio and interview demonstration.

The Kubernetes environment uses kind instead of Amazon EKS to keep the project cost-controlled.

AWS resources created through Terraform should be destroyed after testing when they are no longer required.

No production credentials or sensitive secrets are stored in the repository.

Author

Rishabh Kumar Singh

B.Tech — Electronics and Communication Engineering
