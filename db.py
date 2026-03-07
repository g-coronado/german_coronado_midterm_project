import sqlite3
from pathlib import Path
from tkinter import messagebox
from contextlib import closing

from objects import Player

conn = None


def connect():
    """
    Establishes a connection to the SQLite database if not already connected.

    The database file is expected to be located in the same directory as this
    module under the name 'players.db'. The connection uses `sqlite3.Row` to
    allow dictionary-style column access.

    Returns
    -------
    bool
        True if the connection is successfully established or already active,
        False if the connection attempt fails.
    """
    global conn

    if conn is not None:
        return True

    try:
        db_path = Path(__file__).parent / "players.db"
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return True

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Database connection failed:\n{e}")
        conn = None
        return False


def close():
    """
    Closes the active database connection if one exists.

    This function should be called when the application is shutting down
    to ensure the SQLite connection is properly released.
    """
    if conn:
        conn.close()



def make_player(row):
    """
    Converts a database row into a Player object.

    Parameters
    ----------
    row : sqlite3.Row
        A row returned from a SELECT query on the Player table.

    Returns
    -------
    Player
        A Player instance populated with the row's values.
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
    """
    Converts a list of database rows into a list of Player objects.

    Parameters
    ----------
    results : list[sqlite3.Row]
        Rows returned from a SELECT query.

    Returns
    -------
    list[Player]
        A list of Player objects.
    """
    players = []

    for row in results:
        players.append(make_player(row))

    return players


def get_players():
    """
    Retrieves all players from the database.

    Returns
    -------
    list[Player]
        A list of all players stored in the Player table.
    """
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
    """
    Inserts a new player into the database.

    Parameters
    ----------
    player : Player
        The Player object containing the data to insert.

    Returns
    -------
    bool
        True if the insertion succeeds, False otherwise.
    """
    if not connect():
        return False

    sql_insert = """
        INSERT INTO Player (batOrder, firstName, lastName, position, atBats, hits)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    try:
        with closing(conn.cursor()) as c:
            c.execute(sql_insert, (
                player.batOrder,
                player.firstName,
                player.lastName,
                player.position,
                player.atBats,
                player.hits
            ))

            player.playerID = c.lastrowid
            conn.commit()

            return c.rowcount == 1

    except Exception as e:
        messagebox.showerror("SQL Error", f"Failed to insert player:\n{e}")
        return False


def db_remove_player(player_id):
    """
    Deletes a player from the database by ID.

    Parameters
    ----------
    player_id : int
        The unique ID of the player to remove.

    Returns
    -------
    bool
        True if a row was deleted, False otherwise.
    """
    if not connect():
        return False

    sql = "DELETE FROM Player WHERE playerID = ?"

    try:
        with closing(conn.cursor()) as c:
            c.execute(sql, (player_id,))
            conn.commit()
            return c.rowcount == 1

    except Exception as e:
        messagebox.showerror("SQL Error", f"Failed to delete player:\n{e}")
        return False


def db_edit_player_position(player_id, position):
    """
    Updates the defensive position of a player.

    Parameters
    ----------
    player_id : int
        The player's unique identifier.
    position : str
        The new position abbreviation.

    Returns
    -------
    bool
        True if at least one row was updated, False otherwise.
    """
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
    """
    Updates a player's batting statistics.

    Parameters
    ----------
    player_id : int
        The player's unique identifier.
    new_ab : int
        Updated number of at-bats.
    new_hits : int
        Updated number of hits.

    Returns
    -------
    bool
        True if the update affected at least one row, False otherwise.
    """
    if not connect():
        return False

    sql = """
        UPDATE Player
        SET atBats = ?, hits = ?
        WHERE playerID = ?
    """

    with closing(conn.cursor()) as c:
        c.execute(sql, (new_ab, new_hits, player_id))
        updated = c.rowcount
        conn.commit()

    return updated > 0


def db_move_player(player_id, new_bat_order):
    """
    Reorders a player's batting position and shifts other players accordingly.

    This function ensures that the batting order remains continuous and
    conflict-free by shifting other players up or down depending on the
    direction of the move.

    Parameters
    ----------
    player_id : int
        The ID of the player being moved.
    new_bat_order : int
        The new batting order position.

    Returns
    -------
    bool
        True if the move was successful, False otherwise.
    """
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


def get_player_by_id(player_id):
    """
    Retrieves a single player by ID.

    Parameters
    ----------
    player_id : int
        The unique identifier of the player.

    Returns
    -------
    Player or None
        A Player object if found, otherwise None.
    """
    connect()

    query = """
        SELECT playerID, batOrder, firstName, lastName, position, atBats, hits
        FROM Player
        WHERE playerID=?
    """

    with closing(conn.cursor()) as c:
        c.execute(query, (player_id,))
        row = c.fetchone()

        if row is None:
            return None

    return make_player(row)


def get_all_positions():
    """
    Retrieves all valid defensive positions from the POSITION table.

    Returns
    -------
    list[str]
        A list of position names sorted alphabetically.
    """
    connect()
    query = "SELECT positionName FROM POSITION ORDER BY positionName;"

    with closing(conn.cursor()) as c:
        c.execute(query)
        return [row[0] for row in c.fetchall()]



def debug_print_schema():
    """
    Prints the schema of the Player table to the console.

    This function is intended for debugging and development use only.
    """
    connect()
    with closing(conn.cursor()) as c:
        c.execute("PRAGMA table_info(Player)")
        rows = c.fetchall()
        for r in rows:
            print(tuple(r))
            