from tkinter.ttk import *
from tkinter import filedialog as fd
import random
from tkinter.ttk import OptionMenu
import sqlite3
import soundfile as sf
import pyloudnorm as pyln
import add_new_window
import modify_standards_window
import view_standards_window
from view_standards_window import *
import view_results_window
import report_results_window
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
        filename: The current wav file path to be tested. Can change frequently. String object.
        standards: a dictionary of current standards, needs to change to database
      """

    def __init__(self, master=None):
        """Initializes the application idk add more

        IDK more information about what the application
        does?

        Args:
          self: An App Object. App instance.
          master: some info here

        Raises:
          Any errors raised should be put here

        """
        super().__init__(master)
        # create basic window properties
        self.title("SoundOff")
        self.geometry("1228x775")
        self.configure(bg="#1e1529")
        self.iconbitmap('SoundOff.ico')

        # initialize the filename (path of the wave file) to be blank
        self.filename = ""

        # a dictionary to store standards, initialized to query from standards database
        self.standards = {}

        # True/False value to store whether to make changes after warning message
        self.make_changes = False

        # connect to standards database (assumes it's already made)
        # make sure its in the same folder as py file
        connection = sqlite3.connect('standards.db')

        cursor = connection.cursor()
        standard_info = cursor.execute('''SELECT * FROM Standards''')
        for standard in standard_info:
            # key for dictionary = standard name
            # value for dictionary = (lufs,peak)
            self.standards[standard[0]] = (standard[1], standard[2])

        # button to ask for wav file
        self.open_audio_file = ttk.Button(
            self,
            text="Select a .wav file",
            command=self.select_audio_file,
            style="File.TButton"
        )

        # place select file button onto window
        self.open_audio_file.grid(column=1, row=2, sticky="ns", pady=20, padx=323, ipadx=45, ipady=22)

        # create greeting label
        self.welcome_label = ttk.Label(
            self,
            text="Welcome to SoundOff!",
            style="Greeting.TLabel"
        )

        # I was having trouble without blank labels, hope to eventually get rid of these
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

        # place all of our labels onto the screen
        self.welcome_label.grid(column=1, row=0, pady=60)

        self.blank_label2.grid(column=1, row=3, pady=200)

        # create buttons dealing with standards
        self.add_button = ttk.Button(
            self,
            text="Add a new standard",
            command=lambda: add_new_window.AddNew(self).wait_window(),
            style="Add.TButton"
        )
        self.modify_button = ttk.Button(
            self,
            text="Modify/Delete existing standards",
            command=lambda: modify_standards_window.Modify(self).wait_window(),
            style="Add.TButton"
        )
        self.view_button = ttk.Button(
            self,
            text="View existing standards",
            command=lambda: view_standards_window.ViewStandards(self).wait_window(),
            style="Add.TButton"
        )

        # place buttons dealing with standards
        self.add_button.grid(column=0, row=10, pady=20, padx=10)
        self.modify_button.grid(column=1, row=10, pady=20)
        self.view_button.grid(column=2, row=10, pady=20)

        # Create a style for how our widgets will look :)
        # https://docs.python.org/3/library/tkinter.ttk.html
        style = ttk.Style()

        style.configure(
            "Greeting.TLabel",
            foreground="white",
            background="#1e1529",
            font=('Helvetica', 35)
        )
        style.configure(
            "File.TButton",
            foreground="#1e1529",
            background="white",
            border=0,
            font=('Helvetica', 18)
        )
        style.configure(
            "Add.TButton",
            foreground="#1e1529",
            background="white",
            border=0,
            font=('Helvetica', 10)
        )
        style.configure(
            "Blank.TLabel",
            foreground="#1e1529",
            background="#1e1529",
            font=('Helvetica', 8)
        )

    # return/change filename
    def change_file_name(self, new_file_name):
        """Changes the file name.

        Makes change to the file name, which is an attribute of this instance of App class.

        Args:
          self: An App Object. App instance.
          new_file_name: The new file name (or path) of the wav file to be tested. A string object

        Raises:
          Any errors raised should be put here

        """
        self.filename = new_file_name

    def get_filename(self):
        """ Gives the current file name being stored by the app

        Returns the filename attribute being stored.

        Args:
            self: An App Object. App instance.

        Returns:
            filename: the file path of the wav file selected by the user

        Raises:
            Any errors raised should be put here

        """
        return self.filename

    # add in try catch block
    def add_to_standard_dict(self, name, value):
        """ Add a new standard

        Will add the new standard along with luf values and peak values to the standard dictionary
        and the standards.db database

         Args:
            self: An App Object. App instance.
            name: The name of the standard. A string object.
            value: The LUFS and Peak value. A tuple in the form of (luf,peak).

        Raises:
            Any errors raised should be put here
        """
        luf = value[0]
        luf_int = int(luf)
        peak = value[1]
        peak_int = int(peak)
        self.standards[name] = (luf_int, peak_int)

        # now update database
        connection = sqlite3.connect('standards.db')
        cursor = connection.cursor()

        insert_query = """INSERT INTO Standards
                        (Standard_Name, LUF_Value, Peak_Value)
                        VALUES
                        (?,?,?)"""

        cursor.execute(insert_query, (name, luf_int, peak_int))
        connection.commit()
        connection.close()

    def get_standard_names_dict(self):
        """ Gives the standard names stored within the standard dictionary.

        Returns the standard names currently being stored as list.

        Args:
            self: An App Object. App instance.

        Returns:
            name_list: A list of all of the names currently being stored.

        Raises:
            Any errors raised should be put here
        """
        name_list = []
        for key in self.standards:
            name_list.append(key)
        return name_list

    def get_standard_names_lower(self):
        """ Gives the standard names stored within the standard dictionary.

        Returns the standard names currently being stored as list.

        Args:
            self: An App Object. App instance.

        Returns:
            name_list: A list of all of the names currently being stored.

        Raises:
            Any errors raised should be put here
        """
        name_list = []
        for key in self.standards:
            name_list.append(key.lower())
        return name_list

    def get_standard_value(self, name):
        """ Gives the current file name being stored by the app

        Returns the filename attribute being stored.

        Args:
            self: An App Object. App instance.
            name: the name of the standard we will return lufs and peak values for

        Returns:
            filename: the file path of the wav file selected by the user

        Raises:
            Any errors raised should be put here

        """
        return self.standards.get(name)

    def set_standard_value(self, name, value_type, new_value):
        new_value_int = int(new_value)
        if value_type == "LUFS Value":
            curr_value = list(self.get_standard_value(name))
            curr_value[0] = new_value_int
            self.standards[name] = tuple(curr_value)
            # now update database
            connection = sqlite3.connect('standards.db')
            cursor = connection.cursor()
            update_query = """UPDATE Standards
                            SET LUF_Value = ?
                            WHERE Standard_Name = ?"""
            cursor.execute(update_query, (new_value_int, name))
            connection.commit()
            connection.close()
        else:
            curr_value = list(self.get_standard_value(name))
            curr_value[1] = new_value_int
            self.standards[name] = tuple(curr_value)
            # now update database
            connection = sqlite3.connect('standards.db')
            cursor = connection.cursor()
            update_query = """UPDATE Standards
                            SET Peak_Value = ?
                            WHERE Standard_Name = ?"""
            cursor.execute(update_query, (new_value_int, name))
            connection.commit()
            connection.close()

    def remove_standard(self, name):
        self.standards.pop(name)
        connection = sqlite3.connect('standards.db')
        cursor = connection.cursor()
        delete_query = """DELETE FROM Standards
                            WHERE Standard_Name = ?"""
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()

    def store_changes(self, value):
        if value:
            self.make_changes = True

    def get_change(self):
        return self.make_changes

    def select_audio_file(self):
        """Prompts user for wav file path.

        Uses askopenfilename to select a wav file to be tested.

        Args:
          self: An App Object. App instance.

        Raises:
          Any errors raised should be put here

        """
        # file types to accept
        filetypes = (
            ("WAV file", "*.wav"),
            ("All files", "*.*")
        )
        filename = fd.askopenfilename(
            title="Select a .wav file",
            initialdir='/',
            filetypes=filetypes
        )

        self.change_file_name(filename)

        # define style of the filename to be on screen
        style = ttk.Style()
        style.configure(
            "filename.TLabel",
            foreground="white",
            background="#333147",
            font=('Helvetica', 8)
        )

        if self.get_filename() != "":
            report_results_window.Report(self, self.get_filename())

    def open_wav_file(self):
        '''Opens the wav file and fetches its needed information.
        
        Opens the selected wav file and fetches its sample rate, data itself, length of data, and number of channels.
        
        Args:
            self: An App Object.
        
        Returns:
            A tuple containing the selected wav file's sample rate, data, length of data, and number of channels.
        
        Raises:
            Add possible errors here.
        
        '''
        data, rate = sf.read(self.get_filename())
        length_file = len(data)
        if len(data.shape) > 1:
            nchannels = data.shape[1]
        else:
            nchannels = 1
        wav_info = (data, rate, length_file, nchannels)
        return wav_info

    def get_luf(self, wav_info):
        meter = pyln.Meter(wav_info[1]) #create meter; wav_info[1] is the rate
        lufs = meter.integrated_loudness(wav_info[0]) #get lufs value; wav_info[0] is the data
        return lufs

    def get_peak(self, wav_info):
        resampling_factor = 4 #use a resampling factor of 4
        
        #calculate number of samples in resampled file
        samples = wav_info[2] * resampling_factor # wav_info[2] is the length of the data 

        #resample using FFT
        newAudio = scipy.signal.resample(wav_info[0], samples)
        current_peak1 = np.max(np.abs(newAudio)) #find peak value
        current_peak1 = math.log(current_peak1,10)*20 #convert to decibels

        #resample using resampy
        newAudio = resampy.resample(wav_info[0], wav_info[2], samples, axis=-1)
        current_peak2 = np.max(np.abs(newAudio)) #find peak value
        current_peak2 = math.log(current_peak2,10)*20 #convert to decibels

        #resample using polynomial
        newAudio = scipy.signal.resample_poly(wav_info[0], resampling_factor,1)
        current_peak3 = np.max(np.abs(newAudio)) #find peak value
        current_peak3 = math.log(current_peak3,10)*20 #convert to decibels

        #get and return median of the three techniques
        peak = statistics.median([current_peak1,current_peak2,current_peak3])
        return(peak)


if __name__ == "__main__":
    app = App()
    app.mainloop()
