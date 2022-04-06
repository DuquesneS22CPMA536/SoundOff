from tkinter import filedialog as fd
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter import Listbox
from tkinter import Label
from tkinter import OptionMenu
from tkinter import StringVar
from tkinter import Entry
import soundfile as sf
import pyloudnorm as pyln
import numpy as np
import scipy
from scipy import signal
import math
import resampy
import statistics


class App(tk.Tk):
    """A SoundOff window.

    Will hold a primary window with functions to select a wav file, test the wav file's peak value
    against a standard's peak value, and test the wav file's LUF value against a standard's LUF
    value.

    Attributes:
        file_path: The current audio file path to be tested. Can change frequently. String object.
        platforms: a dictionary of current platforms with lufs and peak values
        make_changes: a boolean value used by the warning window to hold whether the user wishes to
        make a change
      """

    def __init__(self, master=None):
        """Initializes the main window application

        Will hold buttons for the main functions and store platform information by accessing the
        standards.db file

        Args:
          self: The main window
          master: no master, this is the first instance of a window

        Raises:
          Any errors raised should be put here

        """
        super().__init__(master)
        # create basic window properties
        self.title("SoundOff")
        self.geometry("1048x775")
        self.configure(bg="#2d2933")
        self.iconbitmap('SoundOff.ico')

        # initialize path of the file being passed in
        self.file_path = ""

        # a dictionary to store platform standards, initialized to query from standards database
        self.platforms = {}

        # True/False value to store whether to make changes after warning message
        self.make_changes = False

        # define our labels and widgets to be placed on the screen
        self.open_audio_file = ttk.Button(
            self,
            text="Select a file",
            command=self.select_audio_file,
            style="File.TButton"
        )
        self.welcome_label = ttk.Label(
            self,
            text="Welcome to SoundOff!",
            style="Greeting.TLabel"
        )
        self.blank_label = ttk.Label(
            self,
            text="",
            width=16,
            style="Blank.TLabel"
        )
        self.blank_label2 = ttk.Label(
            self,
            text="",
            width=16,
            style="Blank.TLabel"
        )
        # create buttons dealing with platforms
        self.add_button = ttk.Button(
            self,
            text="Add a new platform",
            command=lambda: AddNew(self),
            style="Add.TButton"
        )
        self.modify_button = ttk.Button(
            self,
            text="Modify/Delete existing platform standards",
            command=lambda: Modify(self),
            style="Add.TButton"
        )
        self.view_button = ttk.Button(
            self,
            text="View existing platform standards",
            command=lambda: ViewPlatforms(self),
            style="Add.TButton"
        )

        # define the look of our labels and widgets
        style = ttk.Style()
        style.configure(
            "Greeting.TLabel",
            foreground="white",
            background="#2d2933",
            font=('Helvetica', 35)
        )
        style.configure(
            "File.TButton",
            foreground="#2d2933",
            background="white",
            border=0,
            font=('Helvetica', 18)
        )
        style.configure(
            "Add.TButton",
            foreground="#2d2933",
            background="white",
            border=0,
            font=('Helvetica', 10)
        )
        style.configure(
            "Blank.TLabel",
            foreground="#2d2933",
            background="#2d2933",
            font=('Helvetica', 8)
        )

        # place our widgets on the screen
        self.open_audio_file.grid(column=1, row=2, ipadx=30, ipady=18, pady=20, sticky="nsew")
        self.welcome_label.grid(column=1, row=0, pady=60, sticky="nsew")
        self.blank_label2.grid(column=1, row=3, pady=200)
        self.add_button.grid(column=0, row=10, pady=20, padx=80)
        self.modify_button.grid(column=1, row=10, pady=20)
        self.view_button.grid(column=2, row=10, pady=20, padx=30)

        # connect to standards database
        # make sure it's in the same folder as main file
        try:
            connection = sqlite3.connect('standards.db')
            cursor = connection.cursor()

            # define empty dictionary to store platform names and LUFS and peak max values
            not_sorted_platforms = {}
            platform_info = cursor.execute('''SELECT * FROM Standards''')
            for platform_name in platform_info:
                # key for dictionary = platform name
                # value for dictionary = (lufs,peak)
                not_sorted_platforms[platform_name[0]] = (platform_name[1], platform_name[2])
            # sort by platform names
            sorted_names = sorted(not_sorted_platforms)
            self.platforms = {key: not_sorted_platforms[key] for key in sorted_names}
            # close connection to database
            connection.commit()
            connection.close()
        except sqlite3.OperationalError:
            # create an error window which will destroy the main window
            NoStandardsWindow(self)

    def change_file_path(self, new_file_path):
        """Changes the file path.

        Makes change to the file path, which is an attribute of this instance of App class.
        This will change the attribute used by the view report window.

        Args:
          self: Instance of main window
          new_file_path: The new file name (or path) of the wav file to be tested. A string object

        Raises:
          Any errors raised should be put here

        """
        self.file_path = new_file_path

    def get_file_path(self):
        """ Gives the current file name being stored by the app

        Returns the filename attribute being stored.

        Args:
            self: Instance of main window

        Returns:
            file_path: the file path of the audio file selected by the user

        Raises:
            Any errors raised should be put here

        """
        return self.file_path

    def add_to_platforms(self, name, value):
        """ Add a new platform to both the platform dictionary and standards.db file

        Will add the new standard along with luf values and peak values to the standard dictionary
        and the standards.db database

         Args:
            self: Instance of main window
            name: The name of the platform to add
            value: The LUFS and Peak value. A tuple in the form of (luf,peak).

        Raises:
            Any errors raised should be put here
        """
        if value[0] != "":
            lufs = value[0]
            lufs_value = float(lufs)
        else:
            lufs_value = ""
        if value[1] != "":
            peak = value[1]
            peak_value = float(peak)
        else:
            peak_value = ""

        # before we add this new platform to the platform dictionary, sort it
        not_sorted_platforms = self.platforms
        not_sorted_platforms[name] = (lufs_value, peak_value)
        sorted_names = sorted(not_sorted_platforms)
        self.platforms = {key: not_sorted_platforms[key] for key in sorted_names}

        # now update database
        connection = sqlite3.connect('standards.db')
        cursor = connection.cursor()

        insert_query = """INSERT INTO Standards
                        (Standard_Name, LUF_Value, Peak_Value)
                        VALUES
                        (?,?,?)"""

        cursor.execute(insert_query, (name, lufs_value, peak_value))
        connection.commit()
        connection.close()

    def is_valid_input(self, input):
        """ Gives the standard names stored within the standard dictionary.

        Returns the standard names currently being stored as list.

        Args:
            self: Instance of main window
            curr_input: the LUFS or peak input a user is trying to include as a platform standard

        Returns:
            is_valid: a boolean value for whether the input is valid or not
            error_msg: the error message to report if the input is not valid

        Raises:
            Any errors raised should be put here
        """
        error_msg = ""
        is_valid = True
        if input[0] == '-':
            if not input[1:].isnumeric():
                split_value = input[1:].split(".")
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


    def get_platform_names(self):
        """ Gives the standard names stored within the standard dictionary.

        Returns the standard names currently being stored as list.

        Args:
            self: Instance of main window

        Returns:
            name_list: A list of all the names currently being stored.

        Raises:
            Any errors raised should be put here
        """
        name_list = []
        for key in self.platforms:
            name_list.append(key)
        return name_list

    def get_platform_names_lower(self):
        """ Gives the standard names stored within the standard dictionary in lower case

        Returns the standard names in lower case in a list. To be used to check whether a name is
        being stored, not to display the names.

        Args:
            self: Instance of main window

        Returns:
            name_list: A list of all the names currently being stored.

        Raises:
            Any errors raised should be put here
        """
        name_list = []
        for key in self.platforms:
            name_list.append(key.lower())
        return name_list

    def get_platform_standard(self, name):
        """ Gives the standard values for a platform passed

        Returns the LUFS and Peak values for the platform

        Args:
            self: Instance of main window
            name: the name of the platform we will return lufs and peak values for

        Returns:
            A tuple in the form of (max integrated LUFS, max true peak dB)

        Raises:
            Any errors raised should be put here

        """
        return self.platforms.get(name)

    def set_platform_standard(self, name, value_type, new_value):
        """ Set (change) an existing platform standard

        Will change the platforms dictionary and the standards.db database based on changes passed
        by user

        Args:
            self: Instance of main window
            name: The name of the platform
            value_type: Whether the user wishes to change the LUFS or peak value
            new_value: The new value to change to. A string.

        Raises:
            Any errors raised should be put here
        """
        if new_value != "":
            new_value_float = float(new_value)
        else:
            new_value_float = ""
        if value_type == "Integrated Loudness (LUFS)":
            curr_value = list(self.get_platform_standard(name))
            curr_value[0] = new_value_float
            self.platforms[name] = tuple(curr_value)
            # now update database
            connection = sqlite3.connect('standards.db')
            cursor = connection.cursor()
            update_query = """UPDATE Standards
                            SET LUF_Value = ?
                            WHERE Standard_Name = ?"""
            cursor.execute(update_query, (new_value_float, name))
            connection.commit()
            connection.close()
        else:
            curr_value = list(self.get_platform_standard(name))
            curr_value[1] = new_value_float
            self.platforms[name] = tuple(curr_value)
            # now update database
            connection = sqlite3.connect('standards.db')
            cursor = connection.cursor()
            update_query = """UPDATE Standards
                            SET Peak_Value = ?
                            WHERE Standard_Name = ?"""
            cursor.execute(update_query, (new_value_float, name))
            connection.commit()
            connection.close()

    def remove_platform(self, name):
        """ Removes the platform name passed

        Removes the platform from the platform dictionary as well as the standards.db database

        Args:
            self: Instance of main window
            name: the name of the platform we will remove

        Raises:
            Any errors raised should be put here

        """
        self.platforms.pop(name)
        connection = sqlite3.connect('standards.db')
        cursor = connection.cursor()
        delete_query = """DELETE FROM Standards
                            WHERE Standard_Name = ?"""
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()

    def get_max_platform_name_length(self):
        """Returns the length of the longest platform name

        Uses the get_platform_names method to get a list of all platform names and then find the
        maximum length of these. Will be used to configure window sizes that use platform names.

        Args:
            self: Instance of main window

        Raises:
            Any errors raised should be put here

        """
        name_list = self.get_platform_names()
        max_length = 0
        for name in name_list:
            if len(name) > max_length:
                max_length = len(name)
        return max_length

    def store_changes(self, value):
        """Stores whether a user should make changes after a warning window.

        Will be used by the warning window if a user selects yes after a warning. Will also be used
        by the window that prompted the warning after the changed has been made to reset the value.

        Args:
            self: Instance of main window
            value: A boolean value

        Raises:
            Any errors raised should be put here

        """
        if value:
            self.make_changes = True
        else:
            self.make_changes = False

    def get_change(self):
        """Returns whether a user should make changes after a warning window.

        Will also be used by the window that prompted a warning to see if the user wishes to do the
        action that caused a warning.

        Args:
            self: Instance of main window

        Returns:
            A boolean value for whether a user should make a change or not.

        Raises:
            Any errors raised should be put here

        """
        return self.make_changes

    def select_audio_file(self):
        """ Prompts user for an audio file path.

        Uses askopenfilename to select can audio file to be tested.

        Args:
          self: Instance of main window

        Raises:
          Any errors raised should be put here

        """
        # file types to accept
        filetypes = (
            ("WAV file", "*.wav"),
            ("FLAC file", "*.flac"),
            ("All files", "*.*")
        )
        filename = fd.askopenfilename(
            title="Select a file",
            initialdir='/',
            filetypes=filetypes
        )

        self.change_file_path(filename)

        if self.get_file_path() != "":
            Report(self, self.get_file_path())

    def open_wav_file(self):
        """Opens the wav file and fetches its needed information.

        Opens the selected wav file and fetches its sample rate, data itself, length of data, and
        number of channels.

        Args:
            self: An App Object.

        Returns:
            A tuple containing the selected wav file's sample rate, data, length of data, and number
             of channels.

        Raises:
            Add possible errors here.

        """
        data, rate = sf.read(self.get_file_path())
        length_file = len(data)
        if len(data.shape) > 1:
            n_channels = data.shape[1]
        else:
            n_channels = 1
        wav_info = (data, rate, length_file, n_channels)
        return wav_info

    def get_luf(self, wav_info):
        """Returns the integrated loudness in LUFS of an audio file.

        Uses pyloudnorm to find the LUFS of an audio file found at a file path passed.

        Args:
            self: Instance of main window
            wav_info: a tuple of the selected wav file's sample rate, data, length of data, number
                of channels

        Returns:
            The integrated loudness of the audio file in LUFS

        Raises:
            Any errors raised should be put here

        """

        meter = pyln.Meter(wav_info[1])  # create meter; wav_info[1] is the rate
        lufs = meter.integrated_loudness(wav_info[0])  # get lufs value; wav_info[0] is the data
        return lufs

    def get_peak(self, wav_info):
        """Returns the true peak in dBFS of an audio file.

        Uses some method to find the peak of an audio file found at a file path passed.

        Args:
            self: Instance of main window
            wav_info: a tuple of the selected wav file's sample rate, data, length of data, number
                of channels

        Returns:
            The true peak of the audio file in dB

        Raises:
            Any errors raised should be put here

        """
        resampling_factor = 4  # use a resampling factor of 4

        # calculate number of samples in resampled file
        samples = wav_info[2] * resampling_factor  # wav_info[2] is the length of the data

        # resample using FFT
        new_audio = scipy.signal.resample(wav_info[0], samples)
        current_peak1 = np.max(np.abs(new_audio))  # find peak value
        current_peak1 = math.log(current_peak1, 10) * 20  # convert to decibels

        # resample using resampy
        new_audio = resampy.resample(wav_info[0], wav_info[2], samples, axis=-1)
        current_peak2 = np.max(np.abs(new_audio))  # find peak value
        current_peak2 = math.log(current_peak2, 10) * 20  # convert to decibels

        # resample using polynomial
        new_audio = scipy.signal.resample_poly(wav_info[0], resampling_factor, 1)
        current_peak3 = np.max(np.abs(new_audio))  # find peak value
        current_peak3 = math.log(current_peak3, 10) * 20  # convert to decibels

        # get and return median of the three techniques
        peak = statistics.median([current_peak1, current_peak2, current_peak3])
        return peak


