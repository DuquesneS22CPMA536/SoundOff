"""
This module will add a new platform to both the standards.db file and the standards
stored within the main window.
"""
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
import error_window


class AddNew(tk.Toplevel):
    """A window to prompt the user for a new platform name, max lufs value, and max peak value

    Will make changes to the main window and standards.db file

    """
    def __init__(self, parent):
        """Initializes the add new platform window

        Will prompt the user for a platform name, a max integrated (LUFS) value and true peak (dB)
        value. Will call the add_new_standard method to make changes.

        Args:
          self: The instance of the add new standard window
          parent: App object, window it came from

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("Add a New Platform Standard")
        self.geometry("835x95")
        self.configure(bg="#2d2933")

        # define our labels and widgets to be placed on the screen
        platform_label = ttk.Label(
            self,
            text="Platform Name",
            style="Header.TLabel"
        )
        lufs_label = ttk.Label(
            self,
            text="Max Integrated Loudness (LUFS)",
            style="Header.TLabel"
        )
        peak_label = ttk.Label(
            self,
            text="Max True Peak (dBFS)",
            style="Header.TLabel"
        )
        blank_label = ttk.Label(
            self,
            text="",
            width=16,
            style="Blank.TLabel"
        )
        enter_button = ttk.Button(
            self,
            text="Enter",
            style="Enter.TButton",
            command=lambda: self.add_new_standard(
                platform_value_entry_tf.get(),
                lufs_value_entry_tf.get(),
                peak_value_entry_tf.get(),
                parent
            )
        )

        def enter_key_clicked(event):
            self.add_new_standard(
                platform_value_entry_tf.get(),
                lufs_value_entry_tf.get(),
                peak_value_entry_tf.get(),
                parent
            )

        self.bind("<Return>", enter_key_clicked)

        # set entry values to blank string variables
        platform_name_entry = StringVar(self)
        lufs_entry = StringVar(self)
        peak_entry = StringVar(self)

        # define entry boxes
        platform_value_entry_tf = ttk.Entry(
            self,
            textvariable=platform_name_entry,
            width=52
        )
        lufs_value_entry_tf = ttk.Entry(
            self,
            textvariable=lufs_entry
        )
        peak_value_entry_tf = ttk.Entry(
            self,
            textvariable=peak_entry
        )

        # define the look of our labels and widgets
        style = ttk.Style()
        style.configure(
            "Header.TLabel",
            font=("Helvetica", 11, "bold"),
            background="#2d2933",
            foreground="white"
        )
        style.configure(
            "Blank.TLabel",
            foreground="#2d2933",
            background="#2d2933",
            font=('Helvetica', 8)
        )
        style.configure(
            "Enter.TButton",
            foreground="#1e1529",
            background="white",
            border=0,
            font=('Helvetica', 11)
        )

        # place all of our labels and widgets on the screen
        platform_label.grid(column=0, row=0)
        lufs_label.grid(column=1, row=0, padx=50)
        peak_label.grid(column=2, row=0)
        platform_value_entry_tf.grid(column=0, row=1, padx=5)
        lufs_value_entry_tf.grid(column=1, row=1, padx=5)
        peak_value_entry_tf.grid(column=2, row=1, padx=5)
        blank_label.grid(column=0, row=2, padx=10)
        enter_button.grid(column=0, row=3)

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)

    def add_new_standard(self, platform_name, lufs_value, peak_value, parent):
        """Uses input from add new window to make changes to original window.

        Will add a new platform with corresponding max integrated (LUFS) and max true peak (dB) by
        calling the add_to_standard_dict method within the main window class. Calls the error window
        method when an error in user input was made.

        Args:
            self: The instance of the add new standard window
            platform_name: The name of the platform
            lufs_value: The max integrated (LUFS) value
            peak_value: The max true peak (dB)
            parent: App object, window it came from

        Raises:
        Any errors raised should be put here

        """
        # some errors may be found with user input, destroy is a boolean variable that marks whether
        # an error was raised, if so the window may be destroyed
        destroy = True
        if platform_name.lower().split() in parent.get_platform_names_lower():
            error_window.AddError(self, "Platform name already exists")
            destroy = False
        elif platform_name == "":
            error_window.AddError(self, "Please enter a platform name")
            destroy = False

        if lufs_value != "":
            # make sure we have negative numbers
            is_valid, error_msg = is_valid_input(lufs_value)
            if not is_valid:
                error_window.AddError(self, error_msg)
                destroy = False

        if peak_value != "":
            is_valid, error_msg = is_valid_input(peak_value)
            if not is_valid:
                error_window.AddError(self, error_msg)
                destroy = False

        if lufs_value == "" and peak_value == "":
            error_window.AddError(
                self,
                "Please enter either a max integrated loudness or max true peak value."
            )
            destroy = False

        # an error was not found with the latest input, changes can be made and the window can be
        # destroyed
        if destroy:
            parent.add_to_platforms(
                platform_name,
                (lufs_value, peak_value)
            )
            self.destroy()


def is_valid_input(curr_input):
    """ Gives the standard names stored within the standard dictionary.

    Returns the standard names currently being stored as list.

    Args:
        curr_input: the LUFS or peak input a user is trying to include as a platform standard

    Returns:
        is_valid: a boolean value for whether the input is valid or not
        error_msg: the error message to report if the input is not valid

    Raises:
        Any errors raised should be put here
    """
    error_msg = ""
    is_valid = True
    if curr_input[0] == '-':
        if not curr_input[1:].isnumeric():
            split_value = curr_input[1:].split(".")
            if len(split_value) != 2:
                error_msg = "Enter a numeric value"
                is_valid = False
            elif not split_value[0].isnumeric() or not split_value[0].isnumeric():
                if split_value[0] != "":
                    error_msg = "Enter a numeric value"
                    is_valid = False
    else:
        error_msg = "Must enter a negative value"
        is_valid = False
    return is_valid, error_msg
