import tkinter as tk
from tkinter import ttk
from tkinter import *


class ViewStandards(tk.Toplevel):
    """View all available platforms and standards.

    Will allow users to view every platorm with max integrated loudness (LUFS) and max peak (dB)

    """
    def __init__(self, parent):
        """Initializes the ViewStandards window

        More info if needed

        Args:
          self: An add new variable object
          parent: App object, window it came from

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("View Standards")
        self.geometry("400x400")

        container = ttk.Frame(self)
        container.pack(fill=BOTH, expand=1)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar.set)

        style = ttk.Style()
        style.configure(
            "Heading.TLabel",
            font=("Helvetica", 9, "bold")
        )
        style.configure(
            "Data.TLabel",
            font="Helvetica, 8"
        )

        standard_label = ttk.Label(
            scrollable_frame,
            text="Standard Name",
            style="Heading.TLabel")

        standard_label.grid(column=0, row=0, padx=5)

        lufs_level_label = ttk.Label(
            scrollable_frame,
            text="Max Integrated (LUFS)",
            style="Heading.TLabel")

        lufs_level_label.grid(column=1, row=0, padx=5)
        peak_level_label = ttk.Label(
            scrollable_frame,
            text="Max True Peak (dB)",
            style="Heading.TLabel")

        peak_level_label.grid(column=2, row=0, padx=5)

        standard_names = parent.get_standard_names_dict()
        # row variable
        i = 1
        for name in standard_names:
            name_label = ttk.Label(
                scrollable_frame,
                text=name,
                style="Data.TLabel"
            )
            values = parent.get_standard_value(name)

            lufs_label = ttk.Label(
                scrollable_frame,
                text=values[0],
                style="Data.TLabel"
            )
            peak_label = ttk.Label(
                scrollable_frame,
                text=values[1],
                style="Data.TLabel"
            )

            name_label.grid(column=0, row=i, padx=5)
            lufs_label.grid(column=1, row=i, padx=5)
            peak_label.grid(column=2, row=i, padx=5)
            i += 1

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
