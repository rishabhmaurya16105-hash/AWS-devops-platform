# INC-002 — Kubernetes ImagePullBackOff

## Incident Summary

A controlled deployment failure was introduced in the AWS DevOps Platform Kubernetes deployment by updating the application image from the known-good version 1.2 to the unavailable image 999.

The purpose of this exercise was to validate Kubernetes troubleshooting and recovery procedures.

## Environment

- Application: AWS DevOps Platform
- Runtime: Kubernetes (kind)
- Previous known-good image: aws-devops-platform:1.2
- Faulty image: aws-devops-platform:999
- Replicas: 2
- Monitoring: Prometheus + Grafana

## Detection

After the deployment image was changed to aws-devops-platform:999, Kubernetes created a new pod with the following status:

0/1 ImagePullBackOff

The existing application pods remained healthy:

1/1 Running

## Investigation

The failed pod was inspected using:

kubectl describe pod <failed-pod>

The Kubernetes events showed that the node could not pull:

aws-devops-platform:999

The image pull failed because the image was unavailable from the configured container registry.

Kubernetes subsequently reported:

- ErrImagePull
- ImagePullBackOff

The deployment rollout was also checked using:

kubectl rollout status deployment/aws-devops-platform --timeout=10s

The rollout timed out because the new replica could not become Ready.

## Root Cause

The Kubernetes Deployment referenced the unavailable container image:

aws-devops-platform:999

The known-good image was:

aws-devops-platform:1.2

Because the 999 image was unavailable, Kubernetes could not start the new application pod.

## Recovery

A Kubernetes rollback was initially attempted:

kubectl rollout undo deployment/aws-devops-platform

The deployment was then inspected and was still referencing:

aws-devops-platform:999

The known-good image was explicitly restored using:

kubectl set image deployment/aws-devops-platform aws-devops-platform:1.2

## Verification

The deployment rollout completed successfully:

deployment "aws-devops-platform" successfully rolled out

The application pods returned to:

2/2 Running

The final deployment image was verified as:

aws-devops-platform:1.2

## Lessons Learned

- ImagePullBackOff indicates that Kubernetes cannot successfully obtain the requested container image.
- kubectl describe pod and Kubernetes events provide important troubleshooting information.
- Deployment rollout status helps identify when a new version cannot become Ready.
- ReplicaSet inspection helps distinguish the failed rollout from the previously healthy version.
- A known-good container image provides a reliable recovery point.
- After recovery, the actual Deployment image and pod health should be verified.
