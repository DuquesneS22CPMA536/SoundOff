"""
This module will display the lufs value, true peak value, sample rate, and
number of channels of a file passed. It will also prompt the user to pick
a certain report of these values against available platforms.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import Listbox
from tkinter import OptionMenu
import view_results_window


class Report(tk.Toplevel):
    """A window to report the LUFS and peak value of the file selected.

        Will prompt the user to select the type of report (which standards to test against) to view.

    """
    def __init__(self, parent, file_path, rate, num_channels, lufs, peak):
        """Initializes the view report window

        Will provide user with the LUFS and true peak value of the audio file passed. Will also
        prompt the user to select the platform and standard type to test the audio file against.

        Args:
          self: The instance of the report result window
          parent: App object, window it came from
          file_path: The path of the file selected
          rate: The rate of the file path
          num_channels: The number of channels of the file path
          lufs: the lufs value
          peak: the peak value

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("Select Report")
        max_name_length = parent.get_max_platform_name_length()
        size = str(max_name_length * 6 + 450) + "x500"
        self.geometry(size)

        # get platform names to be used in drop-down widget
        platform_names = parent.get_platform_names()
        # preselect first option so if a user does not click drop down list, it is assumed
        # they wanted the first option
        selected_lufs_peak = StringVar()
        selected_lufs_peak.set("LUFS and Peak")

        # only print first 50 characters of the file path
        if len(file_path) > 50:
            new_file_path = file_path[:50] + "..."
        else:
            new_file_path = file_path

        # define labels and widgets to be placed on the screen
        selected_file_label = ttk.Label(
            self,
            text="Selected file path: " + new_file_path,
            font=("Helvetica", 11, "bold")
        )
        directions_label = ttk.Label(
            self,
            text="Please select the type of report you wish you view",
            font=("Helvetica", 11, "bold")
        )
        scrollbar = ttk.Scrollbar(self)
        scrollbar.grid(column=0, row=7, sticky="ns")
        listbox_of_platforms = Listbox(
            self,
            bg="#6f67c2",
            fg="white",
            font="Helvetica",
            selectbackground="#2d2933",
            selectmode="multiple",
            yscrollcommand=scrollbar.set,
            width=10 + parent.get_max_platform_name_length()
        )
        for name in platform_names:
            listbox_of_platforms.insert("end", name)

        drop_lufs_peak = OptionMenu(
            self,
            selected_lufs_peak,
            "LUFS and Peak",
            "LUFS Value",
            "Peak Value",
        )
        lufs_value_label = ttk.Label(
            self,
            text=f'Your Integrated Loudness (LUFS) = {lufs:.1f}',
            font=("Helvetica", 10)
        )
        peak_value_label = ttk.Label(
            self,
            text=f'Your True Peak (dBFS) = {peak:.1f}',
            font=("Helvetica", 10)
        )
        sample_rate_label = ttk.Label(
            self,
            text="Your Sample Rate (Hz) = " + str(rate),
            font=("Helvetica", 10)
        )
        num_channels_label = ttk.Label(
            self,
            text="Your number of channels = " + str(num_channels),
            font=("Helvetica", 10)
        )
        blank_label = ttk.Label(
            self,
            text=""
        )
        enter_button = ttk.Button(
            self,
            text="Select",
            style="Enter.TButton",
            command=lambda: make_selection()

        )
        select_all_button = ttk.Button(
            self,
            text="Select All Platforms",
            style="Enter.TButton",
            command=lambda: view_results_window.View(
                parent,
                platform_names,
                selected_lufs_peak.get(),
                peak,
                lufs,
                self
            )
        )

        def enter_key_clicked(event):
            make_selection()

        self.bind("<Return>", enter_key_clicked)

        def make_selection():
            selected_names = []
            for curr_name in listbox_of_platforms.curselection():
                selected_names.append(listbox_of_platforms.get(curr_name))

            view_results_window.View(
                parent,
                selected_names,
                selected_lufs_peak.get(),
                peak,
                lufs,
                self
            )

        # change look of labels and widgets
        drop_lufs_peak.config(
            width=20,
            bg="#6f67c2",
            fg="white",
            font=("Helvetica", 12)
        )
        style = ttk.Style()
        style.configure(
            "Enter.TButton",
            foreground="#1e1529",
            background="white",
            border=0,
            font=('Helvetica', 11)
        )
        selected_file_label.grid(column=0, row=0, columnspan=4, sticky="w")
        directions_label.grid(column=0, row=6, columnspan=4, sticky="w")
        listbox_of_platforms.grid(column=0, row=7, sticky="w", padx=5)
        drop_lufs_peak.grid(column=1, row=7, sticky="n")
        lufs_value_label.grid(column=0, row=1, sticky="w")
        peak_value_label.grid(column=0, row=2, sticky="w")
        sample_rate_label.grid(column=0, row=3, sticky="w")
        num_channels_label.grid(column=0, row=4, sticky="w")
        blank_label.grid(column=0, row=5, pady=10)
        enter_button.grid(column=0, row=8, sticky="w", padx=5)
        select_all_button.grid(column=0, row=9, sticky="w", padx=5)

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)
