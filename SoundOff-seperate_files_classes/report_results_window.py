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

        Will provide user with the LUFS and true peak value of the audio file passed. Will also prompt the user to
        select the platform and standard type to test the audio file against.

        Args:
          self: The instance of the report result window
          parent: App object, window it came from
          file_path: The path of the file selected

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("Select Report")
        self.geometry("490x200")

        # get LUFS and peak from audio file
        wav_info = parent.open_wav_file()
        lufs = parent.get_luf(wav_info)
        peak = parent.get_peak(wav_info)

        # get platform names to be used in drop-down widget
        platform_names = parent.get_platform_names()
        platform_names.insert(0, "All Available Platforms")
        selected_name = StringVar()
        # preselect first option so if a user does not click drop down list, it is assumed they wanted the first option
        selected_name.set(platform_names[0])
        selected_lufs_peak = StringVar()
        selected_lufs_peak.set("LUFS and Peak")

        # only print first 50 characters of the file path
        if len(file_path) > 50:
            new_file_path = file_path[:50] + "..."
        else:
            new_file_path = file_path

        # define labels and widgets to be placed on the screen
        selected_file_label = Label(
            self,
            text="Selected file path: " + new_file_path,
            font=("Helvetica", 10, "bold")
        )
        directions_label = Label(
            self,
            text="Please select the type of report you wish you view",
            font=("Helvetica", 10, "bold")
        )
        drop_platforms = OptionMenu(
            self,
            selected_name,
            *platform_names,
        )
        drop_lufs_peak = OptionMenu(
            self,
            selected_lufs_peak,
            "LUFS and Peak",
            "LUFS Value",
            "Peak Value",
        )
        lufs_value_label = Label(
            self,
            text="Your Integrated Loudness (LUFS) = " + "{:.2f}".format(lufs)
        )
        peak_value_label = Label(
            self,
            text="Your True Peak (dB) =" + "{:.2f}".format(peak)
        )
        blank_label = Label(
            self,
            text=""
        )
        enter_button = ttk.Button(
            self,
            text="Enter",
            style="Enter.TButton",
            command=lambda: view_results_window.View(
                parent,
                selected_name.get(),
                selected_lufs_peak.get(),
                peak,
                lufs,
                self
            )
        )

        # change look of labels and widgets
        drop_platforms.config(
            width=25,
            bg="#6f67c2",
            fg="white",
            font=("Helvetica", 11)
        )
        drop_lufs_peak.config(
            width=20,
            bg="#6f67c2",
            fg="white",
            font=("Helvetica", 11)
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
        directions_label.grid(column=0, row=4, columnspan=4, sticky="w")
        drop_platforms.grid(column=0, row=5)
        drop_lufs_peak.grid(column=1, row=5)
        lufs_value_label.grid(column=0, row=1, sticky="w")
        peak_value_label.grid(column=0, row=2, sticky="w")
        blank_label.grid(column=0, row=3, pady=10)
        enter_button.grid(column=0, row=6, sticky="w")

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)
