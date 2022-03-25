import tkinter as tk
from tkinter import ttk


class AddError(tk.Toplevel):
    """An error window.

        Will print an error that occurs

    """
    def __init__(self, parent, error):
        """Initializes the add new

        IDK more information about what the application
        does?

        Args:
          self: An add new variable object
          parent: App object, window it came from
          error: The error to print on window

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("ERROR")
        self.geometry("300x80")

        style = ttk.Style()

        style.configure(
            "ErrorMsg.TLabel",
            foreground="red",
            font=("Helvetica", 10)
        )

        style.configure(
            "Okay.TButton",
            background="white",
            font=("Helvetica", 10, "bold")
        )

        error_msg = ttk.Label(
            self,
            text="Error: " + error,
            style="ErrorMsg.TLabel"
        )

        okay = ttk.Button(
            self,
            text="Okay",
            command=lambda: self.exit_window(),
            style="Okay.TButton"
        )

        error_msg.pack()
        okay.pack()

    def exit_window(self):
        self.destroy()
