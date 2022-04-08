import tkinter as tk
from tkinter import ttk


class AddError(tk.Toplevel):
    """An error window.

        Will print an error that occurs

    """
    def __init__(self, parent, error):
        """Initializes the error window

        Will print a clear error made by the user and prompt the user's acknowledgment of this error

        Args:
          self: The instance of the error window
          parent: App object, window it came from
          error: The error to print on window

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("ERROR")
        size = str(len(error)*6+100)+"x70"
        self.geometry(size)

        # define label and button
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
        
        def enter_key_clicked(event):
            self.exit_window()

        self.bind("<Return>", enter_key_clicked)

        # define look of our widgets
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

        # place our widgets on the screen
        error_msg.grid(column=0, row=0)
        okay.grid(column=0, row=1)

    def exit_window(self):
        """Exit the error window

        Will exit the error window by using the destroy function

        Args:
            self: The instance of the error window

        Raises:
            Any errors raised should be put here

        """
        self.destroy()
