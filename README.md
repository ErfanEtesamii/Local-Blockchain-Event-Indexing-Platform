# Local-Blockchain-Event-Indexing-Platform

## Project Overview

I am building a local blockchain event indexing platform that collects, stores, and exposes blockchain transfer events through a backend API service.

I built the infrastructure around:

- Kubernetes (`kind`)
- Docker
- PostgreSQL
- Local containerized services

My goal is to create a fully local-first development environment for indexing blockchain events and exposing them through scalable backend services.

---

## Prerequisites

To get started with this project, I installed the following tools on my local machine.

### Docker

I use Docker to build and run the application containers.

I installed Docker Desktop from:

[https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)

### kubectl

I use `kubectl` to interact with my Kubernetes cluster.

On Windows, I installed it with:

```bash
winget install Kubernetes.kubectl
```

### kind

I use `kind` to run a local Kubernetes cluster inside Docker.

I downloaded the binary from:

[https://kind.sigs.k8s.io/docs/user/quick-start/](https://kind.sigs.k8s.io/docs/user/quick-start/)

### PostgreSQL

I use PostgreSQL as the primary relational database for storing indexed blockchain events.

I use pgAdmin for graphical database management, query execution, and schema inspection.

---

## Environment Verification

After installing the required tools, I verified my setup with:

```bash
docker --version
kubectl version --client
kind --version
```

---

## Getting Started

### Create the Local Kubernetes Cluster

I initialize the cluster using `kind`:

```bash
kind create cluster --name local-blockchain
```

Then I verify the cluster status:

```bash
kubectl get nodes
```

### Build the Application Containers

I build the Docker images for the indexer and API services.

#### Build Indexer

```bash
docker build -t my-indexer ./app/indexer
```

#### Build API

```bash
docker build -t my-api ./app/api
```

### Load Images into the kind Cluster

I load the local Docker images into the Kubernetes cluster:

```bash
kind load docker-image my-indexer --name local-blockchain
kind load docker-image my-api --name local-blockchain
```

### Deploy the Infrastructure

I deploy the Kubernetes manifests using:

```bash
kubectl apply -k infra/k8s/base/
```

### Verify Deployments

I check the running pods with:

```bash
kubectl get pods
```

I expect these core services to run:

- `indexer`
- `api`
- `postgres`

---

## Database Layer

I configured PostgreSQL as the main database for storing indexed blockchain transfer events.

### Current Table

I use the `token_transfers` table for blockchain event storage.

The table includes:

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

---

## Schema Setup

I stored my initial database schema in:

```text
infra/db/schema.sql
```

The schema creates:

- the `token_transfers` table,
- indexes on:
  - block number,
  - token address,
  - sender address,
  - receiver address.

---

## Progress So Far

So far, I have:

- Defined the project scope and architecture.
- Designed the PostgreSQL database schema.
- Installed and configured PostgreSQL locally.
- Created the `token_transfers` table.
- Executed the schema successfully.
- Verified database connectivity.
- Inserted and validated test records.
- Added PostgreSQL to the Kubernetes cluster.
- Created:
  - a PersistentVolumeClaim,
  - a PostgreSQL Deployment,
  - a PostgreSQL Service,
  - a PostgreSQL Secret,
  - and Kubernetes manifests organized with `kustomization.yaml`.
- Built the API and indexer Docker images locally.
- Loaded local images into the `kind` cluster successfully.
- Verified local Docker and Kubernetes integration.
- Built a FastAPI backend and connected it to PostgreSQL.
- Created a working `/health` endpoint.
- Added Kubernetes health endpoints for service readiness and liveness.
- Separated PostgreSQL configuration into dedicated manifest files.
- Added logging to the indexer flow.
- Built and ran the indexer inside Docker.
- Fixed the `DATABASE_URL` issue by passing the environment variable at runtime.
- Started the indexer pipeline and validated that it can write new transfer data into `token_transfers`.
- Confirmed the end-to-end flow from source to processor to database to API.

---

## Issues I Encountered

During deployment verification, the PostgreSQL pod initially remained in `Pending` state due to an `ImagePullBackOff` error caused by Docker Hub connectivity issues and network instability.

To avoid repeated external downloads, I switched to a local-first workflow by using locally built Docker images and loading them directly into the `kind` cluster.

This approach:

- reduces internet dependency,
- speeds up deployments,
- improves local development reliability.

I also encountered a Docker runtime issue where the indexer container could not find `DATABASE_URL` until I passed it explicitly at runtime.

---

## Current Infrastructure Status

At this stage, my infrastructure includes:

- A running local Kubernetes cluster.
- PostgreSQL configured inside Kubernetes.
- Local API and indexer images loaded into `kind`.
- Kubernetes manifests for infrastructure deployment.
- A functional PostgreSQL schema for blockchain event storage.
- A working FastAPI backend connected to PostgreSQL.
- A working initial indexing pipeline that can write blockchain transfer records into the database.
- A Dockerized indexer that can run locally with runtime environment configuration.
- Health-aware Kubernetes manifests for the API and PostgreSQL.
- Separate Kubernetes files for `Secret`, `Service`, and workload resources.

---

## Today’s Progress

Today, I focused on making the indexer pipeline runnable inside Docker and validating the end-to-end data flow again.

### What I did today

- I added logging to the indexer flow.
- I cleaned up the indexer execution path.
- I built the indexer Docker image successfully.
- I ran the indexer container locally.
- I debugged the missing `DATABASE_URL` issue.
- I passed the correct PostgreSQL connection string at runtime.
- I verified that the indexer container ran successfully.
- I confirmed that a new row was written into `token_transfers`.
- I re-checked the table contents from PostgreSQL.
- I confirmed that the full source → processor → database flow works inside Docker.
- I reorganized the Kubernetes manifests into separate files for PostgreSQL deployment, service, and secret.
- I updated the Kubernetes structure to be more local-first and easier to maintain.
- I prepared the cluster manifests for readiness/liveness handling.

### Result

My indexer is now runnable inside Docker, and it can write blockchain transfer data into PostgreSQL successfully.

---

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

---

## Next Steps

The next phase of development includes:

- Finalizing Kubernetes manifests for fully local deployments.
- Running all services entirely from local Docker images.
- Expanding the blockchain event indexing functionality.
- Adding more API endpoints for querying indexed blockchain data.
- Improving the indexer with retries and duplicate handling.
- Moving the indexer runtime configuration into a cleaner `.env`-based setup.
- Verifying health probes and readiness behavior in the local cluster.