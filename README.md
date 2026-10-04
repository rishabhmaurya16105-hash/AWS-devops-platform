# Production-Grade AWS DevOps Platform

An end-to-end DevOps portfolio project demonstrating application development, containerization, Infrastructure as Code, Kubernetes deployment, CI/CD automation, container security scanning, monitoring, observability, and production-oriented troubleshooting.

## Project Overview

This project implements a production-oriented DevOps platform for a Python Flask application.

The platform uses:

- Python and Flask for the application
- Docker for containerization
- Kubernetes for container orchestration
- kind for local Kubernetes deployment
- Terraform for AWS Infrastructure as Code
- GitHub Actions for CI/CD automation
- Trivy for container security scanning
- Prometheus for metrics collection
- Grafana for monitoring and visualization
- Bash scripts for deployment and health checks

The Kubernetes environment runs locally using `kind` instead of a managed Kubernetes service such as Amazon EKS. This keeps the project cost-controlled while still demonstrating real Kubernetes and DevOps workflows.

---

## Key Features

- Python Flask application
- Application health endpoint
- Prometheus metrics endpoint
- Docker containerization
- Kubernetes Deployment
- Kubernetes ClusterIP Service
- Kubernetes ConfigMap integration
- Kubernetes Secret integration
- Liveness and readiness probes
- CPU and memory resource requests and limits
- Horizontal Pod Autoscaler
- NGINX Ingress
- Terraform-based AWS infrastructure
- GitHub Actions Continuous Integration
- GitHub Actions Continuous Deployment
- Kubernetes manifest validation
- Docker image security scanning with Trivy
- Prometheus monitoring
- Grafana dashboards
- Controlled HTTP 500 failure testing
- ImagePullBackOff troubleshooting
- Kubernetes rollout and recovery
- Reusable deployment script
- Reusable application health-check script

---

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
                 +-----------+-----------+
                 |                       |
                 v                       v
            CI Pipeline             CD Pipeline
                 |                       |
        +--------+--------+       +------+----------------+
        |        |        |       |      |       |       |
        v        v        v       v      v       v       v
      Tests    K8s      Docker   Build   kind   Deploy  Health
              Validate   Build   Image   Cluster  App    Check
                 |                 |
                 v                 v
              Trivy            Load Image
               Scan                |
                                   v
                          Kubernetes (kind)
                                   |
                +------------------+------------------+
                |                  |                  |
                v                  v                  v
           Deployment           Service              HPA
                |
                v
         Python Flask App
                |
        +-------+--------+
        |                |
        v                v
   Prometheus         Grafana


                    Terraform
                        |
                        v
                AWS Infrastructure
