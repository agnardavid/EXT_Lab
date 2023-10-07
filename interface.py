'''Copyright Information'''
__author__ = "Agnar Davíð Halldórsson"
__copyright__ = "Copyright (C) 2023 Agnar Davíð Halldórsson"
__license__ = "Public Domain"
__version__ = "1.0"

import os
import tkinter as tk
from tkinter import ttk
from main_script import Main
from tkinter import filedialog
import threading
from PIL import Image, ImageTk

# fg="#009891", background="#002D2B"
# fg="#FFFFFF", background="#486ADC"

DEFAULT_TEXT_COLOR = "#002D2B"
DEFAULT_BACKGROUND_COLOR = "#486ADC"

class CustomIcon(tk.Canvas):
    def __init__(self, parent, size, bg_color, text_color, text):
        super().__init__(parent, width=size, height=size, highlightthickness=0, bg=bg_color, borderwidth=0)
        self.oval_outer = self.create_oval(1, 1, size-1, size-1, outline=text_color, width=20, fill=bg_color)
        self.oval_inner = self.create_oval(4, 4, size-4, size-4, outline=bg_color, width=6, fill=bg_color)
        self.text = self.create_text(size//2, size//2, text=text, fill=text_color, font=('Sans Serif', size//2, "bold"))
        self.hide()  # Initially hide the icon

    def show(self):
        self.grid()

    def hide(self):
        self.grid_remove()

class LoadingScreen(tk.Frame):
    
    def __init__(self, parent, switch_callback_state):
        super().__init__(parent)
        self.folderpath = ""
        self.format_extension = ""
        self.switch_callback_state = switch_callback_state

        tk.Label(self, text="Converting...", font=('Sans Serif', 11), fg=DEFAULT_TEXT_COLOR, background=DEFAULT_BACKGROUND_COLOR).pack(padx=10, pady=10)

        self.progressbar = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate')
        self.progressbar.pack(pady=10)
    
    def update_progress(self, progress):
        self.progressbar['value'] = progress
        self.progressbar.update()
        
    def configure(self, folderpath, format_extension):
        self.folderpath = folderpath
        self.format_extension = format_extension

    def start_task(self, folderpath, format_extension):
        self.folderpath = folderpath
        self.format_extension = format_extension

        # Create a separate thread to run the Main task
        threading.Thread(target=self.run_main).start()

    def run_main(self):
        # Define the progress callback function
        def progress_callback(progress):
            self.update_progress(progress)

        def progress_fail_or_complete(state):
            if state == "Complete":
                self.switch_callback_state(True)
            if state == "Fail":
                self.switch_callback_state(False)

        Main(self.folderpath, self.format_extension, progress_callback, progress_fail_or_complete)
        
        
    
class CompleteScreen(tk.Frame):
    
    def __init__(self, parent, switch_callback_interface):
        super().__init__(parent)
        tk.Label(self, text="Conversion Completed!", font=('Sans Serif', 20, "bold"), fg=DEFAULT_TEXT_COLOR, background=DEFAULT_BACKGROUND_COLOR).pack(padx=10, pady=10)
        tk.Button(self, text="Return", font=("Sans Serif", 16, "bold"), fg=DEFAULT_TEXT_COLOR, command=switch_callback_interface).pack(padx=20, pady=20)

class FailedScreen(tk.Frame):
    
    def __init__(self, parent, switch_callback_interface):
        super().__init__(parent)
        tk.Label(self, text="Conversion partially or completely failed", font=('Sans Serif', 20, "bold"), fg=DEFAULT_TEXT_COLOR, background=DEFAULT_BACKGROUND_COLOR).pack(padx=10, pady=10)
        tk.Button(self, text="Return", font=("Sans Serif", 16, "bold"), fg=DEFAULT_TEXT_COLOR, command=switch_callback_interface).pack(padx=20, pady=20)

        
class Interface(tk.Frame):
    
    def __init__(self, parent, switch_callback_loading) -> None:
        super().__init__(parent)
        self.switch_callback_loading = switch_callback_loading
        self.config(background=DEFAULT_BACKGROUND_COLOR)
        self.folder_image = Image.open("folder_icon.gif")
        self.folder_image = self.folder_image.resize((25, 25))  # Adjust the size as needed
        self.folder_image = ImageTk.PhotoImage(self.folder_image)
        self.setup()

        

    def setup(self):
        
        # introduction label
        self.introduction_text = tk.Label(self, text="Please enter the desired file format and folder.", font=('Sans Serif', 16, "bold"), fg=DEFAULT_TEXT_COLOR, background=DEFAULT_BACKGROUND_COLOR)
        self.introduction_text.grid(row=0, column=0, columnspan=2, padx=20, pady=30)
        
        # file format instruction label
        self.file_format_label = tk.Label(self, text="New File Format:", font=('Sans Serif', 12, "bold"), fg=DEFAULT_TEXT_COLOR, background=DEFAULT_BACKGROUND_COLOR)
        self.file_format_label.grid(row=1, column=0, sticky=tk.W)
        
        # # Format selection with a dropdown menu
        # self.file_formats = ["png", "jpg", "pdf", "txt", "docx"]  # Add your predefined formats here
        # self.file_format_var = tk.StringVar()
        # self.file_format = ttk.Combobox(self, textvariable=self.file_format_var, values=self.file_formats, font=('Sans Serif', 16), state="readonly")
        # self.file_format.grid(row=1, column=1, columnspan=2, pady=2, sticky=tk.W + tk.E)  # Use columnspan=2 to make it span across 2 columns
        # self.file_format.focus_set()
        # self.file_format.bind("<FocusIn>", self.on_file_format_focus)


        # Format selection
        self.file_format = tk.Entry(self, font=('Sans Serif', 16), fg=DEFAULT_TEXT_COLOR)
        self.file_format.grid(row=1, column=1, pady=2, sticky=tk.W+tk.E)
        self.file_format.focus_set()
        
                
        # Folder selection label
        self.current_folder_label = tk.Label(self, text="Current folder:", font=('Sans Serif', 12, "bold"), fg=DEFAULT_TEXT_COLOR, background=DEFAULT_BACKGROUND_COLOR)
        self.current_folder_label.grid(row=2, column=0, sticky=tk.W)
        
        
        # Folder selection
        self.current_folder = tk.Entry(self, font=('Sans Serif', 16), fg=DEFAULT_TEXT_COLOR)
        self.current_folder.grid(row=2, column=1, pady=2, sticky=tk.W+tk.E)

        self.folder_button = tk.Button(self, image=self.folder_image, fg=DEFAULT_TEXT_COLOR, command=self.browse_folder)
        self.folder_button.grid(row=2, column=2, padx=5 , sticky=tk.E)
        

        self.error_icon = CustomIcon(self, size=25, bg_color="#FECC00", text_color="#486ADC", text="!")
        self.error_icon.grid(row=4, column=0, columnspan=2, pady=5, padx=10)

        self.error_label = tk.Label(self, text="", font=('Sans Serif', 12, "bold"), fg="#FECC00", background=DEFAULT_BACKGROUND_COLOR)
        self.error_label.grid(row=4, column=1, columnspan=2, padx=10, pady=5)

        self.convert_button = tk.Button(self, text="Convert", font=('Sans Serif', 12, "bold"), fg=DEFAULT_TEXT_COLOR, width=20, command=self.get_input)
        self.convert_button.grid(row=3, column=1, padx=20, pady=8)

        self.clear_error_message()

    # def on_file_format_focus(self, event):
    #     # Set the current text of the entry to the dropdown value
    #     if self.file_format_var.get() not in self.file_formats:
    #         pass

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.current_folder.delete(0, tk.END)
            self.current_folder.insert(0, folder_path)
    
    def show_error_message(self, message):
        if message:
            self.error_label.config(text=message)
            self.error_icon.grid(row=3, column=0, columnspan=2)
            self.error_label.grid(row=3, column=1, columnspan=2, padx=10, pady=5)
            
            
            self.convert_button.grid(row=4, column=1, padx=20, pady=8)
            self.error_icon.show()  # Show the custom icon
        

    def clear_error_message(self):
        self.error_label.config(text="")
        self.error_label.grid_forget()
        
        
        self.convert_button.grid(row=3, column=1, padx=20, pady=8)
        self.error_icon.hide()  # Hide the custom icon


    def get_input(self):

        self.clear_error_message()    
        self.format_extension = self.file_format.get()
        self.folderpath = self.current_folder.get()
        self.file_format.focus_set()
        

        if not self.format_extension:
            self.show_error_message("Please enter a file format.")
            self.file_format.focus_set()
        elif not self.folderpath:
            self.show_error_message("Please enter a folder path.")
            self.current_folder.focus_set()
        elif not os.path.isdir(self.folderpath):
            self.show_error_message("No such directory was found")
            self.current_folder.delete(0, tk.END)
            self.current_folder.focus_set()
        elif self.format_extension !="" and os.path.isdir(self.folderpath):
            print(f"{self.folderpath}:{self.format_extension}")
            # Main(self.folderpath, self.format_extension)
            # execute main and show the loading screen or clear the input fields
            self.current_folder.delete(0, tk.END)
            self.file_format.delete(0, tk.END)
            self.pack_forget()
            self.switch_callback_loading(self.folderpath, self.format_extension)
        

class Window():
    
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.mainframe = tk.Frame(self.root)
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=1)
        self.root.geometry("700x500")
        self.root.title("Ext Lab")
        self.header_image = tk.PhotoImage(file='E_header_icon_mod.gif')
        self.root.iconphoto(False, self.header_image)

        spacer_frame = tk.Frame(self.root, background=DEFAULT_BACKGROUND_COLOR)
        spacer_frame.pack(fill="both", expand=True)  # Fill available space vertically

        self.logo_label = tk.Label(self.root, text="EXT LAB", font=('Sans Serif', 48, "bold"), fg=DEFAULT_TEXT_COLOR, background=DEFAULT_BACKGROUND_COLOR, width=100)
        self.logo_label.pack()

        self.mainframe.pack(padx=20, pady=30, expand=1)
        self.root.resizable(False, False)
        self.root.config(background=DEFAULT_BACKGROUND_COLOR)

        # Frames setup
        self.framelist_index = 0
        self.framelist = [
            Interface(self.mainframe, self.switch_callback_loading), 
            LoadingScreen(self.mainframe, self.switch_callback_state), 
            CompleteScreen(self.mainframe, self.switch_callback_interface),
            FailedScreen(self.mainframe, self.switch_callback_interface)
        ]
        for frame in self.framelist:
            frame.pack_forget()
        
        self.framelist[self.framelist_index].pack()

    def switch_callback_loading(self, folderpath, format_extension):
        self.framelist[self.framelist_index].pack_forget()
        loading_screen = self.framelist[1] # Loading screen
        loading_screen.start_task(folderpath, format_extension)
        loading_screen.config(background=DEFAULT_BACKGROUND_COLOR)
        loading_screen.pack()
        self.framelist_index = 1 # current screen displayed

    def switch_callback_state(self, state): # would be cool to add the total amount of complete files converted
        ''' State can be failed (False) or completed (True) and calls the appropriate window depending on which'''
        if state == False:
            self.framelist[self.framelist_index].pack_forget()
            failed_screen = self.framelist[3] # 3 is FailedScreen's index in self.framelist
            failed_screen.config(background=DEFAULT_BACKGROUND_COLOR)
            failed_screen.pack()

            self.framelist_index = 3 # current screen displayed
            
        elif state == True:
            self.framelist[self.framelist_index].pack_forget()
            complete_screen = self.framelist[2] # 2 is CompleteScreen's index in self.framelist
            complete_screen.config(background=DEFAULT_BACKGROUND_COLOR)
            complete_screen.pack()
            self.framelist_index = 2 # current screen displayed

    def switch_callback_interface(self):
        self.framelist[self.framelist_index].pack_forget()
        interface = self.framelist[0] # interface screen
        interface.config(background=DEFAULT_BACKGROUND_COLOR)
        interface.pack()
        self.framelist_index = 0 # current screen displayed

    def run(self):
        self.root.mainloop()
        
interface = Window()
interface.run()

