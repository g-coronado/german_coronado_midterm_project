import pandas as pd
from pathlib import Path
from objects import Player, Lineup

FILENAME = Path(__file__).parent / "players.csv"
VALID_POSITIONS = ('C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P')


def db_load_players():
    try:
        df = pd.read_csv(FILENAME, header=None)
        lineup = Lineup()

        for _, row in df.iterrows():
            first = row[0]
            last = row[1]
            position = row[2]
            at_bats = int(row[3])
            hits = int(row[4])

            player = Player(first, last, position, at_bats, hits)
            lineup.add_player(player)
        return lineup
    except:
        print('Error loading player data from file. Please check the file location and structure, and try again.')


def update_file(lineup: Lineup):
    rows = []
    for p in lineup:
        rows.append([
            p.first_name,
            p.last_name,
            p.position,
            p.at_bats,
            p.hits
        ])

    to_update = pd.DataFrame(rows)
    to_update.to_csv(FILENAME, index=False, header=False)


def db_add_player(lineup: Lineup, player: Player):
    lineup.add_player(player)
    update_file(lineup)


def db_remove_player(lineup: Lineup, lineup_to_delete: int):
    player = lineup.players[lineup_to_delete]
    lineup.remove_player(player)
    update_file(lineup)
    return player


def db_move_player(lineup: Lineup, old_index: int, new_index: int):
    player = lineup.players[old_index]
    lineup.move_player(player, new_index)
    update_file(lineup)
    return player


def db_edit_player_position(lineup: Lineup, index: int, new_position: str):
    player = lineup.players[index]
    lineup.edit_player_position(player, new_position)
    update_file(lineup)
    return player


def db_edit_player_stats(lineup: Lineup, index: int, new_ab: int, new_hits: int):
    player = lineup.players[index]
    lineup.edit_player_stats(player, new_ab, new_hits)
    update_file(lineup)
    return player