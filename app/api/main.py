from fastapi import FastAPI, HTTPException

from app.api.database import get_connection
from app.api.transfers import router as transfers_router

app = FastAPI()

app.include_router(transfers_router)


@app.get("/livez")
def livez():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"database is not ready: {exc}")

    return {"status": "ready"}