from fastapi import FastAPI
from app.api.transfers import router as transfers_router

app = FastAPI(title="Blockchain Indexer API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(transfers_router)