```

Terraform is used independently to demonstrate AWS Infrastructure as Code.

The Kubernetes application itself runs locally through `kind` and does not require Amazon EKS.

---

## Technology Stack

| Category | Technology |
|---|---|
| Application | Python, Flask |
| Testing | Pytest |
| Version Control | Git, GitHub |
| Containerization | Docker |
| Orchestration | Kubernetes |
| Local Kubernetes | kind |
| Infrastructure as Code | Terraform |
| Cloud | AWS |
| CI/CD | GitHub Actions |
| Security Scanning | Trivy |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Ingress | NGINX Ingress |
| Automation | Bash |

---

## CI/CD Workflow

### Continuous Integration

Every push or pull request targeting the `main` branch triggers the CI pipeline.

The CI pipeline performs:

1. Checkout source code
2. Set up Python 3.14
3. Install application dependencies
4. Run automated tests using Pytest
5. Validate Kubernetes manifests
6. Build the Docker image
7. Scan the Docker image using Trivy
8. Fail the pipeline when HIGH or CRITICAL vulnerabilities are detected

The CI workflow provides automated validation before changes are considered deployable.

### Continuous Deployment

After a successful CI workflow for a push to the `main` branch, the CD workflow is triggered automatically.

The CD pipeline:

1. Checks out the exact commit that passed CI
2. Creates a temporary Kubernetes `kind` cluster
3. Builds the Docker image
4. Loads the image into the `kind` cluster
5. Deploys the ConfigMap
6. Deploys the Kubernetes Secret
7. Deploys the application
8. Creates the Kubernetes Service
9. Creates the Horizontal Pod Autoscaler
10. Waits for the deployment rollout
11. Performs an application health check

This provides an automated path from source-code change to a validated Kubernetes deployment.

---

## Kubernetes Deployment

The application is deployed on a local Kubernetes cluster created using `kind`.

The Kubernetes configuration includes:

- Deployment with 2 application replicas
- ClusterIP Service
- ConfigMap for application configuration
- Secret for demonstration sensitive configuration
- Liveness probe
- Readiness probe
- CPU and memory resource requests
- CPU and memory resource limits
- Horizontal Pod Autoscaler from 2 to 5 replicas
- NGINX Ingress
- Rolling deployment
- Rollback and recovery support

### Application Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Application information |
| `/health` | Application health check |
| `/info` | Application configuration information |
| `/metrics` | Prometheus metrics |
| `/error` | Controlled HTTP 500 failure for incident testing |

### Configuration Management

The application environment is provided through a Kubernetes ConfigMap.

Example:

```text
APP_ENV=development
```

A Kubernetes Secret is also used for demonstration purposes.

The Secret contains only a dummy value and does not contain real credentials.

---

## Monitoring and Observability

Prometheus is used to collect application and Kubernetes metrics.

Grafana is used to visualize the collected metrics through dashboards.

The monitoring setup tracks:

- Application request rate
- HTTP status codes
- HTTP 5xx error rate
- Application pod CPU usage
- Application pod memory usage
- Pod restart count
- Kubernetes node CPU usage

The application exposes the `/metrics` endpoint for Prometheus.

A controlled `/error` endpoint was also used to generate HTTP 500 responses and verify that application errors were visible through Prometheus and Grafana.

---

## Security

Container images are scanned using Trivy as part of the CI pipeline.

The CI security stage checks for:

- HIGH vulnerabilities
- CRITICAL vulnerabilities

The pipeline is configured to fail when applicable HIGH or CRITICAL vulnerabilities are detected.

The Docker image was also tested locally with Trivy during development.

Kubernetes configuration separates:

- Non-sensitive configuration using ConfigMaps
- Demonstration sensitive configuration using Secrets

No real production credentials are stored in the repository.

---

## Troubleshooting and Incident Response

This project includes controlled failure scenarios to demonstrate practical troubleshooting and incident-response skills.

### Incident 1 — HTTP 500 Application Error

A controlled `/error` endpoint was used to intentionally generate HTTP 500 responses.

Prometheus detected the increase in 5xx traffic and Grafana displayed the corresponding error spike.

The incident demonstrated:

- Application-level failure generation
- Prometheus metric analysis
- Grafana visualization
- HTTP error monitoring
- Controlled failure testing

### Incident 2 — ImagePullBackOff

The deployment was intentionally configured with an unavailable Docker image tag.

The resulting `ImagePullBackOff` condition was investigated using:

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl get events
kubectl rollout status deployment/aws-devops-platform
```

The failed deployment was then restored to a known-good image and successfully rolled out again.

The incident demonstrated:

- Kubernetes pod troubleshooting
- Image pull failure diagnosis
- Kubernetes event analysis
- Rollout troubleshooting
- Recovery to a known-good image

Detailed incident documentation is maintained under:

```text
docs/incidents/
```

---

## Automation Scripts

The repository contains reusable Bash scripts for common Kubernetes operations.

### Deployment Script

File:

```text
scripts/deploy.sh
```

The deployment script:

1. Applies the Kubernetes Deployment
2. Applies the Kubernetes Service
3. Applies the Horizontal Pod Autoscaler
4. Waits for the deployment rollout
5. Runs the application health check

Run it using:

```bash
./scripts/deploy.sh
```

### Health Check Script

File:

```text
scripts/health-check.sh
```

The health-check script runs an HTTP request from inside the Kubernetes cluster against the application Service.

It verifies that the `/health` endpoint responds successfully.

Run it using:

```bash
./scripts/health-check.sh
```

---

## AWS and Terraform

Terraform is used to demonstrate Infrastructure as Code and AWS resource provisioning.

The Terraform configuration:

- Configures the AWS provider
- Uses the selected AWS region
- Retrieves the AWS account identity
- Creates an S3 bucket using a generated bucket prefix
- Applies project and environment tags
- Provides Terraform outputs for account ID, region, and bucket name

The AWS infrastructure is intentionally kept minimal and cost-controlled for a student portfolio project.

### Terraform Initialization

From the project root:

```bash
cd terraform
terraform init
```

### Terraform Validation

```bash
terraform validate
```

### Terraform Plan

```bash
terraform plan
```

### Terraform Apply

```bash
terraform apply
```

### Terraform Destroy

Temporary AWS resources should be removed after testing when they are no longer required:

```bash
terraform destroy
```

