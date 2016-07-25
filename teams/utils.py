from teams.models import pink_tie_teams


def teams_get_rankings():
    """
    Returns a list of tuples that contain (rank, team) tuple for
    each team.
    """
    team_data_map = {}
    for team in pink_tie_teams():
        score = team.score
        if score not in team_data_map:
            team_data_map[score] = []
        team_data_map[score].append(team)

    rankings = []
    for idx, (_, teams) in enumerate(sorted(team_data_map.items(), reverse=True), start=1):
        for team in teams:
            rankings.append((idx, team))
    return rankings
