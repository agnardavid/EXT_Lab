'''Copyright Information'''
__author__ = "Agnar Davíð Halldórsson"
__copyright__ = "Copyright (C) 2023 Agnar Davíð Halldórsson"
__license__ = "Public Domain"
__version__ = "1.0"


import shutil
import os
import pathlib
import time




# Error handling
class InvalidFilenameError(Exception):
    '''Problem:\n\t The name of the designated file or its extension is invalid. It might contain more than one dot (.) \n
        Solution:\n\t A file must only contain one dot which defines its extension'''

class Main:
    '''Runs the main program to apply the extension given and create a new folder with copies of the original files\n\n
    Input: \n\tFolderpath: String containing the path to the folder containing the desired files to be converted
    \n\tExtension: String containing the extension to be applied to all files in the folder'''
    
    def __init__(self, folderpath:str, extension:str, progress_callback, progress_fail_or_complete) -> None:
        
        self.FOLDERPATH = folderpath
        self.EXTENSION = extension
        self.progress_callback = progress_callback
        self.progress_fail_or_complete = progress_fail_or_complete

        destination_folderpath = self.__create_folder()
        self.__copy_files(destination_folderpath)
        self.rename_files(destination_folderpath)
        
    def __create_folder(self) -> str:
        destination_parent = pathlib.Path(self.FOLDERPATH).parent.absolute()

        basename = pathlib.PurePath(self.FOLDERPATH).name
        destination_folderpath = os.path.join(destination_parent, f"{basename}_{self.EXTENSION}")
        os.mkdir(destination_folderpath)
        return destination_folderpath

    def rename_files(self, destination_folderpath:str) -> None:
        files_in_folder = os.listdir(destination_folderpath)
        i = 0
        self.progress_callback(0)
        for file in files_in_folder:
            extension_list = file.split(".")
            if len(extension_list) == 2:
                os.rename(f"{destination_folderpath}\\{extension_list[0]}.{extension_list[1]}", f"{destination_folderpath}\\{extension_list[0]}.{self.EXTENSION}")
            elif len(extension_list) == 1:
                os.rename(f"{destination_folderpath}\\{extension_list[0]}", f"{destination_folderpath}\\{extension_list[0]}.{self.EXTENSION}")
            else:
                pass
                # raise InvalidFilenameError()
                # override the error message with an option from the interface, be able to go back and seperate it anyway using the following command: 
                # os.rename(f"{destination_folderpath}\\{file}", f"{destination_folderpath}\\{extension_list[0]}.{EXTENSION}")
            
            # Calculations for the progress bar
            progress = (i+1) * 100 / len(files_in_folder)
            i += 1

            # Update the progress through the callback function
            if len(files_in_folder) < 100:
                time.sleep(0.1)
            self.progress_callback(progress)
        
        self.progress_callback(100)
        self.progress_fail_or_complete("Complete") # will need to be changed to fail if something fails 
                                                    # but for now we keep it at complete

    def open_files(self, destination_folderpath:str):
        '''returns a list of the objects in the destination folderpath'''
        files_in_folder = os.listdir(destination_folderpath)
        object_list = []
        for file in files_in_folder:
            file_path = os.path.join(destination_folderpath, file)
            with open(file_path) as file_object:
                object_list.append(file_object)
        return object_list

    

    def __copy_files(self, destination_folderpath:str) -> None:
        files_in_folder = os.listdir(self.FOLDERPATH)
        for file in files_in_folder:
            if os.path.isfile(f"{self.FOLDERPATH}\\{file}"):
                shutil.copy(f"{self.FOLDERPATH}\\{file}", destination_folderpath)
        return