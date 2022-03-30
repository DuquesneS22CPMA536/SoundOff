from tkinter import filedialog as fd
import sqlite3
import soundfile as sf
import pyloudnorm as pyln
import add_new_window
import modify_standards_window
import view_standards_window
from view_standards_window import *
import report_results_window
import no_standards_file_window
import numpy as np
import scipy
import math
import resampy
import statistics


class App(tk.Tk):
    """A SoundOff window.

    Will hold a primary window with functions to select a wav file, test the wav file's peak value against
    a standard's peak value, and test the wav file's LUF value against a standard's LUF value.

    Attributes:
        file_path: The current audio file path to be tested. Can change frequently. String object.
        platforms: a dictionary of current platforms with lufs and peak values
        make_changes: a boolean value used by the warning window to hold whether the user wishes to make a change
    """

    def __init__(self, master=None):
        """Initializes the main window application

        Will hold buttons for the main functions and store platform information by accessing the standards.db file

        Args:
          self: The main window
          master: no master, this is the first instance of a window

        Raises:
          Any errors raised should be put here

        """
        super().__init__(master)
        # create basic window properties
        self.title("SoundOff")
        self.geometry("1155x775")
        self.configure(bg="#2d2933")

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
            command=lambda: add_new_window.AddNew(self),
            style="Add.TButton"
        )
        self.modify_button = ttk.Button(
            self,
            text="Modify/Delete existing platform standards",
            command=lambda: modify_standards_window.Modify(self),
            style="Add.TButton"
        )
        self.view_button = ttk.Button(
            self,
            text="View existing platform standards",
            command=lambda: view_standards_window.ViewPlatforms(self),
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
        self.open_audio_file.grid(column=0, row=2, columnspan=3, padx=450, ipadx=45, ipady=22, pady=20)
        self.welcome_label.grid(column=0, row=0, pady=60, columnspan=3)
        self.blank_label2.grid(column=1, row=3, pady=200)
        self.add_button.grid(column=0, row=10, pady=20, padx=10)
        self.modify_button.grid(column=1, row=10, pady=20)
        self.view_button.grid(column=2, row=10, pady=20)

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
            no_standards_file_window.NoStandardsWindow(self)

    def change_file_path(self, new_file_path):
        """Changes the file path.

        Makes change to the file path, which is an attribute of this instance of App class. This will change the
        attribute used by the view report window.

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

        Returns the standard names in lower case in a list. To be used to check whether a name is being stored,
        not to display the names.

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

        Will change the platforms dictionary and the standards.db database based on changes passed by user

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
        if value_type == "LUFS Value":
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

        Uses the get_platform_names method to get a list of all platform names and then find the maximum length of
        these. Will be used to configure window sizes that use platform names.

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

        Will be used by the warning window if a user selects yes after a warning. Will also be used by the window
        that prompted the warning after the changed has been made to reset the value.

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

        Will also be used by the window that prompted a warning to see if the user wishes to do the action that
        caused a warning.

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
            report_results_window.Report(self, self.get_file_path())

    def open_wav_file(self):
        """Opens the wav file and fetches its needed information.

        Opens the selected wav file and fetches its sample rate, data itself, length of data, and number of channels.

        Args:
            self: An App Object.

        Returns:
            A tuple containing the selected wav file's sample rate, data, length of data, and number of channels.

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
            wav_info: a tuple of the selected wav file's sample rate, data, length of data, number of channels

        Returns:
            The integrated loudness of the audio file in LUFS

        Raises:
            Any errors raised should be put here

        """

        meter = pyln.Meter(wav_info[1])  # create meter; wav_info[1] is the rate
        lufs = meter.integrated_loudness(wav_info[0])  # get lufs value; wav_info[0] is the data
        return lufs

    def get_peak(self, wav_info):
        """Returns the true peak in dB of an audio file.

        Uses some method to find the peak of an audio file found at a file path passed.

        Args:
            self: Instance of main window
            wav_info: a tuple of the selected wav file's sample rate, data, length of data, number of channels

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
