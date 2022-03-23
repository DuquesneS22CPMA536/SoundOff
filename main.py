import tkinter as tk
from tkinter import *
from tkinter import ttk, OptionMenu
from tkinter.ttk import *
from tkinter import filedialog as fd
import random
from tkinter.ttk import OptionMenu
import sqlite3
import soundfile as sf
import pyloudnorm as pyln


class App(tk.Tk):
    """A SoundOff window.

    Will hold a primary window with functions to select a wav file, test the wav file's peak value against a standard's peak value, and test the wav file's LUF value against a standard's LUF value.

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

        #a dictionary to store standards, initialized to query from standards database
        self.standards = {}


        connection = sqlite3.connect('standards.db')

        cursor = connection.cursor()
        standard_info = cursor.execute('''SELECT * FROM Standards''')
        for standard in standard_info:
            self.standards[standard[0]]=(standard[1],standard[2])


        # button to ask for wav file
        self.open_audio_file = ttk.Button(
            self,
            text="Select a .wav file",
            command=self.select_audio_file,
            style="File.TButton"
        )


        # place select file button onto window
        self.open_audio_file.grid(column=1, row=2, sticky="ns", pady=20,padx=323, ipadx=45, ipady = 22)

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
            command=self.add_standard,
            style="Add.TButton"
        )
        self.modify_button = ttk.Button(
            self,
            text="Modify/Delete existing standards",
            command=self.modify_standards,
            style="Add.TButton"
        )
        self.view_button = ttk.Button(
            self,
            text="View existing standards",
            command=self.view_standards,
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

        #now update database
        connection = sqlite3.connect('standards.db')
        cursor = connection.cursor()

        insert_query = """INSERT INTO Standards
                        (Standard_Name, LUF_Value, Peak_Value)
                        VALUES
                        (?,?,?)"""

        cursor.execute(insert_query,(name, luf_int, peak_int))
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
            cursor.execute(update_query,(new_value_int,name))
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
            cursor.execute(update_query,(new_value_int,name))
            connection.commit()
            connection.close()

    def remove_standard(self,name):
        self.standards.pop(name)
        connection = sqlite3.connect('standards.db')
        cursor = connection.cursor()
        delete_query = """DELETE FROM Standards
                            WHERE Standard_Name = ?"""
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()


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
            self.report_results(self.get_filename())

    def report_results(self, file_name):
        # change to actual peak and luf
        peak = self.get_peak(file_name)
        luf = self.get_luf(file_name)

        top = Toplevel()
        top.title("Select Report")
        top.geometry("490x200")

        if len(file_name)>50:
            new_file_name = file_name[:50]+"..."
        else:
            new_file_name = file_name

        selected_file_label = Label(
            top,
            text="Selected file path: "+new_file_name,
            font=("Helvetica",10,"bold")
        )
        selected_file_label.grid(column=0, row=0, columnspan=4)

        directions_label = Label(
            top,
            text="Please select the type of report you wish you view",
            font=("Helvetica", 10,"bold")
        )
        directions_label.grid(column=0, row=4, columnspan=4, sticky="w")

        standard_names = self.get_standard_names_dict()
        standard_names.append("All Available Standards")
        standard_names.insert(0, standard_names[0])
        selected_name = StringVar()
        selected_name.set(standard_names[0])
        selected_LUF_Peak = StringVar()
        selected_LUF_Peak.set("LUF Value")

        drop_standards = OptionMenu(
            top,
            selected_name,
            *standard_names,
        )

        drop_LUF_Peak = OptionMenu(
            top,
            selected_LUF_Peak,
            "LUFS Value",
            "LUFS Value",
            "Peak Value",
            "LUFS and Peak"
        )
        drop_standards.config(width=25)
        drop_standards["menu"].config(bg="#333147")
        drop_standards["menu"].config(fg="white")
        drop_LUF_Peak.config(width=20)
        drop_LUF_Peak["menu"].config(bg="#333147")
        drop_LUF_Peak["menu"].config(fg="white")
        drop_standards.grid(column=0, row=5)
        drop_LUF_Peak.grid(column=1, row=5)
        luf_value_label = Label(
            top,
            text="Your LUF = " + str(luf)
        )
        peak_value_label = Label(
            top,
            text="Your Peak =" + str(peak)
        )
        luf_value_label.grid(column=0, row=1, sticky="w")
        peak_value_label.grid(column=0, row=2, sticky="w")

        blank_label = Label(
            top,
            text=""
        )
        blank_label.grid(column=0, row=3, pady=10)

        enter_button = ttk.Button(
            top,
            text="Enter",
            command=lambda: self.view_results(
                selected_name.get(),
                selected_LUF_Peak.get(),
                peak,
                luf,
                top
            )
        )
        enter_button.grid(column=0, row=6, sticky="w")

    def view_results(self, name_selected, luf_or_peak, peak, luf, window):
        window.destroy()
        top = Toplevel()
        top.title("View Report")
        top.geometry("630x300")

        container = ttk.Frame(top)
        container.pack(fill=BOTH, expand=1)
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

        style = ttk.Style()

        style.configure(
            "Input.TLabel",
            foreground="white",
            background="#333147",
            font=('Helvetica', 10)
        )

        style.configure(
            "Column.TLabel",
            font=("Helvetica", 9, "bold")
        )

        style.configure(
            "Result.TLabel",
            font=("Helvetica", 8)
        )

        style.configure(
            "Pass.TLabel",
            foreground="green",
            font=("Helvetica", 8, "bold")
        )

        style.configure(
            "Fail.TLabel",
            foreground="red",
            font=("Helvetica", 8, "bold")
        )

        standard_label = ttk.Label(
            scrollable_frame,
            text="Standard Name",
            style="Column.TLabel") .grid(column=0, row=1, padx=5)

        standard_names = self.get_standard_names_dict()

        if luf_or_peak == "LUFS Value":
            LUF_label = ttk.Label(scrollable_frame, text="Max Integrated (LUFS)", style="Column.TLabel").grid(column=1,
                                                                                                              row=1,
                                                                                                              padx=5)
            LUF_Result_label = ttk.Label(scrollable_frame, text="LUFS Result", style="Column.TLabel").grid(column=2,
                                                                                                          row=1)
            input_LUF_label = ttk.Label(scrollable_frame, text="Input LUF from file: " + str(luf),
                                        style="Input.TLabel").grid(column=0, row=0, columnspan=2)

        elif luf_or_peak == "Peak Value":
            Peak_label = ttk.Label(scrollable_frame, text="Max True Peak (dB)", style="Column.TLabel").grid(column=1,
                                                                                                            row=1,
                                                                                                            padx=5)
            Peak_Result_label = ttk.Label(scrollable_frame, text="Peak Result", style="Column.TLabel").grid(column=2,
                                                                                                            row=1)
            input_Peak_label = ttk.Label(scrollable_frame, text="Input Peak from file: " + str(peak),
                                         style="Input.TLabel").grid(column=0, row=0, columnspan=2)

        else:
            LUF_label = ttk.Label(scrollable_frame, text="Max Integrated (LUFS)", style="Column.TLabel").grid(column=1,
                                                                                                              row=1,
                                                                                                              padx=5)
            Peak_label = ttk.Label(scrollable_frame, text="Max True Peak (dB)", style="Column.TLabel").grid(column=2,
                                                                                                            row=1,
                                                                                                            padx=5)
            LUF_Result_label = ttk.Label(scrollable_frame, text="LUFS Result", style="Column.TLabel").grid(column=3,
                                                                                                          row=1, padx=5)
            Peak_Result_label = ttk.Label(scrollable_frame, text="Peak Result", style="Column.TLabel").grid(column=4,
                                                                                                            row=1,
                                                                                                            padx=5)
            input_LUF_label = ttk.Label(scrollable_frame, text="Input LUF from file: " + str(luf),
                                        style="Input.TLabel").grid(column=0, row=0, columnspan=2,padx=10)
            input_Peak_label = ttk.Label(scrollable_frame, text="Input Peak from file: " + str(peak),
                                         style="Input.TLabel").grid(column=2, row=0, columnspan=2)

            # we need a report of everything
        if name_selected == "All Available Standards":
            if luf_or_peak == "LUFS Value":
                i = 2
                for name in standard_names:
                    name_label = ttk.Label(
                        scrollable_frame,
                        text=name,
                        style="Result.TLabel"
                    )

                    values = self.get_standard_value(name)
                    luf_label = ttk.Label(
                        scrollable_frame,
                        text=values[0],
                        style="Result.TLabel"
                    )

                    name_label.grid(column=0, row=i, padx=5)
                    luf_label.grid(column=1, row=i, padx=5)

                    if luf <= values[0]:
                        result_luf = ttk.Label(
                            scrollable_frame,
                            text="Pass",
                            style="Pass.TLabel"
                        )
                    else:
                        result_luf = ttk.Label(
                            scrollable_frame,
                            text="Fail",
                            style="Fail.TLabel"
                        )
                    result_luf.grid(column=2, row=i, padx=5)
                    i += 1


            elif luf_or_peak == "Peak Value":
                i = 2
                for name in standard_names:
                    name_label = ttk.Label(
                        scrollable_frame,
                        text=name,
                        style="Result.TLabel"
                    )

                    values = self.get_standard_value(name)
                    peak_label = ttk.Label(
                        scrollable_frame,
                        text=values[1],
                        style="Result.TLabel"
                    )

                    name_label.grid(column=0, row=i, padx=5)
                    peak_label.grid(column=1, row=i, padx=5)

                    if peak <= values[1]:
                        result_peak = ttk.Label(
                            scrollable_frame,
                            text="Pass",
                            style="Pass.TLabel"
                        )
                    else:
                        result_peak = ttk.Label(
                            scrollable_frame,
                            text="Fail",
                            style="Fail.TLabel"
                        )
                    result_peak.grid(column=2, row=i, padx=5)
                    i += 1
            else:
                i = 2
                for name in standard_names:
                    name_label = ttk.Label(
                        scrollable_frame,
                        text=name,
                        style="Result.TLabel"
                    )

                    values = self.get_standard_value(name)
                    luf_label = ttk.Label(
                        scrollable_frame,
                        text=values[0],
                        style="Result.TLabel"
                    )
                    peak_label = ttk.Label(
                        scrollable_frame,
                        text=values[1],
                        style="Result.TLabel"
                    )

                    name_label.grid(column=0, row=i, padx=5)
                    luf_label.grid(column=1,row=i,padx=5)
                    peak_label.grid(column=2, row=i, padx=5)

                    if luf <= values[0]:
                        result_luf = ttk.Label(
                            scrollable_frame,
                            text="Pass",
                            style="Pass.TLabel"
                        )
                    else:
                        result_luf = ttk.Label(
                            scrollable_frame,
                            text="Fail",
                            style="Fail.TLabel"
                        )
                    result_luf.grid(column=3, row=i, padx=5)
                    if peak <= values[1]:
                        result_peak = ttk.Label(
                            scrollable_frame,
                            text="Pass",
                            style="Pass.TLabel"
                        )
                    else:
                        result_peak = ttk.Label(
                            scrollable_frame,
                            text="Fail",
                            style="Fail.TLabel"
                        )
                    result_peak.grid(column=4, row=i, padx=5)
                    i += 1

        # result of just 1 standard
        else:
            name_label = ttk.Label(
                scrollable_frame,
                text=name_selected,
                style="Result.TLabel"
            )
            name_label.grid(column=0, row=2, padx=5)
            values = self.get_standard_value(name_selected)
            if luf_or_peak == "LUFS Value":
                luf_value_label = ttk.Label(
                    scrollable_frame,
                    text=values[0],
                    style="Result.TLabel"
                )
                luf_value_label.grid(column=1, row=2, padx=5)
                if luf <= values[0]:
                    result_luf = ttk.Label(
                        scrollable_frame,
                        text="Pass",
                        style="Pass.TLabel"
                    )
                else:
                    result_luf = ttk.Label(
                        scrollable_frame,
                        text="Fail",
                        style="Fail.TLabel"
                    )

                result_luf.grid(column=2, row=2, padx=5)
            elif luf_or_peak == "Peak Value":
                peak_value_label = ttk.Label(
                    scrollable_frame,
                    text=values[1],
                    style="Result.TLabel"
                )
                peak_value_label.grid(column=1, row=2, padx=5)
                if peak <= values[1]:
                    result_peak = ttk.Label(
                        scrollable_frame,
                        text="Pass",
                        style="Pass.TLabel"
                    )
                else:
                    result_peak = ttk.Label(
                        scrollable_frame,
                        text="Fail",
                        style="Fail.TLabel"
                    )
                result_peak.grid(column=2, row=2, padx=5)

            else:
                luf_value_label = ttk.Label(
                    scrollable_frame,
                    text=values[0],
                    style="Result.TLabel"
                )
                luf_value_label.grid(column=1, row=2, padx=5)
                luf_value_label = ttk.Label(
                    scrollable_frame,
                    text=values[1],
                    style="Result.TLabel"
                )
                luf_value_label.grid(column=2, row=2, padx=5)
                if luf <= values[0]:
                    result_luf = ttk.Label(
                        scrollable_frame,
                        text="Pass",
                        style="Pass.TLabel"
                    )
                else:
                    result_luf = ttk.Label(
                        scrollable_frame,
                        text="Fail",
                        style="Fail.TLabel"
                    )
                if peak <= values[1]:
                    result_peak = ttk.Label(
                        scrollable_frame,
                        text="Pass",
                        style="Pass.TLabel"
                    )
                else:
                    result_peak = ttk.Label(
                        scrollable_frame,
                        text="Fail",
                        style="Fail.TLabel"
                    )
                result_luf.grid(column=3, row=2, padx=5)
                result_peak.grid(column=4, row=2, padx=5)

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    #######################################################
    # from this point onward it all has to do with adding,
    # modifying, or viewing standards
    #######################################################

    # Create a button to ask if the user wants to modify
    # the current standards (do nothing now)

    def add_standard(self):
        top = Toplevel()
        top.title("Add Standard")
        top.geometry("408x75")

        style = Style()

        style.configure(
            "Header.TLabel",
            font=("Helvetica", 10, "bold")
        )
        style.configure(
            "Enter.TButton",
            font=('Helvetica', 10)
        )

        standard_label = ttk.Label(
            top,
            text = "Standard Name",
            style = "Header.TLabel"
        )
        luf_label = ttk.Label(
            top,
            text = "LUFS Value",
            style="Header.TLabel"
        )
        peak_label = ttk.Label(
            top,
            text = "Peak Value",
            style="Header.TLabel"
        )
        enter_button = ttk.Button(
            top,
            text="Enter",
            style="Enter.TButton",
            command=lambda: self.add_new_standard(
                standard_value_entry_Tf.get(),
                LUF_value_entry_Tf.get(),
                Peak_value_entry_Tf.get(),
                top
            )

        )

        name1 = StringVar(top)
        name2 = StringVar(top)
        name3 = StringVar(top)
        standard_value_entry_Tf = ttk.Entry(
            top,
            textvariable=name1
        )
        LUF_value_entry_Tf = ttk.Entry(
            top,
            textvariable=name2
        )
        Peak_value_entry_Tf = ttk.Entry(
            top,
            textvariable=name3
        )

        # put all of our crap on the screen
        standard_label.grid(column=0, row=0)
        luf_label.grid(column=1, row=0)
        peak_label.grid(column=2, row=0)
        standard_value_entry_Tf.grid(column=0, row=1, padx=5)
        LUF_value_entry_Tf.grid(column=1, row=1, padx=5)
        Peak_value_entry_Tf.grid(column=2, row=1, padx = 5)
        enter_button.grid(column=1, row=2)

    def add_new_standard(self, standard_name, LUF_value, Peak_value, window):

        destroy = True
        if standard_name.lower() in self.get_standard_names_lower():

            self.error_window("Standard name already exists")

            destroy = False

        elif standard_name == "":

            self.error_window("Please enter a standard name")
            destroy = False

        if LUF_value != "":
            # make sure we have negative numbers
            if LUF_value[0] == '-':
                # we most likely have a valid input
                if not LUF_value[1:].isnumeric():

                    self.error_window("Enter a numeric LUFS value")
                    destroy = False
            else:

                self.error_window("Enter a negative LUFS value")
                destroy = False

        if Peak_value != "":
            if Peak_value[0] == '-':
                # we most likely have a valid input
                if not Peak_value[1:].isnumeric():

                    self.error_window("Enter a numeric peak value")
                    destroy = False
            else:

                self.error_window("Enter a negative peak value")
                destroy = False

        if destroy:
            self.add_to_standard_dict(
                standard_name,
                (LUF_value, Peak_value)
            )
            print(self.get_standard_names_dict())
            window.destroy()

    def error_window(self, error):
        top = Toplevel()
        top.title("ERROR")
        top.geometry("300x100")

        style = ttk.Style()

        style.configure(
            "ErrorMsg.TLabel",
            foreground="red",
            font=("Helvetica", 10)
        )

        style.configure(
            "Okay.TButton",
            background="white",
            font=("Helvetica",10,"bold")
        )

        error_msg = ttk.Label(
            top,
            text="Error: " + error,
            style="ErrorMsg.TLabel"
        )

        okay = ttk.Button(
            top,
            text="Okay",
            command=lambda: self.exit_window(top),
            style="Okay.TButton"
        )

        error_msg.pack()
        okay.pack()

    def exit_window(self, window):
        window.destroy()

    def modify_standards(self):
        top = Toplevel()
        top.title("Modify Standards")
        top.geometry("415x50")

        standard_names = self.get_standard_names_dict()
        standard_names.insert(0, standard_names[0])
        selected_name = StringVar()
        selected_name.set(standard_names[0])
        selected_LUF_Peak = StringVar()
        selected_LUF_Peak.set("LUFS Value")

        drop_standards = OptionMenu(
            top,
            selected_name,
            *standard_names)

        drop_LUF_Peak = OptionMenu(
            top,
            selected_LUF_Peak,
            "LUFS Value",
            "LUFS Value",
            "Peak Value",
            "Delete Standard"
        )
        drop_standards.config(width=25)
        #drop_standards.config(height=2)
        #drop_standards.config(bg="white")
        #drop_standards.config(fg="#6f67c2")
        drop_LUF_Peak.config(width=15)
        #drop_LUF_Peak.config(height=2)
        #drop_LUF_Peak.config(bg="white")
        #drop_LUF_Peak.config(fg="#6f67c2")
        drop_standards.grid(column=0, row=0)
        drop_LUF_Peak.grid(column=1, row=0)

        blank_value = StringVar(top)
        blank_value.set("")
        new_value_Tf = ttk.Entry(
            top,
            textvariable=blank_value,
            width=13,
        )

        new_value_Tf.grid(column=2, row=0)

        enter_button = ttk.Button(
            top,
            text="Enter",
            command=lambda: self.modify_existing_standards(
                selected_name.get(),
                selected_LUF_Peak.get(),
                new_value_Tf.get(),
                top
            )
        )
        enter_button.grid(column=0, row=1)

    def modify_existing_standards(
            self,
            name,
            value_type,
            value,
            window
    ):

        destroy = True
        if value_type == "Delete Standard":
            destroy = False
            self.remove_standard(name)
            window.destroy()

        elif value != "":
            if value[0] == '-':
                if not value[1:].isnumeric():
                    self.error_window("Error: please enter numeric value")
                    destroy = False
            else:
                self.error_window("Error: must be negative")
                destroy = False

        if destroy:
            self.set_standard_value(name, value_type, value)

            window.destroy()

    def view_standards(self):
        top = Toplevel()
        top.title("View Standards")
        top.geometry("400x400")

        container = ttk.Frame(top)
        container.pack(fill=BOTH, expand=1)
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

        style = Style()
        style.configure(
            "Heading.TLabel",
            font = ("Helvetica", 9, "bold")
        )
        style.configure(
            "Data.TLabel",
            font = ("Helvetica, 8")
        )

        standard_label = Label(scrollable_frame, text="Standard Name",style="Heading.TLabel").grid(column=0, row=0, padx=5)

        luf_level_label = Label(scrollable_frame, text="Max Integrated (LUFS)",style="Heading.TLabel").grid(column=1, row=0, padx=5)
        peak_level_label = Label(scrollable_frame, text="Max True Peak (dB)",style="Heading.TLabel").grid(column=2, row=0, padx=5)

        standard_names = self.get_standard_names_dict()
        # row variable
        i = 1
        for name in standard_names:
            name_label = Label(
                scrollable_frame,
                text=name,
                style="Data.TLabel"
            )
            values = self.get_standard_value(name)

            luf_label = Label(
                scrollable_frame,
                text=values[0],
                style="Data.TLabel"
            )
            peak_label = Label(
                scrollable_frame,
                text=values[1],
                style="Data.TLabel"
            )

            name_label.grid(column=0, row=i, padx=5)
            luf_label.grid(column=1, row=i, padx=5)
            peak_label.grid(column=2, row=i, padx=5)
            i += 1

        container.pack()
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def get_luf(self, file_path):
        data, rate = sf.read(file_path)

        meter = pyln.Meter(rate)
        lufs = meter.integrated_loudness(data)
        return lufs

    def get_peak(self, file_path):
        return random.randint(-3,1)


if __name__ == "__main__":
    app = App()
    app.mainloop()
