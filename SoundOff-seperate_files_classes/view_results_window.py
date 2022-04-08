import tkinter as tk
from tkinter import ttk
from tkinter import *


class ViewPlatforms(tk.Toplevel):
    """View all available platforms and standards.

    Will allow users to view every platform with max integrated loudness (LUFS) and max peak (dB)

    """
    def __init__(self, parent):
        """Initializes the View Platforms window

        Will display current directory of platforms by using the get_platform_names method and the
        standards of these platforms by using the get_platform_standard method.

        Args:
          self: The instance of the view platforms window
          parent: App object, window it came from

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("View Platforms")
        # change size according to the longest platform name
        max_name_length = parent.get_max_platform_name_length()
        size = str(max_name_length*6+480) + "x400"
        self.geometry(size)

        # define a scrollable frame
        container = ttk.Frame(self)
        container.pack(fill="both", expand=1)
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

        # define our headers
        platform_label = ttk.Label(
            scrollable_frame,
            text="Platform Name",
            style="Heading.TLabel"
        )
        lufs_level_label = ttk.Label(
            scrollable_frame,
            text="Max Integrated Loudness (LUFS)",
            style="Heading.TLabel"
        )
        peak_level_label = ttk.Label(
            scrollable_frame,
            text="Max True Peak (dBFS)",
            style="Heading.TLabel"
        )

        # define the look of our headers and platform data
        style = ttk.Style()
        style.configure(
            "Heading.TLabel",
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "Data.TLabel",
            font=("Helvetica", 9)
        )

        # place our headers on the screen
        platform_label.grid(column=0, row=0, padx=5)
        lufs_level_label.grid(column=1, row=0, padx=5)
        peak_level_label.grid(column=2, row=0, padx=5)

        platform_names = parent.get_platform_names()
        # row variable
        i = 1
        for name in platform_names:
            name_label = ttk.Label(
                scrollable_frame,
                text=name,
                style="Data.TLabel"
            )
            values = parent.get_platform_standard(name)
            # make sure the value is not null before trying to format it
            if values[0] != "":
                lufs = "{:.1f}".format(values[0])
            else:
                lufs = ""
            if values[1] != "":
                peak = "{:.1f}".format(values[1])
            else:
                peak = ""

            # define our lufs and peak max values as labels to be placed on the screen
            lufs_label = ttk.Label(
                scrollable_frame,
                text=lufs,
                style="Data.TLabel"
            )
            peak_label = ttk.Label(
                scrollable_frame,
                text=peak,
                style="Data.TLabel"
            )

            # place the platform, lufs, and peak labels on the screen
            name_label.grid(column=0, row=i, padx=5)
            lufs_label.grid(column=1, row=i, padx=5)
            peak_label.grid(column=2, row=i, padx=5)
            # iterate the row for next platform
            i += 1

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)
