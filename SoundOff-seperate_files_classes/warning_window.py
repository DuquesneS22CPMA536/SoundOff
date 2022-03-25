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
          self: An add new variable object
          parent: App object, window it came from
          warning: The warning being made to be printed on screen

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("WARNING")
        self.geometry("300x80")

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

        warning_msg.grid(column=0, row=0, columnspan=2)
        yes.grid(column=0, row=1)
        no.grid(column=1, row=1)

    def exit_window(self, response, parent):
        if response == "Yes":
            parent.store_changes(True)
        else:
            parent.store_changes(False)

        self.destroy()
