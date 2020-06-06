# apex-exporter

Exporter for APEX (datasource: https://apex.tracker.gg/)

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
