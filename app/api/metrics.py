from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "path", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "API request duration in seconds",
    ["method", "path"],
)


def metrics_response():
    return generate_latest(), CONTENT_TYPE_LATEST
