import tkinter as tk
from tkinter import ttk, messagebox
import db


from objects import Player



# =====================================================
# Controller Layer
# =====================================================

class PlayerController:
    pass


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

    def create_widgets(self):
    # Main layout: 2 columns (left list, right buttons)
        self.grid_columnconfigure(0, weight=1)   # left side expands
        self.grid_columnconfigure(1, weight=0)   # right side fixed

    # -------------------------
    # LEFT SIDE: Player List
    # -------------------------
        left_frame = ttk.Frame(self)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Example list (Treeview)
        columns = ("ID", "Name", "POS", "AB", "H", "AVG")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")

        self.tree.pack(fill="both", expand=True)

    # -------------------------
    # RIGHT SIDE: Buttons
    # -------------------------
        right_frame = ttk.Frame(self)
        right_frame.grid(row=0, column=1, sticky="ns", padx=10, pady=10)

    # Make buttons full width inside right frame
        right_frame.grid_columnconfigure(0, weight=1)

        button_width = 20

        ttk.Button(right_frame, text="Display Lineup", width=button_width).grid(row=0, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Add Player", width=button_width).grid(row=1, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Remove Player", width=button_width).grid(row=2, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Move Player", width=button_width).grid(row=3, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Edit Position", width=button_width).grid(row=4, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Edit Stats", width=button_width).grid(row=5, column=0, pady=5, sticky="ew")
        ttk.Button(right_frame, text="Exit", width=button_width).grid(row=6, column=0, pady=5, sticky="ew")




def main():

    db.connect()

    root = tk.Tk()
    root.title('Baseball Team Manager')
    root.geometry("800x475")
    #root.eval('tk::PlaceWindow . center')


    PlayerApp(root)

    root.mainloop()

    db.close()


if __name__ == "__main__":
    main()