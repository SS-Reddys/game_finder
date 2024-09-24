from collections import defaultdict

def find_qualified_games(game_data: list[dict], true_shooting_cutoff: int, player_count: int) -> list[int]:
    # Function to calculate true shooting percentage for a player
    def calculate_true_shooting(player_data):
        # Calculate points scored
        points = 2 * player_data['fieldGoal2Made'] + 3 * player_data['fieldGoal3Made'] + player_data['freeThrowMade']
        # Calculate total shooting attempts
        total_attempts = player_data['fieldGoal2Attempted'] + player_data['fieldGoal3Attempted'] + 0.44 * player_data['freeThrowAttempted']
        if total_attempts == 0:
            return 0
        # Calculate TS% using the formula
        return (points / (2 * total_attempts)) * 100

    # Group player data by gameID
    game_players = defaultdict(list)
    game_dates = {}  # To store the date of each gameID for sorting purposes

    for entry in game_data:
        gameID = entry['gameID']
        ts_percentage = calculate_true_shooting(entry)
        game_players[gameID].append(ts_percentage)
        game_dates[gameID] = entry['gameDate']

    qualified_games = []

    # For each game, count how many players have TS% >= true_shooting_cutoff
    for gameID, ts_percentages in game_players.items():
        qualified_players = sum(1 for ts in ts_percentages if ts >= true_shooting_cutoff)
        if qualified_players >= player_count:
            qualified_games.append(gameID)

    # Sort the qualified gameIDs by most recent gameDate (descending order)
    qualified_games.sort(key=lambda gid: game_dates[gid], reverse=True)

    return qualified_games
