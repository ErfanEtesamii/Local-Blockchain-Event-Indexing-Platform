import os

from fastapi import FastAPI, HTTPException
from psycopg2 import connect
from psycopg2.errors import OperationalError

app = FastAPI()


@app.get("/livez")
def livez():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise HTTPException(status_code=503, detail="DATABASE_URL is not set")

    try:
        conn = connect(database_url)
        conn.close()
    except OperationalError:
        raise HTTPException(status_code=503, detail="database is not ready")

    return {"status": "ready"}