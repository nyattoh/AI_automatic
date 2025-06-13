from prometheus_client import Counter, CollectorRegistry, generate_latest

registry = CollectorRegistry()
cc_tokens_total = Counter(
    "cc_tokens_total",
    "Consumed tokens",
    ["role"],
    registry=registry,
)
cc_requests_total = Counter(
    "cc_requests_total",
    "Processed requests",
    ["role"],
    registry=registry,
)


def render_metrics() -> bytes:
    return generate_latest(registry)
