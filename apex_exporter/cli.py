import os
import sys

import requests
from prometheus_client import Summary
from prometheus_client.exposition import generate_latest
from flask import Flask, request, abort, Response

from apex_exporter.metrics.api import metrics as api_metrics
from apex_exporter.metrics.player_stats import metrics as player_metrics


app = Flask(__name__)

APEX_REQUEST_TIME = Summary(
    "apex_request_time",
    "Time spent processing applianceses request")


def get_headers(token):
    return {
        "accept": "application/json",
        "TRN-Api-Key": token,
    }


def update_api_info(headers):
    for header in api_metrics:
        api_metrics[header].set(headers[header])


@APEX_REQUEST_TIME.time()
def apex_process_request(platform, name):
    token = app.config["TOKEN"]

    url = "https://public-api.tracker.gg/v2/apex/standard/profile/{platform}/{name}".format(
        platform=platform,
        name=name)
    res = requests.get(url, headers=get_headers(token))

    data = res.json()
    if "data" not in data:
        print(data, file=sys.stderr)
    data = data["data"]
    player_name = data["platformInfo"]["platformUserId"]

    for segment in data["segments"]:
        metadata = segment["metadata"]
        if metadata["name"] == "Lifetime":
            player_metrics["apex_stats_player_level"].labels(player_name).set(
                segment["stats"]["level"]["value"])
            player_metrics["apex_stats_rank_score"].labels(
                player_name,
                segment["stats"]["rankScore"]["metadata"]["rankName"]
            ).set(segment["stats"]["rankScore"]["value"])

            for key in segment["stats"]:
                if not "season" in key:
                    continue

                player_metrics["apex_stats_season_kill"].labels(
                    player_name,
                    key,
                ).set(segment["stats"][key]["value"])

    update_api_info(res.headers)


@app.route("/metrics")
def metrics():
    platform = request.args.get("platform")
    name = request.args.get("name")

    if platform is None or name is None:
        abort(400)

    apex_process_request(platform, name)

    return Response(generate_latest(), mimetype="text/plain; version=0.0.4; charset=utf-8")


def main(port=9316):
    token = os.environ.get("TOKEN", None)
    if token is None:
        raise RuntimeError("Required: TOKEN environment")
    app.config["TOKEN"] = token

    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
