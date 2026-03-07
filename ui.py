import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import db
from objects import Player

"""
Baseball Team Manager Application
This module provides a GUI and Controller for managing a baseball team lineup,
tracking player statistics, and calculating game countdowns.
"""

# =====================================================
# Controller Layer
# =====================================================

class PlayerController:
    """
    Handles business logic and database interactions for Player objects.
    
    This controller acts as a bridge between the User Interface and the 
    data access layer (db.py), managing the local state of the player list.
    """
    def __init__(self):
        """Initialize the controller by fetching all players from the database."""
        self.players = db.get_players()

    def add_player(self, player):
        """
        Add a new player to the database and update the local player list.

        Args:
            player (Player): An instance of the Player class containing player data.

        Returns:
            bool: True if the database insertion was successful, False otherwise.
        """
        success = db.db_add_player(player)
        if success:
            self.players.append(player)
        return success

    def reload_players(self):
        """Synchronize the local players list with the current database state."""
        self.players = db.get_players()

    def remove_player(self, playerID):
        """
        Remove a player from the database and local list by their ID.

        Args:
            playerID (int): The unique identifier of the player to remove.

        Returns:
            bool: True if removal was successful.
        """
        success = db.db_remove_player(playerID)
        if success:
            self.players = [p for p in self.players if p.playerID != playerID]
        return success
    
    def edit_player_stats(self, player: Player):
        """
        Update the At Bats and Hits for an existing player record.

        Args:
            player (Player): Player object containing the ID and updated stats.

        Returns:
            bool: True if the database update succeeded.
        """
        existing = db.get_player_by_id(player.playerID)
        if existing is None:
            return False

        return db.db_edit_player_stats(
            player.playerID,
            player.atBats,
            player.hits
        )

    def edit_player_position(self, player: Player):
        """
        Update the defensive position for an existing player.

        Args:
            player (Player): Player object containing the ID and new position.

        Returns:
            bool: True if the position update succeeded.
        """
        existing = db.get_player_by_id(player.playerID)
        if existing is None:
            return False

        return db.db_edit_player_position(
            player.playerID,
            player.position
        )

    def edit_player_order(self, player: Player):
        """
        Update the batting order position for a player.

        Args:
            player (Player): Player object containing the ID and new batOrder.

        Returns:
            bool: True if the movement succeeded.
        """
        existing = db.get_player_by_id(player.playerID)
        if existing is None:
            return False

        return db.db_move_player(
            player.playerID,
            player.batOrder
        )

# =====================================================
# View Layer (Tkinter GUI)
# =====================================================

class StartWindow:
    """
    A modal popup window that captures the game date before the main app starts.

    Attributes:
        root (tk.Tk): The parent window.
        on_success (function): Callback function to execute after a valid date is entered.
    """
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success

        self.popup = tk.Toplevel(root, name="startwindow")
        self.popup.title("Game Date")
        self.popup.geometry("275x115")
        self.popup.grab_set()

        tk.Label(self.popup, text="Enter the game date (YYYY-MM-DD):").pack(pady=10)

        self.date_var = tk.StringVar()
        tk.Entry(self.popup, textvariable=self.date_var).pack()

        tk.Button(self.popup, text="Continue", command=self.validate_date).pack(pady=10)

    def validate_date(self):
        """
        Validate the user-inputted date string format (YYYY-MM-DD).
        
        If valid, triggers the on_success callback. If invalid, shows error message.
        """
        date_str = self.date_var.get().strip()

        if date_str == "":
            self.popup.destroy()
            self.on_success("")  
            return

        try:
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Use YYYY-MM-DD format.")
            return

        self.popup.destroy()
        self.on_success(date_str)

