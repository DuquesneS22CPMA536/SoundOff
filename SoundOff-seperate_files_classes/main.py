"""
This module will create the window for the application.
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import sqlite3
import subprocess
import soundfile as sf
import moviepy.editor as mp
import add_new_window
import modify_standards_window
import error_window
from view_standards_window import ViewPlatforms
import report_results_window
import no_standards_file_window


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
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        new_width = int(width/1.1)
        new_height = int(height/1.28)
        size = str(new_width) + "x" + str(new_height)
        self.geometry(size)
        self.configure(bg="#2d2933")
        self.iconbitmap(True, "SoundOff.ico")

        # initialize path of the file being passed in
        self.file_path = ""

        # a dictionary to store platform standards, initialized to query from standards database
        self.platforms = {}

        # True/False value to store whether to make changes after warning message
        self.make_changes = False

        # define our labels and widgets to be placed on the screen
        self.open_file = ttk.Button(
            self,
            text="Select a file",
            command=self.select_file,
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
        self.open_file.grid(column=1, row=2, ipadx=30, ipady=18, pady=20, sticky="nsew")
        self.welcome_label.grid(column=1, row=0, pady=60, sticky="nsew")
        self.blank_label2.grid(column=1, row=3, pady=height/5.9)
        self.add_button.grid(column=0, row=10, pady=20, padx=width/11)
        self.modify_button.grid(column=1, row=10, pady=20)
        self.view_button.grid(column=2, row=10, pady=20, padx=width/12)

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
        try:
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
        except sqlite3.OperationalError:
            # create an error window which will destroy the main window
            no_standards_file_window.NoStandardsWindow(self)

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
            name_list.append(key.lower().split())
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
            try:
                connection = sqlite3.connect('standards.db')
                cursor = connection.cursor()
                update_query = """UPDATE Standards
                                SET LUF_Value = ?
                                WHERE Standard_Name = ?"""
                cursor.execute(update_query, (new_value_float, name))
                connection.commit()
                connection.close()
            except sqlite3.OperationalError:
                # create an error window which will destroy the main window
                no_standards_file_window.NoStandardsWindow(self)
        else:
            curr_value = list(self.get_platform_standard(name))
            curr_value[1] = new_value_float
            self.platforms[name] = tuple(curr_value)
            # now update database
            try:
                connection = sqlite3.connect('standards.db')
                cursor = connection.cursor()
                update_query = """UPDATE Standards
                                SET Peak_Value = ?
                                WHERE Standard_Name = ?"""
                cursor.execute(update_query, (new_value_float, name))
                connection.commit()
                connection.close()
            except sqlite3.OperationalError:
                # create an error window which will destroy the main window
                no_standards_file_window.NoStandardsWindow(self)

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
        try:
            connection = sqlite3.connect('standards.db')
            cursor = connection.cursor()
            delete_query = """DELETE FROM Standards
                                WHERE Standard_Name = ?"""
            cursor.execute(delete_query, (name,))
            connection.commit()
            connection.close()
        except sqlite3.OperationalError:
            # create an error window which will destroy the main window
            no_standards_file_window.NoStandardsWindow(self)

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

    def select_file(self):
        """ Prompts user for a file path (WAV, FLAC, MP4) and computes the number of channels
        and sample rate.

        Calls get_lufs_peak to return the lufs and peak values of the file. Calls the report
        results window to print the results on the screen and prompt user for a report type.

        Args:
          self: Instance of main window

        Raises:
          Any errors raised should be put here

        """
        # file types to accept
        filetypes = (
            ("WAV file", "*.wav"),
            ("FLAC file", "*.flac"),
            ("MP4 file", "*.mp4")
        )
        filename = fd.askopenfilename(
            title="Select a file",
            initialdir='/',
            filetypes=filetypes
        )

        self.change_file_path(filename)
        file_type = self.get_file_path().split('.')  # split file path on '.'
        file_type = file_type[-1]  # take the last entry in the list from split as file extension

        # if the file is an MP4 file then open using moviepy and extract the audio
        if file_type.upper() == 'MP4':
            clip = mp.VideoFileClip(self.get_file_path())
            audio_file = clip.audio
            data = audio_file.to_soundarray(None, 44100)
            rate = 44100
        # else open as an audio (wav/flac) file
        else:
            data, rate = sf.read(self.get_file_path())

        if len(data.shape) > 1:
            n_channels = data.shape[1]
        else:
            n_channels = 1
        lufs_value, peak_value = get_lufs_peak(self, filename)

        if self.get_file_path() != "":
            report_results_window.Report(self,
                                         self.get_file_path(),
                                         rate,
                                         n_channels,
                                         lufs_value,
                                         peak_value)


def get_lufs_peak(parent_window, file_name):
    """Returns the lufs and peak values for a file.

    Uses ffmpeg to calculate the values.

    Args:
        parent_window: Instance of main window
        file_name: The file path of the file to find values for.

    Raises:
        Any errors raised should be put here

    """
    # initialize lufs and peak values to default -99.9
    # if there is an error in the calculation, this value will show up
    lufs_value = -99.9
    peak_value = -99.9

    # create query that would normally be run in the command prompt
    output_query = ['ffmpeg', '-i', file_name, '-af', 'loudnorm=I=-16:print_format=summary',
                    '-f', 'null', '-']
    # run the query and receive the output
    output = subprocess.getoutput(output_query)

    # split the output on new lines
    list_split = output.split('\n')

    # loop through the lines of list_split starting at the end and working backwards
    for i in range(len(list_split) - 1, 0, -1):
        # if the line starts with 'Input True Peak:'
        if list_split[i][0:16] == 'Input True Peak:':
            # then the lufs line is the line preceding current line
            lufs_string = list_split[i - 1]
            # and the peak line is the current line
            peak_string = list_split[i]

            # split the lufs string on spaces and take the 3rd element
            lufs_value = (float(lufs_string.split()[2]))
            # split the peak string on spaces and take the 4th element
            peak_value = (float(peak_string.split()[3]))
            # we don't need to finish the loop since we found what we were looking for
            break

    if lufs_value == -99.9 and peak_value == -99.9:
        error_window.AddError(
            parent_window,
            "There was an error while calculating the LUFS and Peak value")

    return lufs_value, peak_value


if __name__ == "__main__":
    app = App()
    app.mainloop()
