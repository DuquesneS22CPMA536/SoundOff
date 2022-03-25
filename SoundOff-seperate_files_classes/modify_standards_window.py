from tkinter import *
import error_window
import warning_window
from warning_window import *


class Modify(tk.Toplevel):
    """A window to modify or delete existing changes

        Will take input from user to ask what changes should be made and then use the parent SoundOff window
        to make changes

    """
    def __init__(self, parent):
        """Initializes the modify/delete standards window

        Will modify existing standards or delete existing standards

        Args:
          self: The new window
          parent: App object, window it came from

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("Modify Standards")
        self.geometry("450x100")

        standard_names = parent.get_standard_names_dict()
        selected_name = StringVar()
        selected_name.set(standard_names[0])
        selected_lufs_peak = StringVar()
        selected_lufs_peak.set("LUFS Value")

        drop_standards = OptionMenu(
            self,
            selected_name,
            *standard_names)

        drop_lufs_peak = OptionMenu(
            self,
            selected_lufs_peak,
            "LUFS Value",
            "Peak Value",
            "Delete Standard"
        )
        drop_standards.config(width=25)
        drop_standards.config(height=1)
        drop_standards.config(bg="#6f67c2")
        drop_standards.config(fg="white")
        drop_standards.config(font=("Helvetica", 10))
        drop_lufs_peak.config(width=15)
        drop_lufs_peak.config(height=1)
        drop_lufs_peak.config(bg="#6f67c2")
        drop_lufs_peak.config(fg="white")
        drop_standards.grid(column=0, row=0)
        drop_lufs_peak.grid(column=1, row=0)

        blank_value = StringVar(self)
        blank_value.set("")
        new_value_tf = Entry(
            self,
            textvariable=blank_value,
            width=13
        )

        new_value_tf.grid(column=2, row=0)

        enter_button = ttk.Button(
            self,
            text="Enter",
            command=lambda: self.modify_existing_standards(
                selected_name.get(),
                selected_lufs_peak.get(),
                new_value_tf.get(),
                self,
                parent
            )
        )
        enter_button.grid(column=0, row=1)

    def modify_existing_standards(
            self,
            name,
            value_type,
            value,
            window,
            parent
    ):

        destroy = True
        if value_type == "Delete Standard":
            destroy = False
            warning_msg = "Do you want to delete "+name+"?"
            warning = warning_window.CreateWarning(parent, warning_msg)
            warning.wait_window()

            if parent.get_change():
                parent.remove_standard(name)
                self.destroy()

        elif value != "":
            if value[0] == '-':
                if not value[1:].isnumeric():
                    error_window.AddError(self, "Enter a numeric value")
                    destroy = False
            else:
                error_window.AddError(self, "Must be negative")
                destroy = False

        if destroy:
            parent.set_standard_value(name, value_type, value)
            window.destroy()