class PlayerApp(ttk.Frame):
    """
    The main application interface for managing baseball player lineups.

    Inherits from ttk.Frame. Provides the Treeview for player display 
    and buttons for triggering management actions.
    """
    def __init__(self, parent, game_date, db_instance):
        super().__init__(parent, padding=10)

        self.parent = parent
        self.db = db_instance
        self.controller = PlayerController()
        self.game_date = game_date
        self.days_until_game = self.calculate_days_until_game(game_date)
        
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def calculate_days_until_game(self, game_date_str):
        """
        Calculate the integer difference between today and the scheduled game.

        Args:
            game_date_str (str): Date in 'YYYY-MM-DD' format.

        Returns:
            int or str: Number of days remaining, or empty string if invalid.
        """
        if not game_date_str:
            return ""

        try:
            game_date = datetime.strptime(game_date_str, "%Y-%m-%d").date()
        except ValueError:
            return ""

        today = date.today()
        date_difference = (game_date - today).days

        return date_difference if date_difference >= 0 else ""
    
    def load_players(self):
        """
        Refresh the Treeview widget with current database data.
        
        Clears existing rows and repopulates them sorted by batting order.
        """
        self.controller.reload_players()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for player in sorted(self.controller.players, key=lambda p: p.batOrder):
            self.tree.insert(
                "",
                "end",
                values=(
                    player.playerID,
                    player.batOrder,
                    player.firstName,
                    player.lastName,
                    player.position,
                    player.atBats,
                    player.hits,
                    player.batting_average
                )
            )
    
    def create_widgets(self):
        """Initialize the layout, headers, treeview, and sidebar buttons."""
        self.grid_columnconfigure(0, weight=1)   
        self.grid_columnconfigure(1, weight=0)   
        
        header = ttk.Frame(self)
        header.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        today_str = date.today().strftime("%Y-%m-%d")
        ttk.Label(header, text=f"Today: {today_str}").grid(row=0, column=0, padx=(0, 20))
        ttk.Label(header, text=f"Game Date: {self.game_date or ''}").grid(row=0, column=1, padx=(0, 20))
        ttk.Label(header, text=f"Days Until Game: {self.days_until_game}").grid(row=0, column=2)         

        left_frame = ttk.Frame(self)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        columns = ("ID", "Bat order","First", "Last" ,"POS", "AB", "Hits", "AVG")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=60 if "ID" not in col else 40, anchor="center")

        self.tree.pack(fill="both", expand=True)

        right_frame = ttk.Frame(self)
        right_frame.grid(row=1, column=1, sticky="ns", padx=10, pady=10)
        button_width = 20

        ttk.Button(right_frame, text="Display Lineup", width=button_width, command=self.load_players).grid(row=0, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Add Player", command=self.open_add_player_window).grid(row=1, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Remove Player", command=self.open_remove_player_window).grid(row=2, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Move Player", command=self.open_move_player_window).grid(row=3, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Edit Stats", command=self.open_edit_stats_window).grid(row=4, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Edit Position", command=self.open_edit_position_window).grid(row=5, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Exit", command=self.parent.destroy).grid(row=6, column=0, pady=5, sticky="ew")

    # -----------------------------
    # PopUp Window Creators
    # -----------------------------

    def open_add_player_window(self):
        """Create and display the 'Add Player' input dialog."""
        popup = tk.Toplevel(self)
        popup.title("Add Player")
        popup.geometry("240x215")


        # Keep popup on top and modal
        popup.transient(self.parent)
        popup.grab_set()
        popup.focus_force()

        ttk.Label(popup, text="First Name").grid(row=0, column=0, padx=10, pady=5)
        first_var = tk.StringVar()
        ttk.Entry(popup, textvariable=first_var).grid(row=0, column=1, padx=10)

        ttk.Label(popup, text="Last Name").grid(row=1, column=0, padx=10, pady=5)
        last_var = tk.StringVar()
        ttk.Entry(popup, textvariable=last_var).grid(row=1, column=1, padx=10)

        ttk.Label(popup, text="Position").grid(row=2, column=0, padx=10, pady=5)
        pos_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pos_var).grid(row=2, column=1, padx=10)

        ttk.Label(popup, text="At bat").grid(row=3, column=0, padx=10, pady=5)
        ab_var = tk.StringVar()
        ttk.Entry(popup, textvariable=ab_var).grid(row=3, column=1, padx=10)

        ttk.Label(popup, text="Hits").grid(row=4, column=0, padx=10, pady=5)
        hits_var = tk.StringVar()
        ttk.Entry(popup, textvariable=hits_var).grid(row=4, column=1, padx=10)

        btn_f = ttk.Frame(popup)
        btn_f.grid(row=5, column=0, columnspan=2, pady=15)
        ttk.Button(btn_f, text="Save", command=lambda: self.save_new_player(popup, first_var.get(), last_var.get(), pos_var.get(), ab_var.get(), hits_var.get())).pack(side="left", padx=10)
        ttk.Button(btn_f, text="Cancel", command=popup.destroy).pack(side="left", padx=10)

    def open_remove_player_window(self):
        """Create and display the 'Remove Player' ID entry dialog."""
        popup = tk.Toplevel(self)
        popup.title("Remove Player")
        popup.geometry("275x85")

        # Keep popup on top and modal
        popup.transient(self.parent)
        popup.grab_set()
        popup.focus_force()

        ttk.Label(popup, text="Player ID").grid(row=0, column=0, padx=10, pady=5)
        pid_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pid_var).grid(row=0, column=1, padx=10)

        btn_f = ttk.Frame(popup)
        btn_f.grid(row=5, column=0, columnspan=2, pady=15)
        ttk.Button(btn_f, text="Delete", command=lambda: self.remove_player_handler(popup, pid_var.get())).pack(side="left", padx=10)
        ttk.Button(btn_f, text="Cancel", command=popup.destroy).pack(side="left", padx=10)

    def open_edit_stats_window(self):
        """Create and display the 'Edit Stats' dialog for AB and Hits."""
        popup = tk.Toplevel(self)
        popup.title("Edit Player Stats")
        popup.geometry("240x180")

        # Keep popup on top and modal
        popup.transient(self.parent)
        popup.grab_set()
        popup.focus_force()

        ttk.Label(popup, text="Player ID").grid(row=0, column=0, padx=10, pady=5)
        pid_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pid_var).grid(row=0, column=1, padx=10)

        ttk.Label(popup, text="At bat").grid(row=1, column=0, padx=10, pady=5)
        ab_var = tk.StringVar()
        ttk.Entry(popup, textvariable=ab_var).grid(row=1, column=1, padx=10)

        ttk.Label(popup, text="Hits").grid(row=2, column=0, padx=10, pady=5)
        hits_var = tk.StringVar()
        ttk.Entry(popup, textvariable=hits_var).grid(row=2, column=1, padx=10)

        btn_f = ttk.Frame(popup)
        btn_f.grid(row=3, column=0, columnspan=2, pady=15)
        ttk.Button(btn_f, text="Save", command=lambda: self.save_player_stats(popup, pid_var.get(), ab_var.get(), hits_var.get())).pack(side="left", padx=10)
        ttk.Button(btn_f, text="Cancel", command=popup.destroy).pack(side="left", padx=10)

    def open_edit_position_window(self):
        """Create and display the 'Edit Position' dialog with valid options shown."""
        positions = db.get_all_positions()
        popup = tk.Toplevel(self)
        popup.title("Edit Player Position")
        popup.geometry("280x140")

        # Keep popup on top and modal
        popup.transient(self.parent)
        popup.grab_set()
        popup.focus_force()

        ttk.Label(popup, text="Valid positions:").grid(row=0, column=0, columnspan=2, padx=10, sticky="w")
        ttk.Label(popup, text=f"{positions}").grid(row=1, column=0, columnspan=2, padx=10)
        ttk.Label(popup, text="Player ID").grid(row=2, column=0, padx=10, pady=5)
        pid_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pid_var).grid(row=2, column=1, padx=10)

        ttk.Label(popup, text="Position").grid(row=3, column=0, padx=10, pady=5)
        pos_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pos_var).grid(row=3, column=1, padx=10)

        btn_f = ttk.Frame(popup)
        btn_f.grid(row=4, column=0, columnspan=2, pady=15)
        ttk.Button(btn_f, text="Save", command=lambda: self.save_player_position(popup, pid_var.get(), pos_var.get())).pack(side="left", padx=10)
        ttk.Button(btn_f, text="Cancel", command=popup.destroy).pack(side="left", padx=10)

    def open_move_player_window(self):
        """Display an error indicating that manual batting order changes are disabled."""
        messagebox.showerror("Not Allowed", "Changing the batting order is not permitted.")

    # -----------------------------
    # Save and remove handlers
    # -----------------------------

    def save_new_player(self, popup, first, last, pos, ab, hits):
        """
        Validate input strings and save a new player object to the database.
        
        Performs logic checks on name characters, stats consistency, and position validity.
        """
        if not ab.strip():
            ab = 0
        if not hits.strip():
            hits = 0
        

        try:
            ab = int(ab)
            hits = int(hits)
        except ValueError:
            messagebox.showerror("Error", "At Bats and Hits must be numbers.")
            return
        
        if ab < 0 or hits < 0:
            messagebox.showerror("Error", "At Bats and Hits cannot be negative.")
            return

        if hits > ab:
            messagebox.showerror("Error", "Hits cannot be greater than At Bats.")
            return

        if not first.strip() or not last.strip() or not pos.strip():
            messagebox.showerror("Error", "First Name, Last Name, and Position cannot be empty.")
            return

        if not first.replace(" ", "").isalpha():
            messagebox.showerror("Error", "First Name cannot contain numbers or symbols.")
            return

        if not last.replace(" ", "").isalpha():
            messagebox.showerror("Error", "Last Name cannot contain numbers or symbols.")
            return


        valid_positions = db.get_all_positions()
        if pos not in valid_positions:
            messagebox.showerror("Error", f"Invalid position. {valid_positions}")
            return

        self.controller.reload_players()

        bat_order = len(self.controller.players) + 1
        player = Player(None, bat_order, first, last, pos, ab, hits)

        success = self.controller.add_player(player)

        if not success:
            messagebox.showerror("Error", "Failed to add player.")
            return

        self.load_players()
        messagebox.showinfo("Success", "Player added.")
        popup.destroy()



    def remove_player_handler(self, popup, pid):
        """
        Validate ID input and coordinate player removal through the controller.

        Args:
            popup (Toplevel): The popup window instance.
            pid (str): The raw player ID string from the entry field.
        """
        if not pid.strip():
            messagebox.showerror("Error", "Player ID cannot be empty.")
            return
        
        try:
            pid = int(pid)
        except ValueError:
            messagebox.showerror("Error", "Player ID must be a number.")
            return

        if self.controller.remove_player(pid):
            self.load_players()
            messagebox.showinfo("Success", "Player removed.")
            popup.destroy()
        else:
            messagebox.showerror("Error", "Failed to remove player.")

    def save_player_stats(self, popup, pid, ab, hits):
        """
        Validate and update stats for a specific player ID.

        Checks for ID existence, non-negative stats, and AB/Hits consistency.
        """
        if not ab.strip():
            ab = 0
        if not hits.strip():
            hits = 0
        
        try:
            pid, ab, hits = int(pid), int(ab), int(hits)
        except ValueError:
            messagebox.showerror("Error", "IPlayer ID, At Bats, and Hits must be numberic.")
            return

        if ab < 0 or hits < 0:
            messagebox.showerror("Error", "At Bats and Hits cannot be negative.")
            return

        if hits > ab:
            messagebox.showerror("Error", "Hits cannot be greater than At Bats.")
            return

        existing = db.get_player_by_id(pid)
        if existing is None:
            messagebox.showerror("Error", f"Player ID {pid} does not exist.")
            return

        player = Player(playerID=pid, atBats=ab, hits=hits)
        
        success = self.controller.edit_player_stats(player)
        if not success:
            messagebox.showerror("Error", "Failed to edit player stats.")
            return

        self.load_players()
        messagebox.showinfo("Success", "Player Stats modified.")
        popup.destroy()


    def save_player_position(self, popup, pid, pos):
        """
        Validate and update the defensive position for a specific player ID.

        Checks for position validity against the allowed list in the database.
        """
        try:
            pid = int(pid)
        except ValueError:
            messagebox.showerror("Error", "Player ID must be numeric.")
            return

        if pos not in db.get_all_positions():
            messagebox.showerror("Error", "Invalid position.")
            return

        player = Player(playerID=pid, position=pos)
        if self.controller.edit_player_position(player):
            self.load_players()
            messagebox.showinfo("Success", "Position updated.")
            popup.destroy()
        else:
            messagebox.showerror("Error", "Player ID not found.")

def main():
    """Application entry point: initializes DB, sets up root window, and starts GUI."""
    db.connect()
    root = tk.Tk()
    root.title('Baseball Team Manager')
    root.geometry("800x500")
    root.withdraw()
    
    def date_app(game_date):
        root.deiconify()
        PlayerApp(root, game_date, db_instance=db)

    StartWindow(root, date_app)
    root.mainloop()
    db.close()

if __name__ == "__main__":
    main()