from prometheus_client import Gauge


metrics = {
    "apex_stats_rank_score": Gauge("apex_stats_rank_score", "Points obtained in ranked battles.", ["player", "rankName"]),
    "apex_stats_season_kill": Gauge("apex_stats_season_kill", "Number of kills during the season.", ["player", "season"]),
    "apex_stats_player_level": Gauge("apex_stats_player_level", "Player level.", ["player"]),
}