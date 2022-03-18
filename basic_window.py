import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog as fd


class App(tk.Tk):
  def __init__(self, master=None):
    super().__init__(master)
    self.title("SoundOff")
    self.geometry("625x365")
    self.configure(bg="#333147")
    self.filename=""

    #button to ask for wav file
    self.open_audio_file = ttk.Button(
      self,
      text= "Select a .wav file",
      command=self.select_audio_file,
      style="File.TButton"
        
    )

    self.open_audio_file.grid(column=1,row=2,sticky=(N,S),pady=20)
    
    
    
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
    self.welcome_label.grid(column=1,row=1,sticky=(N,W,E,S))
    self.blank_label.grid(column=0,row=1)
    self.blank_label.grid(column=0,row=2)
    self.blank_label.grid(column=0,row=0,pady=20)
    self.blank_label2.grid(column=1,row=3,pady=65)
    
    self.add_button = ttk.Button(
      self,
      text="Add a new standard",
      command = self.add_or_modify,
      style="Add.TButton"
    )
    self.modify_button = ttk.Button(
      self,
      text="Modify existing standards",
      command = self.add_or_modify,
      style="Add.TButton"
    )
    self.view_button = ttk.Button(
      self,
      text="View existing standards",
      command = self.add_or_modify,
      style="Add.TButton"
    )
    

    self.add_button.grid(column=0,row=10,pady=20,padx=10)
    self.modify_button.grid(column=1,row=10,pady=20)
    self.view_button.grid(column=2,row=10,pady=20)


    #Create a style for how our widgets will look :)
    #https://docs.python.org/3/library/tkinter.ttk.html
    style = ttk.Style()

    style.configure( 
      "Greeting.TLabel",
      foreground="white",
      background="#6f67c2",
      font=('Helvetica', 18)
    )
    style.configure( 
      "File.TButton",
      foreground="#6f67c2",
      background="white",
      border=0,
      font=('Helvetica', 10)
    )
    style.configure( 
      "Add.TButton",
      foreground="#6f67c2",
      background="white",
      border=0,
      font=('Helvetica', 10)
    )
    style.configure(
      "Blank.TLabel",
      foreground="#333147",
      background="#333147",
      font=('Helvetica', 8)
    )
    
  def change_file_name(self,filename):
    self.filename = filename
  def get_filename(self):
    return self.filename

  
  #command to ask for name of file
  def select_audio_file(self):
  
    filetypes=(
      ("WAV file","*.wav"),
      ("All files","*.*")
    )
    filename = fd.askopenfilename(
      title="Select a .wav file",
      initialdir='/',
      filetypes= filetypes
    )
    
    self.change_file_name(filename)
    style = ttk.Style()
    
    style.configure(
      "filename.TLabel",
      foreground="white",
      background="#333147",
      font=('Helvetica', 8)
    )
    
    self.filename_label = ttk.Label(
      self,
      text=self.get_filename(),
      width=16,
      style="filename.TLabel"
    )
    self.filename_label.grid(column=0,row=3,columnspan=3,sticky=(W,E))
    

  #Create a button to ask if the user wants to modify 
  #the current standards
  def add_or_modify(self):
    pass
  



if __name__ == "__main__":
    app = App()
    app.mainloop()