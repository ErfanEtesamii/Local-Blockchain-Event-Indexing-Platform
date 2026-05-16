# Local Blockchain Event Indexing Platform

## Overview

This project is a local-first blockchain event indexing platform that collects, stores, and exposes blockchain transfer events through a backend API service. It is designed to run in a self-contained development environment built around Docker, Kubernetes (`kind`), PostgreSQL, and local containerized services.

The current implementation focuses on a practical local workflow for building and validating the indexing pipeline before expanding the project into broader infrastructure and observability stages.

## Goals

- Build a fully local blockchain event indexing platform.
- Store normalized blockchain transfer events in PostgreSQL.
- Expose indexed data through a backend API.
- Use Docker and `kind` for a reproducible local Kubernetes workflow.
- Keep the project structured for gradual, commit-by-commit progress.

## Prerequisites

Install the following tools before running the project:

### Docker

Used for building and running local containers.

- Download: [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### kubectl

Used to interact with the Kubernetes cluster.

On Windows:

```bash
winget install Kubernetes.kubectl
```

### kind

Used to create a local Kubernetes cluster inside Docker.

- Download: [kind Quick Start](https://kind.sigs.k8s.io/docs/user/quick-start/)

### PostgreSQL

Used as the primary relational database for storing indexed blockchain transfer events.

pgAdmin can also be used for schema inspection, query execution, and manual validation.

## Environment Verification

After installation, verify the local environment with:

```bash
docker --version
kubectl version --client
kind --version
```

## Getting Started

### 1. Create the local Kubernetes cluster

```bash
kind create cluster --name local-blockchain
kubectl get nodes
```

### 2. Build the application images

#### Build indexer image

```bash
docker build -t my-indexer ./app/indexer
```

#### Build API image

```bash
docker build -t my-api ./app/api
```

### 3. Load local images into the `kind` cluster

```bash
kind load docker-image my-indexer --name local-blockchain
kind load docker-image my-api --name local-blockchain
```

### 4. Deploy the infrastructure

```bash
kubectl apply -k infra/k8s/base/
```

### 5. Verify deployments

```bash
kubectl get pods
```

Expected core services:

- `postgres`
- `api`
- `indexer`

## Database Layer

PostgreSQL is used as the main storage layer for indexed blockchain transfer events.

### Current table

The current table is `token_transfers`, which stores:

- `tx_hash`
- `block_number`
- `event_index`
- `from_address`
- `to_address`
- `token_address`
- `amount`
- `status`
- `processed_at`
- `created_at`

## Schema Setup

The initial database schema is stored in:

```text
infra/db/schema.sql
```

The schema currently creates:

- The `token_transfers` table
- An index on `block_number`
- An index on `token_address`
- An index on `from_address`
- An index on `to_address`

## Current Application Flow

The current local application flow is:

1. The indexer fetches transfer events from a source module.
2. The processor normalizes the event payload.
3. The normalized record is written into PostgreSQL.
4. The API reads stored records from `token_transfers`.
5. The `/transfers` endpoint exposes the stored data.

At this stage, the blockchain client is still using a mock event source, which is intentional for validating the local end-to-end pipeline before integrating a real blockchain source.

## Progress So Far

Completed work so far includes:

- Defined the project scope and architecture
- Designed the PostgreSQL database schema
- Installed and configured PostgreSQL locally
- Created and executed the `token_transfers` schema
- Verified database connectivity
- Inserted and validated test records
- Added PostgreSQL to the Kubernetes cluster
- Created Kubernetes manifests for PVC, Deployment, Service, Secret, and `kustomization.yaml`
- Built the API and indexer Docker images locally
- Loaded local images into the `kind` cluster
- Verified local Docker and Kubernetes integration
- Built a FastAPI backend connected to PostgreSQL
- Added health-aware API endpoints and Kubernetes probes
- Added logging to the indexer flow
- Built and ran the indexer in Docker
- Fixed runtime `DATABASE_URL` handling
- Validated that the indexer can write transfer rows into PostgreSQL
- Confirmed the end-to-end source → processor → database → API flow

## Today’s Progress

Today’s work focused on cleanup, code correction, and local verification rather than adding new features.

### Changes completed today

- Cleaned up the API and indexer code paths
- Fixed code-level execution issues and made the local modules runnable
- Verified that `python -m app.indexer.main` runs successfully
- Verified that the indexer writes transfer data into `token_transfers`
- Verified that the FastAPI service starts successfully with Uvicorn
- Verified that `GET /transfers` returns stored transfer records correctly
- Confirmed the local ingestion → database write → API query flow again after code fixes

### Result

The project now has a runnable local API and a runnable local indexer, and the `/transfers` endpoint successfully returns stored records from PostgreSQL.

## Issues Encountered

Several issues were encountered during setup and validation:

- PostgreSQL initially entered `Pending` / `ImagePullBackOff` because of Docker Hub connectivity and network instability
- The local workflow was adjusted to rely more on locally built images loaded into `kind`
- The indexer initially failed because `DATABASE_URL` was not being passed correctly at runtime
- API and indexer code required cleanup and correction before the local execution path became stable

### Local-first workaround

To reduce dependency on external image pulls and improve local reliability, the workflow was shifted toward:

- locally building Docker images,
- loading them into `kind`,
- validating services in a local-first development loop.

## Current Infrastructure Status

At the current stage, the project includes:

- A running local Kubernetes cluster
- PostgreSQL running in Kubernetes
- Local API and indexer images loaded into `kind`
- Kubernetes manifests for PostgreSQL and application deployment
- A working PostgreSQL schema for blockchain transfer storage
- A working FastAPI backend connected to PostgreSQL
- A working initial indexing pipeline that writes transfer records into the database
- A local Docker execution path for the indexer
- Health-aware Kubernetes manifests for API and PostgreSQL
- Separate manifest files for Secret, Service, and workload resources

## Repository Structure

```text
.
├── README.md
├── .env
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── schemas.py
│   │   └── transfers.py
│   └── indexer/
│       ├── __init__.py
│       ├── main.py
│       ├── processor.py
│       └── blockchain_client.py
├── infra/
│   ├── db/
│   │   └── schema.sql
│   └── k8s/
│       └── base/
│           ├── namespace.yaml
│           ├── postgres-configmap.yaml
│           ├── postgres-secret.yaml
│           ├── postgres-pv.yaml
│           ├── postgres-pvc.yaml
│           ├── postgres-deployment.yaml
│           ├── postgres-service.yaml
│           ├── api-deployment.yaml
│           ├── api-service.yaml
│           ├── indexer-deployment.yaml
│           ├── indexer-service.yaml
│           ├── ingress.yaml
│           └── kustomization.yaml
├── scripts/
│   ├── init_db.sql
│   └── seed_test_data.sql
└── docs/
    ├── architecture.md
    └── deployment.md
```

## Local Verification Commands

### Run the indexer locally

```bash
python -m app.indexer.main
```

### Run the API locally

```bash
uvicorn app.api.main:app --reload
```

### Verify the API

```bash
curl http://127.0.0.1:8000/livez
curl http://127.0.0.1:8000/readyz
curl http://127.0.0.1:8000/transfers
```

## Next Steps

The next phase of development includes:

- Finalizing Kubernetes manifests for fully local deployments
- Running all services entirely from local Docker images
- Expanding the blockchain event indexing functionality
- Adding more API endpoints for querying indexed blockchain data
- Improving the indexer with retries and stronger duplicate handling
- Moving runtime configuration into a cleaner environment-based setup
- Verifying readiness and liveness behavior inside the local cluster
