# INC-001 — HTTP 500 Application Error

## Incident Summary

A controlled application error was generated on the AWS DevOps Platform Kubernetes deployment to verify application-level error monitoring.

## Environment

- Application: AWS DevOps Platform
- Runtime: Kubernetes (kind)
- Docker image: aws-devops-platform:1.2
- Replicas: 2
- Monitoring: Prometheus + Grafana

## Detection

The `/error` endpoint was intentionally requested and returned:

HTTP/1.1 500 INTERNAL SERVER ERROR

Prometheus detected the resulting HTTP 5xx metric through the application's `/metrics` endpoint.

PromQL query:

sum(rate(http_requests_total{status=~"5.."}[5m]))

Observed value:

0.035 requests/second

## Investigation

The Grafana HTTP status-code dashboard showed HTTP 500 requests.

The Grafana HTTP 5xx Error Rate panel showed a visible spike corresponding to the generated errors.

## Root Cause

The `/error` endpoint is intentionally implemented to return HTTP 500 for controlled failure testing.

This was a simulated application incident used to validate the monitoring pipeline.

## Resolution

No production code fix was required because the HTTP 500 response was intentionally generated for monitoring validation.

The monitoring pipeline successfully detected and visualized the error.

## Verification

The incident was verified through:

1. Kubernetes application endpoint returning HTTP 500.
2. Prometheus recording the HTTP 5xx request rate.
3. Grafana displaying the HTTP 500 status and 5xx error-rate spike.

## Lessons Learned

- Application-level metrics provide visibility into HTTP failures.
- Prometheus can collect custom application metrics.
- Grafana can visualize HTTP error rates.
- Controlled failure testing helps validate monitoring before a real incident.
