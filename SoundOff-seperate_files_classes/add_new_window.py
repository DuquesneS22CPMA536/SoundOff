from tkinter import *
import error_window
from error_window import *


class AddNew(tk.Toplevel):
    def __init__(self, parent):
        """Initializes the add new

        IDK more information about what the application
        does?

        Args:
          self: An add new variable object
          parent: App object, window it came from

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("Add a New Standard")
        self.geometry("490x80")

        standard_label = ttk.Label(
            self,
            text="Standard Name"
        )
        lufs_label = ttk.Label(
            self,
            text="LUFS Value"
        )
        peak_label = ttk.Label(
            self,
            text="Peak Value"
        )
        enter_button = ttk.Button(
            self,
            text="Enter",
            command=lambda: self.add_new_standard(
                standard_value_entry_tf.get(),
                lufs_value_entry_tf.get(),
                peak_value_entry_tf.get(),
                self,
                parent
            )
        )

        name1 = StringVar(self)
        name2 = StringVar(self)
        name3 = StringVar(self)

        standard_value_entry_tf = ttk.Entry(
            self,
            textvariable=name1
        )
        lufs_value_entry_tf = ttk.Entry(
            self,
            textvariable=name2
        )
        peak_value_entry_tf = ttk.Entry(
            self,
            textvariable=name3
        )

        # put all of our crap on the screen
        standard_label.grid(column=0, row=0)
        lufs_label.grid(column=1, row=0)
        peak_label.grid(column=2, row=0)
        standard_value_entry_tf.grid(column=0, row=1)
        lufs_value_entry_tf.grid(column=1, row=1)
        peak_value_entry_tf.grid(column=2, row=1)
        enter_button.grid(column=0, row=2)

    def add_new_standard(self, standard_name, lufs_value, peak_value, window, parent):

        destroy = True
        if standard_name in parent.get_standard_names_lower():
            error_window.AddError(self, "Standard name already exists")
            destroy = False

        elif standard_name == "":
            error_window.AddError(self, "Standard name already exists")
            destroy = False

        if lufs_value != "":
            # make sure we have negative numbers
            if lufs_value[0] == '-':
                # we most likely have a valid input
                if not lufs_value[1:].isnumeric():
                    error_window.AddError(self, "You must enter a numeric LUFS value")
                    destroy = False
            else:
                error_window.AddError(self, "You must enter a negative LUFS value")
                destroy = False

        if peak_value != "":
            if peak_value[0] == '-':
                # we most likely have a valid input
                if not peak_value[1:].isnumeric():
                    error_window.AddError(self, "You must enter a numeric peak value")
                    destroy = False
            else:
                error_window.AddError(self, "You must enter a negative peak value")
                destroy = False

        if destroy:
            parent.add_to_standard_dict(
                standard_name,
                (lufs_value, peak_value)
            )
            window.destroy()
