import tkinter as tk
from tkinter import ttk
from tkinter import *
import view_results_window


class Report(tk.Toplevel):
    """A window to report the LUFS and peak value of the file selected.

        Will prompt the user to select the type of report (which standards to test against) to view.

    """
    def __init__(self, parent, file_path):
        """Initializes the view report window

        more info

        Args:
          self: An add new variable object
          parent: App object, window it came from
          file_path: The path of the file selected

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("Select Report")
        self.geometry("490x200")

        peak = parent.get_peak(file_path)
        lufs = parent.get_luf(file_path)

        if len(file_path) > 50:
            new_file_path = file_path[:50] + "..."
        else:
            new_file_path = file_path

        selected_file_label = Label(
            self,
            text="Selected file path: " + new_file_path,
            font=("Helvetica", 10, "bold")
        )
        selected_file_label.grid(column=0, row=0, columnspan=4)

        directions_label = Label(
            self,
            text="Please select the type of report you wish you view",
            font=("Helvetica", 10, "bold")
        )
        directions_label.grid(column=0, row=4, columnspan=4, sticky="w")

        standard_names = parent.get_standard_names_dict()
        standard_names.append("All Available Standards")
        selected_name = StringVar()
        selected_name.set(standard_names[0])
        selected_lufs_peak = StringVar()
        selected_lufs_peak.set("LUFS Value")

        drop_standards = OptionMenu(
            self,
            selected_name,
            *standard_names,
        )

        drop_lufs_peak = OptionMenu(
            self,
            selected_lufs_peak,
            "LUFS Value",
            "Peak Value",
            "LUFS and Peak"
        )
        drop_standards.config(width=25)
        drop_standards.config(bg="#333147")
        drop_standards.config(fg="white")
        drop_lufs_peak.config(width=20)
        drop_lufs_peak.config(bg="#333147")
        drop_lufs_peak.config(fg="white")
        drop_standards.grid(column=0, row=5)
        drop_lufs_peak.grid(column=1, row=5)
        lufs_value_label = Label(
            self,
            text="Your LUFS = " + str(lufs)
        )
        peak_value_label = Label(
            self,
            text="Your Peak =" + str(peak)
        )
        lufs_value_label.grid(column=0, row=1, sticky="w")
        peak_value_label.grid(column=0, row=2, sticky="w")

        blank_label = Label(
            self,
            text=""
        )
        blank_label.grid(column=0, row=3, pady=10)

        enter_button = ttk.Button(
            self,
            text="Enter",
            command=lambda: view_results_window.View(
                parent,
                selected_name.get(),
                selected_lufs_peak.get(),
                peak,
                lufs,
                self
            )
        )
        enter_button.grid(column=0, row=6, sticky="w")
