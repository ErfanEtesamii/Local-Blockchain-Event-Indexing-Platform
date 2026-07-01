import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response

from app.api.database import get_connection
from app.api.metrics import REQUEST_COUNT, REQUEST_LATENCY, metrics_response
from app.api.transfers import router as transfers_router

app = FastAPI()

app.include_router(transfers_router)


@app.middleware("http")
async def track_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    path = request.url.path
    REQUEST_LATENCY.labels(method=request.method, path=path).observe(duration)
    REQUEST_COUNT.labels(
        method=request.method, path=path, status_code=response.status_code
    ).inc()

    return response


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


@app.get("/metrics")
def metrics():
    content, content_type = metrics_response()
    return Response(content=content, media_type=content_type)
