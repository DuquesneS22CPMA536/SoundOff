from tkinter import *
import error_window
import warning_window
from warning_window import *


class Modify(tk.Toplevel):
    """A window to modify or delete existing changes

        Will take input from user to ask what changes should be made and then use the parent
        SoundOff window to make changes

    """
    def __init__(self, parent):
        """Initializes the modify/delete platform standards window

        Will get user input for the standard to change/delete, the type of change to make (LUFS,
        Peak, Delete), and the value to change LUFS or peak to.

        Args:
          self: The instance of the modify/delete platform standards window
          parent: App object, window it came from

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("Modify Platform Standards")
        self.geometry("600x100")
        self.configure(bg="#2d2933")

        # preselect first option from drop-down menu to be picked
        platform_names = parent.get_platform_names()
        selected_name = StringVar()
        selected_name.set(platform_names[0])
        selected_lufs_peak = StringVar()
        selected_lufs_peak.set("LUFS Value")

        # define our entry box input from user to be blank
        blank_value = StringVar(self)
        blank_value.set("")

        # define all of our labels and widgets
        drop_platforms = OptionMenu(
            self,
            selected_name,
            *platform_names)

        drop_lufs_peak = OptionMenu(
            self,
            selected_lufs_peak,
            "LUFS Value",
            "Peak Value",
            "Delete Platform"
        )
        new_value_tf = Entry(
            self,
            textvariable=blank_value,
            width=13
        )
        enter_button = ttk.Button(
            self,
            text="Enter",
            style="Enter.TButton",
            command=lambda: self.modify_existing_platforms(
                selected_name.get(),
                selected_lufs_peak.get(),
                new_value_tf.get(),
                parent
            )
        )

        def enter_key_clicked(event):
            self.modify_existing_platforms(
                selected_name.get(),
                selected_lufs_peak.get(),
                new_value_tf.get(),
                parent
            )

        self.bind("<Return>", enter_key_clicked)

        blank_label = ttk.Label(
            self,
            text="",
            width=16,
            style="Blank.TLabel"
        )

        # define the look of our labels and widgets
        drop_platforms.config(
            width=38,
            height=1,
            bg="#6f67c2",
            fg="white",
            font=("Helvetica", 11),
        )
        drop_lufs_peak.config(
            width=15,
            height=1,
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
        style.configure(
            "Blank.TLabel",
            foreground="#2d2933",
            background="#2d2933",
            font=('Helvetica', 8)
        )

        # place all of our labels and widgets on the screen
        drop_platforms.grid(column=0, row=0)
        drop_lufs_peak.grid(column=1, row=0)
        new_value_tf.grid(column=2, row=0)
        enter_button.grid(column=0, row=2)
        blank_label.grid(column=0, row=1)

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)

    def modify_existing_platforms(
            self,
            name,
            change_type,
            value,
            parent
    ):
        """Uses input from add new window to make changes to original window.

        Will add a new platform with corresponding max integrated (LUFS) and max true peak (dB) by
        calling the add_to_standard method within the main window class. Calls the error window
        method when an error in user input was made.

        Args:
            self: The instance of the modify/delete platform standards window
            name: The name of the platform being changed
            change_type: The type of change (LUFS, Peak, Delete) to make
            value: The new LUFS or Peak value to change to
            parent: App object, window it came from

        Raises:
            Any errors raised should be put here

        """
        # some errors may be found with user input, destroy is a boolean variable that marks whether
        # an error was raised, if so the window may be destroyed
        destroy = True

        # if a user decides to delete a standard, create a warning message by using the warning
        # window to make sure the user wishes to make this change
        if change_type == "Delete Platform":
            destroy = False
            warning_msg = "Do you want to delete "+name+"?"
            warning_window.CreateWarning(parent, warning_msg)
            # value potentially changed by the warning window if user picked "yes" to delete
            if parent.get_change():
                parent.remove_platform(name)
                self.destroy()
                parent.store_changes(False)

        elif value != "":
            is_valid, error_msg = parent.is_valid_input(value)
            if not is_valid:
                error_window.AddError(self, error_msg)
                destroy = False

        # user is trying to enter a blank value
        else:
            curr_values = parent.get_platform_standard(name)
            if change_type == "LUFS Value" and curr_values[1] == "":
                error_window.AddError(self, "Platform must have at least one valid standard")
                destroy = False
            elif change_type == "Peak Value" and curr_values[0] == "":
                error_window.AddError(self, "Platform must have at least one valid standard")
                destroy = False
        if destroy:
            parent.set_platform_standard(name, change_type, value)
            self.destroy()
