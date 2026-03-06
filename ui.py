import tkinter as tk
from tkinter import ttk, messagebox
import db


from objects import Player



# =====================================================
# Controller Layer
# =====================================================

class PlayerController:
    def __init__(self):

        self.players = db.get_players()

    def add_player(self, player):

        success = db.db_add_player(player)

        if success:
            self.players.append(player)
        return success

    def reload_players(self):
        self.players = db.get_players()

    def remove_player(self, playerID):
        success = db.db_remove_player(playerID)

        if success:
            self.players = [p for p in self.players if p.playerID == playerID]
        return success
    
    def edit_player_stats(self, player: Player):
        existing = db.get_player_by_id(player.playerID)
        if existing is None:
            return False

        return db.db_edit_player_stats(
            player.playerID,
            player.atBats,
            player.hits
        )

    def edit_player_position(self, player: Player):
        existing = db.get_player_by_id(player.playerID)
        if existing is None:
            return False

        return db.db_edit_player_position(
            player.playerID,
            player.position
        )


# =====================================================
# View Layer (Tkinter GUI)
# =====================================================

class PlayerApp(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)

        self.parent = parent
        self.controller = PlayerController()

        self.pack(fill="both", expand=True)

        self.create_widgets()

    def load_players(self):

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

        self.grid_columnconfigure(0, weight=1)   
        self.grid_columnconfigure(1, weight=0)   

    # -------------------------
    # LEFT SIDE: Player List
    # -------------------------
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


        columns = ("ID", "Bat order","First", "Last" ,"POS", "AB", "Hits", "AVG")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.column("ID",        width=40,  anchor="center")
        self.tree.column("Bat order", width=60,  anchor="center")
        self.tree.column("First",     width=120, anchor="w")
        self.tree.column("Last",      width=120, anchor="w")
        self.tree.column("POS",       width=40,  anchor="center")
        self.tree.column("AB",        width=40,  anchor="center")
        self.tree.column("Hits",      width=40,  anchor="center")
        self.tree.column("AVG",       width=40,  anchor="center")

        self.tree.pack(fill="both", expand=True)

    # -------------------------
    # RIGHT SIDE: Buttons
    # -------------------------
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)


        right_frame.grid_columnconfigure(0, weight=1)

        button_width = 20

        ttk.Button(right_frame, text="Display Lineup", width=button_width, command=self.load_players).grid(row=0, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Add Player", command=self.open_add_player_window, width=button_width).grid(row=1, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Remove Player", command=self.open_remove_player_window, width=button_width).grid(row=2, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Move Player", width=button_width).grid(row=3, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Edit Stats", command=self.open_edit_stats_window, width=button_width).grid(row=4, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Edit Position", command=self.open_edit_position_window, width=button_width).grid(row=5, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Exit", command=self.parent.destroy,width=button_width).grid(row=6, column=0, pady=5, sticky="ew")

    # -----------------------------
    # PopUp windows
    # -----------------------------
    def open_add_player_window(self):
        popup = tk.Toplevel(self)
        popup.title("Add Player")
        popup.geometry("240x215")
        popup.grid_columnconfigure(0, weight=0)
        popup.grid_columnconfigure(1, weight=1)


        ttk.Label(popup, text="First Name").grid(row=0, column=0, padx=10, pady=(5, 5), sticky="w")
        first_var = tk.StringVar()
        ttk.Entry(popup, textvariable=first_var).grid(row=0, column=1, padx=10, pady=(5,5), sticky="ew")

        ttk.Label(popup, text="Last Name").grid(row=1, column=0, padx=10, pady=(5, 5), sticky="w")
        last_var = tk.StringVar()
        ttk.Entry(popup, textvariable=last_var).grid(row=1, column=1, padx=10, pady=(5,5), sticky="ew")

        ttk.Label(popup, text="Position").grid(row=2, column=0, padx=10, pady=(5, 5), sticky="w")
        pos_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pos_var).grid(row=2, column=1, padx=10, pady=(5,5), sticky="ew")

        ttk.Label(popup, text="At bat").grid(row=3, column=0, padx=10, pady=(5, 5), sticky="w")
        ab_var = tk.StringVar()
        ttk.Entry(popup, textvariable=ab_var).grid(row=3, column=1, padx=10, pady=(5,5), sticky="ew")

        ttk.Label(popup, text="Hits").grid(row=4, column=0, padx=10, pady=(5, 5), sticky="w")
        hits_var = tk.StringVar()
        ttk.Entry(popup, textvariable=hits_var).grid(row=4, column=1, padx=10, pady=(5,5), sticky="ew")

        button_frame = ttk.Frame(popup)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        ttk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_new_player(
                popup, first_var.get(), last_var.get(), pos_var.get(), ab_var.get(), hits_var.get()
            )
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy   
        ).pack(side="left", padx=10)


    def open_remove_player_window(self):
        popup = tk.Toplevel(self)
        popup.title("Remove Player")
        popup.geometry("275x85")
        popup.grid_columnconfigure(0, weight=0)
        popup.grid_columnconfigure(1, weight=1)

        ttk.Label(popup, text="Player ID").grid(row=0, column=0, padx=10, pady=(5, 5), sticky="w")
        pid_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pid_var).grid(row=0, column=1, padx=10, pady=(5,5), sticky="ew")

        button_frame = ttk.Frame(popup)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        ttk.Button(
            button_frame,
            text="Delete",
            command=lambda: self.remove_player(
                popup, pid_var.get()
            )
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy   
        ).pack(side="left", padx=10)

    def open_edit_stats_window(self):
        popup = tk.Toplevel(self)
        popup.title("Edit Player Stats")
        popup.geometry("240x150")
        popup.grid_columnconfigure(0, weight=0)
        popup.grid_columnconfigure(1, weight=1)


        ttk.Label(popup, text="Player ID").grid(row=0, column=0, padx=10, pady=(5, 5), sticky="w")
        pid_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pid_var).grid(row=0, column=1, padx=10, pady=(5,5), sticky="ew")

        ttk.Label(popup, text="At bat").grid(row=1, column=0, padx=10, pady=(5, 5), sticky="w")
        ab_var = tk.StringVar()
        ttk.Entry(popup, textvariable=ab_var).grid(row=1, column=1, padx=10, pady=(5,5), sticky="ew")

        ttk.Label(popup, text="Hits").grid(row=2, column=0, padx=10, pady=(5, 5), sticky="w")
        hits_var = tk.StringVar()
        ttk.Entry(popup, textvariable=hits_var).grid(row=2, column=1, padx=10, pady=(5,5), sticky="ew")

        button_frame = ttk.Frame(popup)
        button_frame.grid(row=3, column=0, columnspan=2, pady=15)

        ttk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_player_stats(
                popup, pid_var.get(), ab_var.get(), hits_var.get()
            )
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy   
        ).pack(side="left", padx=10)

    def open_edit_position_window(self):
        popup = tk.Toplevel(self)
        popup.title("Edit Player Position")
        popup.geometry("240x125")
        popup.grid_columnconfigure(0, weight=0)
        popup.grid_columnconfigure(1, weight=1)


        ttk.Label(popup, text="Player ID").grid(row=0, column=0, padx=10, pady=(5, 5), sticky="w")
        pid_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pid_var).grid(row=0, column=1, padx=10, pady=(5,5), sticky="ew")

        ttk.Label(popup, text="Position").grid(row=1, column=0, padx=10, pady=(5, 5), sticky="w")
        pos_var = tk.StringVar()
        ttk.Entry(popup, textvariable=pos_var).grid(row=1, column=1, padx=10, pady=(5,5), sticky="ew")

        button_frame = ttk.Frame(popup)
        button_frame.grid(row=2, column=0, columnspan=2, pady=15)

        ttk.Button(
            button_frame,
            text="Save",
            command=lambda: self.save_player_position(
                popup, pid_var.get(), pos_var.get()
            )
        ).pack(side="left", padx=10)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=popup.destroy   
        ).pack(side="left", padx=10)    

    # -----------------------------
    # Save and remove handlers
    # -----------------------------
    def save_new_player(self, popup, first, last, pos, ab, hits):
        try:
            ab = int(ab)
            hits = int(hits)
        except ValueError:
            messagebox.showerror("Error", "At Bats, and Hits must be numbers.")
            return
        

        if not first.strip() or not last.strip() or not pos.strip():
            messagebox.showerror("Error", "First Name, Last Name, and Position cannot be empty.")
            return

        self.controller.reload_players()

        bat_order = len(self.controller.players) + 1

        player = Player(
            playerID=None,
            batOrder=bat_order,
            firstName=first,
            lastName=last,
            position=pos,
            atBats=ab,
            hits=hits
        )

        success = self.controller.add_player(player)

        if not success:
            messagebox.showerror("Error", "Failed to add player.")
            return

        self.load_players()
        messagebox.showinfo("Success", "Player added.")
        popup.destroy()

    def remove_player(self, popup, pid):

        success = self.controller.remove_player(pid)

        if not success:
            messagebox.showerror("Error", "Failed to remove player.")
            return

        self.load_players()

        messagebox.showinfo("Success", "Player removed.")
        popup.destroy()


    def save_player_stats(self, popup, pid, ab, hits):
        try:
            pid = int(pid)
            ab = int(ab)
            hits = int(hits)
        except ValueError:
            messagebox.showerror("Error", "Player ID, At Bats, and Hits must be numbers.")
            return

        if ab < 0 or hits < 0:
            messagebox.showerror("Error", "Stats cannot be negative.")
            return

        if hits > ab:
            messagebox.showerror("Error", "Hits cannot be greater than At Bats.")
            return

        player = Player(
            playerID=pid,
            atBats=ab,
            hits=hits
        )

        success = self.controller.edit_player_stats(player)
        if not success:
            messagebox.showerror("Error", "Failed to edit player stats.")
            return

        self.load_players()
        messagebox.showinfo("Success", "Player Stats modified.")
        popup.destroy()


    def save_player_position(self, popup, pid, pos):

        try:
            pid = int(pid)
        except ValueError:
            messagebox.showerror("Error", "Player ID, At Bats, and Hits must be numbers.")
            return

        if not pos.strip():
            messagebox.showerror("Error", "Position cannot be empty.")
            return
        
        else:
            if pos not in db.VALID_POSITIONS:
                messagebox.showerror("Error", f"Not a valid position. {db.VALID_POSITIONS}")
                return
            
        player = Player(
            playerID=pid,
            position=pos
        )

        success = self.controller.edit_player_position(player)
        if not success:
            messagebox.showerror("Error", "Failed to edit player position.")
            return
        
        self.load_players()
        messagebox.showinfo("Success", "Player Position modified.")
        popup.destroy()
    
    def save_moved_player(self, popup, pid, first, last, pos):
        # call your controller/db logic here
        # db.db_add_player(...)

        self.load_players()
        messagebox.showinfo("Success", "Player moved.")
        popup.destroy()

def main():

    db.connect()
    #b.debug_print_schema()  # Delete after testing

    root = tk.Tk()
    root.title('Baseball Team Manager')
    root.geometry("800x475")
    #root.eval('tk::PlaceWindow . center')


    PlayerApp(root)

    root.mainloop()

    db.close()


if __name__ == "__main__":
    main()