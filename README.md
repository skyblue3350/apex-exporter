# apex-exporter

Exporter for APEX (datasource: https://apex.tracker.gg/)

## install
```bash
pip install https://github.com/skyblue3350/apex-exporter
```

## dev
```bash
poetry install
poetry run python -m apex-exporter
```

## run as exporter
get token: https://tracker.gg/developers/apps

```bash
export TOKEN=${TRN_APEX_TOKEN_HERE}
docker-compose up -d --build
curl http://localhost:9316/metrics?name=${PLAYER_NAME}&platform=${PLATFORM}
```

## Prometheus Config
```yaml
  - job_name: apex
    scrape_interval: 5s #api limit 30s/token
    metrics_path: /metrics
    params:
      platform: ["origin"]
    static_configs:
      - targets:
        - player-A
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: target
      - target_label: __address__
        replacement: apex-exporter:9316
```
