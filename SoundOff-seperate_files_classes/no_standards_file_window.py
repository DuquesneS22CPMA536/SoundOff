import tkinter as tk
from tkinter import ttk
import sqlite3


class NoStandardsWindow(tk.Toplevel):
    """A window to display an error in the standards.db file

    Will display the message that the standards.db file must be held in the same file as the program. Will also
    automatically exit out of the main window, as it cannot function without the standards.db file.

    """

    def __init__(self, parent):
        """Initializes the no standards.db file found window.

        Will display the error message and prompt user to close this window and the main window.

        Args:
          self: The no standards.db file found window
          parent: The main window

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        self.geometry("500x80")

        # define the error message and button for user to acknowledge error
        error_msg = ttk.Label(
            self,
            text="Error: You must have the standards.db file downloaded within the same folder",
            style="ErrorMsg.TLabel"
        )
        okay = ttk.Button(
            self,
            text="Okay",
            command=lambda: parent.destroy(),
            style="Okay.TButton"
        )
        create_button = ttk.Button(
            self,
            text="Create a new standards.db (empty) file",
            command=lambda: self.create_blank(),
            style="Okay.TButton"
        )

        # define look of our error message and button
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
        error_msg.grid(column=0, row=0, columnspan=2, sticky="w")
        okay.grid(column=0, row=1)
        create_button.grid(column=1, row=1)

        # catch whether a user exits early
        def if_closed():
            parent.destroy()
        self.protocol("WM_DELETE_WINDOW", if_closed)

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)

    def create_blank(self):
        """Creates a blank table within the standards.db file

        Will create a functioning table within the standards.db file so that if a user deletes the standards.db file,
        the program will still function, just without any platform standards.

        Args:
            self: The no standards.db file found window

        Raises:
            Any errors raised should be put here

        """
        connection = sqlite3.connect('standards.db')
        cursor = connection.cursor()

        create_table = """CREATE TABLE Standards(
                        Standard_Name CHAR,
                        LUF_Value FLOAT,
                        Peak_Value FLOAT
                        )"""

        cursor.execute(create_table)

        connection.commit()
        connection.close()

        self.destroy()