> AWS resources may incur charges depending on the resource, account, region, and applicable AWS pricing/free-tier eligibility. Always verify resources after testing and destroy temporary infrastructure when it is no longer needed.

---

## Project Structure

The following structure reflects the files currently tracked in the repository:

```text
aws-devops-platform/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   └── tests/
│       └── test_app.py
│
├── docs/
│   └── incidents/
│       ├── INC-001-http-500.md
│       └── INC-002-image-pull-backoff.md
│
├── k8s/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── hpa.yaml
│   ├── ingress.yaml
│   ├── secret.yaml
│   ├── service.yaml
│   └── servicemonitor.yaml
│
├── scripts/
│   ├── deploy.sh
│   └── health-check.sh
│
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── versions.tf
│   └── .terraform.lock.hcl
│
├── Dockerfile
├── .gitignore
└── README.md
```

Generated local files such as the Python virtual environment, Python cache files, Terraform state, local Docker image archives, and local Trivy reports are intentionally excluded from version control.

---

## Local Development

### Prerequisites

The following tools are required:

- Git
- Python 3.14+
- Docker
- kubectl
- kind
- Terraform
- AWS CLI

### Clone the Repository

```bash
git clone https://github.com/rishabhmaurya16105-hash/AWS-devops-platform.git
cd AWS-devops-platform
```

### Create Python Virtual Environment

On Linux/WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r app/requirements.txt
```

### Run Tests

```bash
pytest -q
```

### Build Docker Image

```bash
docker build -t aws-devops-platform:latest .
```

### Create Kubernetes Cluster

```bash
kind create cluster --name aws-devops
```

### Deploy the Application

```bash
./scripts/deploy.sh
```

The deployment script waits for the Kubernetes rollout and performs an application health check.

---

## Kubernetes Validation

Check the application pods:

```bash
kubectl get pods
```

Check the deployment:

```bash
kubectl get deployment
```

Check the service:

```bash
kubectl get service
```

Check the HPA:

```bash
kubectl get hpa
```

Check the rollout:

```bash
kubectl rollout status deployment/aws-devops-platform
```

---

## Project Validation

The project has been validated through:

- Automated Python unit tests
- Docker image builds
- Trivy security scanning
- Kubernetes manifest validation
- Successful Kubernetes rollouts
- Kubernetes health checks
- Horizontal Pod Autoscaler testing
- Prometheus metric collection
- Grafana dashboard validation
- Controlled HTTP 500 incident testing
- ImagePullBackOff troubleshooting and recovery
- Successful GitHub Actions CI execution
- Successful GitHub Actions CD execution

---

## Future Improvements

Potential future improvements include:

- Deployment to Amazon EKS
- Container image publishing to Amazon ECR
- HTTPS/TLS configuration
- Centralized logging
- Alertmanager integration
- GitOps deployment using Argo CD
- Remote Terraform state management
- Production-grade secrets management using AWS Secrets Manager
- Advanced CI/CD approval and promotion stages
- Infrastructure monitoring and alerting

These are intentionally listed as future improvements and are not required for the current project.

---

## Project Notes

This project is designed as a student portfolio and interview demonstration.

The project intentionally combines local Kubernetes with AWS Infrastructure as Code so that Kubernetes concepts can be demonstrated without requiring a continuously running managed Kubernetes cluster.

The Kubernetes environment uses `kind` instead of Amazon EKS to keep the project cost-controlled.

AWS resources created through Terraform should be destroyed after testing when they are no longer required.

No production credentials or sensitive secrets are stored in the repository.

The Kubernetes Secret included in this project contains only a demonstration value.

---

## Learning Outcomes

This project demonstrates practical experience with:

- Linux and Bash
- Git and GitHub
- Python application development
- Docker
- Kubernetes
- Kubernetes troubleshooting
- Kubernetes health probes
- Kubernetes autoscaling
- ConfigMaps and Secrets
- Ingress
- Terraform
- AWS
- GitHub Actions
- CI/CD
- Container security scanning
- Prometheus
- Grafana
- Incident investigation
- Deployment automation
- Infrastructure as Code

The project focuses not only on deploying an application but also on validating, monitoring, troubleshooting, securing, and automating the deployment lifecycle.

---

## Author

**Rishabh Kumar Singh**

B.Tech — Electronics and Communication Engineering

GitHub:  
https://github.com/rishabhmaurya16105-hash

LinkedIn:  
https://www.linkedin.com/in/rishabh-kumar-singh-7593a9301
