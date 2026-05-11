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

```text
https://www.docker.com/products/docker-desktop/
```

### kubectl

I use `kubectl` to interact with my Kubernetes cluster.

On Windows, I installed it with:

```bash
winget install Kubernetes.kubectl
```

### kind

I use `kind` to run a local Kubernetes cluster inside Docker.

I downloaded the binary from:

```text
https://kind.sigs.k8s.io/docs/user/quick-start/
```

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
kubectl apply -f infra/k8s/base/
```

### Verify Deployments

I check the running pods with:

```bash
kubectl get pods
```

I expect these core services to run:

- `indexer-deployment`
- `api-deployment`
- PostgreSQL deployment

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
  - a PostgreSQL Service.
- Built the API and indexer Docker images locally.
- Loaded local images into the `kind` cluster successfully.
- Verified local Docker and Kubernetes integration.
- Built a FastAPI backend and connected it to PostgreSQL.
- Created a working `/health` endpoint.
- Created a working `/transfers` endpoint.
- Fixed PostgreSQL authentication issues for `indexer_user`.
- Confirmed the API can read data from PostgreSQL successfully.

---

## Issues I Encountered

During deployment verification, the PostgreSQL pod initially remained in `Pending` state due to an `ImagePullBackOff` error caused by Docker Hub connectivity issues and network instability.

To avoid repeated external downloads, I switched to a local-first workflow by using locally built Docker images and loading them directly into the `kind` cluster.

This approach:

- reduces internet dependency,
- speeds up deployments,
- improves local development reliability.

---

## Current Infrastructure Status

At this stage, my infrastructure includes:

- A running local Kubernetes cluster.
- PostgreSQL configured inside Kubernetes.
- Local API and indexer images loaded into `kind`.
- Kubernetes manifests for infrastructure deployment.
- A functional PostgreSQL schema for blockchain event storage.
- A working FastAPI backend connected to PostgreSQL.

---

## Today’s Progress

Today, I focused on the backend API foundation and validated end-to-end communication with PostgreSQL.

### What I did today

- I organized my project structure under `app/api` and `app/indexer`.
- I created the initial FastAPI application.
- I added PostgreSQL database connection logic.
- I created the `token_transfers` endpoint.
- I fixed PostgreSQL authentication issues for `indexer_user`.
- I confirmed that the schema was applied successfully.
- I inserted a test blockchain transfer record into the database.
- I verified the database content through `psql`.
- I ran the FastAPI server locally with `uvicorn`.
- I tested the `/health` endpoint successfully.
- I tested the `/transfers` endpoint successfully through Swagger UI.
- I reached a working `200 OK` response from the API after fixing database credentials.

### Result

My local API is now connected to PostgreSQL and can read indexed blockchain transfer data successfully.

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

- Connecting the backend API service to PostgreSQL in the Kubernetes environment.
- Finalizing Kubernetes manifests for fully local deployments.
- Running all services entirely from local Docker images.
- Expanding the blockchain event indexing functionality.
- Adding more API endpoints for querying indexed blockchain data.