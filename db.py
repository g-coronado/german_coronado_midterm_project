import pandas as pd
from pathlib import Path
import sqlite3
from contextlib import closing

from objects import Player


# Global connection object
# Only one connection is maintained during program execution
conn = None
VALID_POSITIONS = ('C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P')

def connect():
    global conn

    if conn:
        return

    try:
        db_path = Path(__file__).parent / "players.db"
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")
        conn = None
        return False

    return True


def close():

    if conn:
        conn.close()



def make_player(row):
    """
    Convert a database row into a Player object.

    Returns
    -------
    Player
        A Player object populated with database values.
    """
    return Player(
        row["playerID"],
        row["batOrder"],
        row["firstName"],
        row["lastName"],
        row["position"],
        row["atBats"],
        row["hits"]
    )    

def make_player_list(results):
    players = []

    for row in results:
        players.append(make_player(row))
    
    return players

def get_players():
    connect()

    query = """
        SELECT playerID, batOrder, firstName, lastName, position,
               atBats, hits
        FROM Player
    """
    with closing(conn.cursor()) as c:
        c.execute(query)
        results = c.fetchall()    
    return make_player_list(results)


def db_add_player(player):
    if not connect():
        return False 

    sql_check = "SELECT playerID FROM Player WHERE playerID = ?"
    with closing(conn.cursor()) as c:
        c.execute(sql_check, (player.playerID,))
        exists = c.fetchone()

    if exists:
        return False  

    sql_insert = """
        INSERT INTO Player (playerID, batOrder, firstName, lastName, position, atBats, hits)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    with closing(conn.cursor()) as c:
        c.execute(sql_insert, (
            player.playerID,
            player.batOrder,
            player.firstName,
            player.lastName,
            player.position,
            player.atBats,
            player.hits
        ))
        conn.commit()

        return c.rowcount == 1
    

def db_remove_player(player_id):
    if not connect():
        return False 

    sql = "DELETE FROM Player WHERE playerID = ?"

    with closing(conn.cursor()) as c:
        c.execute(sql, (player_id,))
        deleted = c.rowcount
        conn.commit()

    return deleted > 0


def db_edit_player_position(player_id, position):
    if not connect():
        return False

    sql = """
        UPDATE Player
        SET position = ?
        WHERE playerID = ?
    """

    with closing(conn.cursor()) as c:
        c.execute(sql, (position, player_id))
        updated = c.rowcount
        conn.commit()

    return updated > 0


def db_edit_player_stats(player_id, new_ab, new_hits):
    if not connect():
        return False

    sql = """UPDATE Player
        SET atBats = ?, hits = ?
        WHERE playerID = ?"""

    with closing(conn.cursor()) as c:
        c.execute(sql, (new_ab, new_hits, player_id))
        updated = c.rowcount
        conn.commit()
    
    return updated > 0


def db_move_player(player_id, new_bat_order):
    if not connect():
        return False

    sql_get_old = "SELECT batOrder FROM Player WHERE playerID = ?"
    with closing(conn.cursor()) as c:
        c.execute(sql_get_old, (player_id,))
        row = c.fetchone()

    if row is None:
        return False 

    old_bat_order = row["batOrder"]

    if old_bat_order == new_bat_order:
        return True

    with closing(conn.cursor()) as c:

        if new_bat_order < old_bat_order:
            sql_move = """
                UPDATE Player
                SET batOrder = batOrder + 1
                WHERE batOrder >= ? AND batOrder < ? AND playerID != ?;
            """
            c.execute(sql_move, (new_bat_order, old_bat_order, player_id))

        else:
            sql_move = """
                UPDATE Player
                SET batOrder = batOrder - 1
                WHERE batOrder <= ? AND batOrder > ? AND playerID != ?;
            """
            c.execute(sql_move, (new_bat_order, old_bat_order, player_id))

        sql_update = "UPDATE Player SET batOrder = ? WHERE playerID = ?"
        c.execute(sql_update, (new_bat_order, player_id))

        conn.commit()

    return True