'''Copyright Information'''
__author__ = "Agnar Davíð Halldórsson"
__copyright__ = "Copyright (C) 2023 Agnar Davíð Halldórsson"
__license__ = "Public Domain"
__version__ = "1.0"

import shutil
import os
import pathlib

class Basic:
    '''Runs the main program to apply the extension given and create a new folder with copies of the original files\n\n
    Input: \n\tFolderpath: String containing the path to the folder containing the desired files to be converted
    \n\tExtension: String containing the extension to be applied to the new folder name'''
    
    def __init__(self, folderpath:str, extension:str) -> None:
        
        self.FOLDERPATH = folderpath
        self.EXTENSION = extension

        self.destination_folderpath = self.create_folder()
        self.copy_files(self.destination_folderpath)

        
        
    def create_folder(self) -> str:
        '''Returns new folder path as a string'''
        destination_parent = pathlib.Path(self.FOLDERPATH).parent.absolute()

        basename = pathlib.PurePath(self.FOLDERPATH).name
        destination_folderpath = os.path.join(destination_parent, f"{basename}_{self.EXTENSION}")
        os.mkdir(destination_folderpath)
        return destination_folderpath

    def open_files(self, destination_folderpath:str) -> tuple[list, list]:
        '''returns a tuple of lists of: 
            * 1. The objects in the destination directory
            * 2. The filepaths in the destination directory'''
        files_in_folder = os.listdir(destination_folderpath)
        object_list = []
        for file in files_in_folder:
            file_path = os.path.join(destination_folderpath, file)
            with open(file_path) as file_object:
                object_list.append(file_object)
        return object_list, files_in_folder

    def copy_files(self, destination_folderpath:str) -> None:
        files_in_folder = os.listdir(self.FOLDERPATH)
        for file in files_in_folder:
            if os.path.isfile(f"{self.FOLDERPATH}\\{file}"):
                shutil.copy(f"{self.FOLDERPATH}\\{file}", destination_folderpath)
        return