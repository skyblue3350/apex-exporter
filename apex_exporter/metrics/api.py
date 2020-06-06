from prometheus_client import Gauge

definitions = {
    "x-ratelimit-limit-minute": "Ratelimit limit minute",
    "x-ratelimit-remaining-minute": "Ratelimit remaining minute",
}

metrics = {}
for label, desc in definitions.items():
    metrics[label] = Gauge(label.replace("-", "_"), desc)
