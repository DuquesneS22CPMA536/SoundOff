import tkinter as tk
from tkinter import ttk


class CreateWarning(tk.Toplevel):
    """A warning window.

        Will make sure user is sure about what they clicked

    """
    def __init__(self, parent, warning):
        """Initializes the create warning window

        more info

        Args:
          self: The instance of the create warning window
          parent: App object, window it came from
          warning: The warning being made to be printed on screen

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("WARNING")

        size_x = 150 + len(warning)*7
        size = str(size_x)+"x50"
        self.geometry(size)

        # define labels and widgets to be placed on screen
        warning_msg = ttk.Label(
            self,
            text="Warning: " + warning,
            style="WarningMsg.TLabel"
        )
        yes = ttk.Button(
            self,
            text="Yes",
            command=lambda: self.exit_window("Yes", parent),
            style="Yes_No.TButton"
        )
        no = ttk.Button(
            self,
            text="No",
            command=lambda: self.exit_window("No", parent),
            style="Yes_No.TButton"
        )

        # define the look of our labels and widgets
        style = ttk.Style()
        style.configure(
            "WarningMsg.TLabel",
            foreground="red",
            font=("Helvetica", 10)
        )
        style.configure(
            "Yes_No.TButton",
            background="white",
            font=("Helvetica", 10, "bold")
        )

        # place labels and widgets on screen
        warning_msg.grid(column=0, row=0, columnspan=2)
        yes.grid(column=0, row=1)
        no.grid(column=1, row=1)

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)

    def exit_window(self, response, parent):
        """Will store changes based on user response from the warning window.

        Will use store_changes() function to store whether a user wishes to keep changes made or not.

        Args:
            self: The instance of the create warning window
            response: Yes/No response from user
            parent: App object, the original, main window

        Raises:
            Any errors raised should be put here

        """
        if response == "Yes":
            parent.store_changes(True)
        else:
            parent.store_changes(False)

        self.destroy()