class NoStandardsWindow(tk.Toplevel):
    """A window to display an error in the standards.db file

    Will display the message that the standards.db file must be held in the same file as the
    program. Will also automatically exit out of the main window, as it cannot function without the
    standards.db file.

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
            command=parent.destroy(),
            style="Okay.TButton"
        )
        create_button = ttk.Button(
            self,
            text="Create a new standards.db (empty) file",
            command=self.create_blank(),
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

        Will create a functioning table within the standards.db file so that if a user deletes the
        standards.db file, the program will still function, just without any platform standards.

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


class Report(tk.Toplevel):
    """A window to report the LUFS and peak value of the file selected.

        Will prompt the user to select the type of report (which standards to test against) to view.

    """
    def __init__(self, parent, file_path):
        """Initializes the view report window

        Will provide user with the LUFS and true peak value of the audio file passed. Will also
        prompt the user to select the platform and standard type to test the audio file against.

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
        max_name_length = parent.get_max_platform_name_length()
        size = str(max_name_length * 6 + 450) + "x500"
        self.geometry(size)

        # get LUFS and peak from audio file
        wav_info = parent.open_wav_file()
        lufs = parent.get_luf(wav_info)
        peak = parent.get_peak(wav_info)
        data, sample_rate, length_of_data, num_channels = parent.open_wav_file()

        # get platform names to be used in drop-down widget
        platform_names = parent.get_platform_names()
        # preselect first option so if a user does not click drop down list, it is assumed
        # they wanted the first option
        selected_lufs_peak = StringVar()
        selected_lufs_peak.set("LUFS and Peak")

        # only print first 50 characters of the file path
        if len(file_path) > 50:
            new_file_path = file_path[:50] + "..."
        else:
            new_file_path = file_path

        # define labels and widgets to be placed on the screen
        selected_file_label = ttk.Label(
            self,
            text="Selected file path: " + new_file_path,
            font=("Helvetica", 10, "bold")
        )
        directions_label = ttk.Label(
            self,
            text="Please select the type of report you wish you view",
            font=("Helvetica", 10, "bold")
        )
        scrollbar = ttk.Scrollbar(self)
        scrollbar.grid(column=0, row=7, sticky="ns")
        listbox_of_platforms = Listbox(
            self,
            bg="#6f67c2",
            fg="white",
            font="Helvetica",
            selectbackground="#2d2933",
            selectmode="multiple",
            yscrollcommand=scrollbar.set,
            width=10 + parent.get_max_platform_name_length()
        )
        for name in platform_names:
            listbox_of_platforms.insert("end", name)

        drop_lufs_peak = OptionMenu(
            self,
            selected_lufs_peak,
            "LUFS and Peak",
            "LUFS Value",
            "Peak Value",
        )
        lufs_value_label = Label(
            self,
            text="Your Integrated Loudness (LUFS) = " + "{:.1f}".format(lufs)
        )
        peak_value_label = Label(
            self,
            text="Your True Peak (dBFS) = " + "{:.1f}".format(peak)
        )
        sample_rate_label = Label(
            self,
            text="Your Sample Rate (Hz) = " + str(sample_rate)
        )
        num_channels_label = Label(
            self,
            text="Your number of channels = " + str(num_channels)
        )
        blank_label = Label(
            self,
            text=""
        )
        enter_button = ttk.Button(
            self,
            text="Select",
            style="Enter.TButton",
            command=lambda: make_selection()

        )
        select_all_button = ttk.Button(
            self,
            text="Select All Platforms",
            style="Enter.TButton",
            command=lambda: View(
                parent,
                platform_names,
                selected_lufs_peak.get(),
                peak,
                lufs,
                self
            )
        )

        def make_selection():
            selected_names = []
            for curr_name in listbox_of_platforms.curselection():
                selected_names.append(listbox_of_platforms.get(curr_name))

            View(
                parent,
                selected_names,
                selected_lufs_peak.get(),
                peak,
                lufs,
                self
            )

        # change look of labels and widgets
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
        directions_label.grid(column=0, row=6, columnspan=4, sticky="w")
        listbox_of_platforms.grid(column=0, row=7, sticky="w", padx=5)
        drop_lufs_peak.grid(column=1, row=7, sticky="n")
        lufs_value_label.grid(column=0, row=1, sticky="w")
        peak_value_label.grid(column=0, row=2, sticky="w")
        sample_rate_label.grid(column=0, row=3, sticky="w")
        num_channels_label.grid(column=0, row=4, sticky="w")
        blank_label.grid(column=0, row=5, pady=10)
        enter_button.grid(column=0, row=8, sticky="w", padx=5)
        select_all_button.grid(column=0, row=9, sticky="w", padx=5)

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)


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
        yes_button = ttk.Button(
            self,
            text="Yes",
            command=lambda: self.exit_window("Yes", parent),
            style="Yes_No.TButton"
        )
        no_button = ttk.Button(
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
        yes_button.grid(column=0, row=1)
        no_button.grid(column=1, row=1)

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)

    def exit_window(self, response, parent):
        """Will store changes based on user response from the warning window.

        Will use store_changes() function to store whether a user wishes to keep changes made or
        not.

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
                self,
                parent
            )
        )

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

    def add_new_standard(self, platform_name, lufs_value, peak_value, window, parent):
        """Uses input from add new window to make changes to original window.

        Will add a new platform with corresponding max integrated (LUFS) and max true peak (dB) by
        calling the add_to_standard_dict method within the main window class. Calls the error window
        method when an error in user input was made.

        Args:
            self: The instance of the add new standard window
            platform_name: The name of the platform
            lufs_value: The max integrated (LUFS) value
            peak_value: The max true peak (dB)
            window: The add new window
            parent: App object, window it came from

        Raises:
        Any errors raised should be put here

        """
        # some errors may be found with user input, destroy is a boolean variable that marks whether
        # an error was raised, if so the window may be destroyed
        destroy = True
        if platform_name in parent.get_platform_names_lower():
            AddError(self, "Platform name already exists")
            destroy = False
        elif platform_name == "":
            AddError(self, "Please enter a platform name")
            destroy = False

        if lufs_value != "":
            # make sure we have negative numbers
            is_valid, error_msg = parent.is_valid_input(lufs_value)
            if not is_valid:
                AddError(self, error_msg)
                destroy = False

        if peak_value != "":
            is_valid, error_msg = parent.is_valid_input(peak_value)
            if not is_valid:
                AddError(self, error_msg)
                destroy = False

        if lufs_value == "" and peak_value == "":
            AddError(self, "Please enter either a max integrated loudness or max true peak value.")
            destroy = False

        # an error was not found with the latest input, changes can be made and the window can be
        # destroyed
        if destroy:
            parent.add_to_platforms(
                platform_name,
                (lufs_value, peak_value)
            )
            window.destroy()


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
        calling the add_to_standard_dict method within the main window class. Calls the error window
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
            CreateWarning(parent, warning_msg)
            # value potentially changed by the warning window if user picked "yes" to delete
            if parent.get_change():
                parent.remove_platform(name)
                self.destroy()
                parent.store_changes(False)

        elif value != "":
            is_valid, error_msg = parent.is_valid_input(value)
            if not is_valid:
                AddError(self, error_msg)
                destroy = False

        # user is trying to enter a blank value
        else:
            curr_values = parent.get_platform_standard(name)
            if change_type == "LUFS Value" and curr_values[1] == "":
                AddError(self, "Platform must have at least one valid standard")
                destroy = False
            elif change_type == "Peak Value" and curr_values[0] == "":
                AddError(self, "Platform must have at least one valid standard")
                destroy = False
        if destroy:
            parent.set_platform_standard(name, change_type, value)
            self.destroy()


class View(tk.Toplevel):
    """A window to view the report of the lufs and peak values against the standards selected within
     the report results window

    Will use a scrollable frame to print results.

    """
    def __init__(self, parent, names_selected, lufs_or_peak, peak, lufs, report_window):
        """Initializes the view report window

        Will print the report a user selected in the report results window. Will print the report in
        a scrollable frame.

        Args:
          self: The instance of the view results window
          parent: App object, window it came from
          names_selected: a list of all names to report for
          lufs_or_peak: whether to test against lufs, peak, or both
          peak: the peak value of the file to test
          lufs: the lufs value of the file to test
          report_window: the previous window, will destroy upon initialization

        Raises:
          Any errors raised should be put here

        """
        report_window.destroy()
        super().__init__(parent)
        # create basic window properties
        self.title("View Report")
        max_name_length = parent.get_max_platform_name_length()
        size = str(max_name_length * 6 + 750) + "x300"
        self.geometry(size)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=1)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # define a style of labels to display
        style = ttk.Style()
        style.configure(
            "Input.TLabel",
            foreground="white",
            background="#333147",
            font=('Helvetica', 10)
        )
        style.configure(
            "Column.TLabel",
            font=("Helvetica", 11, "bold")
        )
        style.configure(
            "Result.TLabel",
            font=("Helvetica", 10)
        )
        style.configure(
            "Pass.TLabel",
            foreground="green",
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "Fail.TLabel",
            foreground="red",
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "Close.TLabel",
            foreground="orange",
            font=("Helvetica", 10, "bold")
        )

        # create header labels
        platform_name_label = ttk.Label(
            scrollable_frame,
            text="Platform Name",
            style="Column.TLabel")
        max_lufs_label = ttk.Label(
            scrollable_frame,
            text="Max Integrated Loudness (LUFS)",
            style="Column.TLabel")
        max_peak_label = ttk.Label(
            scrollable_frame,
            text="Max True Peak (dBFS)",
            style="Column.TLabel")
        lufs_result_label = ttk.Label(
            scrollable_frame,
            text="LUFS Result",
            style="Column.TLabel")
        peak_result_label = ttk.Label(
            scrollable_frame,
            text="Peak Result",
            style="Column.TLabel")
        input_lufs_label = ttk.Label(
            scrollable_frame,
            text="Input Integrated Loudness (LUFS) from file: " + "{:.1f}".format(lufs),
            style="Input.TLabel")
        input_peak_label = ttk.Label(
            scrollable_frame,
            text="Input True Peak (dBFS) from file: " + "{:.1f}".format(peak),
            style="Input.TLabel")

        # always display platform name header
        platform_name_label.grid(column=0, row=1, padx=5)

        # only display headers for the type of report requested
        if lufs_or_peak == "LUFS Value":
            max_lufs_label.grid(column=1, row=1, padx=5)
            lufs_result_label.grid(column=2, row=1)
            input_lufs_label.grid(column=0, row=0, columnspan=2)
        elif lufs_or_peak == "Peak Value":
            max_peak_label.grid(column=1, row=1, padx=5)
            peak_result_label.grid(column=2, row=1)
            input_peak_label.grid(column=0, row=0, columnspan=2)
        else:
            max_lufs_label.grid(column=1, row=1, padx=5)
            max_peak_label.grid(column=2, row=1, padx=5)
            lufs_result_label.grid(column=3, row=1, padx=5)
            peak_result_label.grid(column=4, row=1, padx=5)
            input_lufs_label.grid(column=0, row=0, columnspan=2, padx=10)
            input_peak_label.grid(column=2, row=0, columnspan=2)

        i = 2
        for name in names_selected:
            name_label = ttk.Label(
                scrollable_frame,
                text=name,
                style="Result.TLabel"
            )

            values = parent.get_platform_standard(name)
            # format the max lufs and peak to only display one decimal point
            if values[0] != "":
                lufs_from_platform = "{:.1f}".format(values[0])
            else:
                lufs_from_platform = ""
            if values[1] != "":
                peak_from_platform = "{:.1f}".format(values[1])
            else:
                peak_from_platform = ""

            # create labels for the max luf and peak from the current platform
            lufs_label = ttk.Label(
                scrollable_frame,
                text=lufs_from_platform,
                style="Result.TLabel"
            )

            peak_label = ttk.Label(
                scrollable_frame,
                text=peak_from_platform,
                style="Result.TLabel"
            )

            # test whether the input luf value is less than or equal to the max luf value
            # if true: pass, if false: fail
            if values[0] == "":
                result_lufs = ttk.Label(
                    scrollable_frame,
                    text=""
                )
            elif values[0] - lufs > 2:
                result_lufs = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(lufs-values[0])),
                    style="Pass.TLabel"
                )
            elif values[0] - lufs > - 2:
                result_lufs = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(lufs-values[0])),
                    style="Close.TLabel"
                )
            else:
                result_lufs = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(lufs-values[0])),
                    style="Fail.TLabel"
                )
            # test whether the input peak value is less than or equal to the max peak value
            # if true: pass, if false: fail
            if values[1] == "":
                result_peak = ttk.Label(
                    scrollable_frame,
                    text=""
                )
            elif values[1] - peak > .5:
                result_peak = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(peak-values[1])),
                    style="Pass.TLabel"
                )
            elif values[1] - peak > -.5:
                result_peak = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(peak-values[1])),
                    style="Close.TLabel"
                )
            else:
                result_peak = ttk.Label(
                    scrollable_frame,
                    text="{:.1f}".format(-(peak-values[1])),
                    style="Fail.TLabel"
                )
            # always place name on the screen
            name_label.grid(column=0, row=i, padx=5, sticky="w")

            # only display report the user requested
            if lufs_or_peak == "LUFS Value":
                lufs_label.grid(column=1, row=i, padx=5)
                result_lufs.grid(column=2, row=i, padx=5)
            elif lufs_or_peak == "Peak Value":
                peak_label.grid(column=1, row=i, padx=5)
                result_peak.grid(column=2, row=i, padx=5)
            else:
                lufs_label.grid(column=1, row=i, padx=5)
                peak_label.grid(column=2, row=i, padx=5)
                result_lufs.grid(column=3, row=i, padx=5)
                result_peak.grid(column=4, row=i, padx=5)
            i += 1

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)


class ViewPlatforms(tk.Toplevel):
    """View all available platforms and standards.

    Will allow users to view every platform with max integrated loudness (LUFS) and max peak (dB)

    """
    def __init__(self, parent):
        """Initializes the View Platforms window

        Will display current directory of platforms by using the get_platform_names method and the
        standards of these platforms by using the get_platform_standard method.

        Args:
          self: The instance of the view platforms window
          parent: App object, window it came from

        Raises:
          Any errors raised should be put here

        """
        super().__init__(parent)
        # create basic window properties
        self.title("View Platforms")
        # change size according to the longest platform name
        max_name_length = parent.get_max_platform_name_length()
        size = str(max_name_length*6+480) + "x400"
        self.geometry(size)

        # define a scrollable frame
        container = ttk.Frame(self)
        container.pack(fill="both", expand=1)
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=scrollbar.set)

        # define our headers
        platform_label = ttk.Label(
            scrollable_frame,
            text="Platform Name",
            style="Heading.TLabel"
        )
        lufs_level_label = ttk.Label(
            scrollable_frame,
            text="Max Integrated Loudness (LUFS)",
            style="Heading.TLabel"
        )
        peak_level_label = ttk.Label(
            scrollable_frame,
            text="Max True Peak (dBFS)",
            style="Heading.TLabel"
        )

        # define the look of our headers and platform data
        style = ttk.Style()
        style.configure(
            "Heading.TLabel",
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "Data.TLabel",
            font=("Helvetica", 9)
        )

        # place our headers on the screen
        platform_label.grid(column=0, row=0, padx=5)
        lufs_level_label.grid(column=1, row=0, padx=5)
        peak_level_label.grid(column=2, row=0, padx=5)

        platform_names = parent.get_platform_names()
        # row variable
        i = 1
        for name in platform_names:
            name_label = ttk.Label(
                scrollable_frame,
                text=name,
                style="Data.TLabel"
            )
            values = parent.get_platform_standard(name)
            # make sure the value is not null before trying to format it
            if values[0] != "":
                lufs = "{:.1f}".format(values[0])
            else:
                lufs = ""
            if values[1] != "":
                peak = "{:.1f}".format(values[1])
            else:
                peak = ""

            # define our lufs and peak max values as labels to be placed on the screen
            lufs_label = ttk.Label(
                scrollable_frame,
                text=lufs,
                style="Data.TLabel"
            )
            peak_label = ttk.Label(
                scrollable_frame,
                text=peak,
                style="Data.TLabel"
            )

            # place the platform, lufs, and peak labels on the screen
            name_label.grid(column=0, row=i, padx=5)
            lufs_label.grid(column=1, row=i, padx=5)
            peak_label.grid(column=2, row=i, padx=5)
            # iterate the row for next platform
            i += 1

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # make the window modal
        self.focus_set()
        self.grab_set()
        self.transient(parent)
        self.wait_window(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
