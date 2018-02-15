# -*- coding: utf-8 -*-
"""
NetCDF parser for air temperature by time with constant level, lat and long

@author: Danil Borchevkin
"""

import xarray as xr
import csv
import fileinput
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        # Define frame size and position in the screen :
        ScreenSizeX = master.winfo_screenwidth()  # Get screen width [pixels]
        ScreenSizeY = master.winfo_screenheight() # Get screen height [pixels]
        ScreenRatio = 0.8                              # Set the screen ratio for width and height
        FrameSizeX  = int(ScreenSizeX * ScreenRatio)
        FrameSizeY  = int(ScreenSizeY * ScreenRatio)
        FramePosX   = (ScreenSizeX - FrameSizeX)/2 # Find left and up border of window
        FramePosY   = (ScreenSizeY - FrameSizeY)/2
        #self.master.geometry("%sx%s+%s+%s"%(FrameSizeX,FrameSizeY,FramePosX,FramePosY))
        #self.master.geometry("500x500")
        self.PADDING = 4
        self.createWidgets()

    def createWidgets(self):
        # ------------------------------First row------------------------------
        self.sourcePathLabel = tk.Label(self.master)
        self.sourcePathLabel["text"] = "Source folder:"
        self.sourcePathLabel.grid(row=0, column=0, padx=4, pady=4)
        
        self.sourcePathInput = tk.Entry(self.master)
        self.sourcePathInput["width"] = 50
        self.sourcePathInput.grid(row=0, column=1, padx=4, pady=4)
        
        self.sourcePathButton = tk.Button(self.master)
        self.sourcePathButton["text"] = "Browse"
        self.sourcePathButton["command"] = self.chooseSourcePath
        self.sourcePathButton.grid(row=0, column=2, padx=4, pady=4)
        
        # ----------------------------Second row-------------------------------
        self.targetFileLabel = tk.Label(self.master)
        self.targetFileLabel["text"] = "Target file:"
        self.targetFileLabel.grid(row=1, column=0, padx=4, pady=4)

        self.targetFileInput = tk.Entry(self.master)
        self.targetFileInput["width"] = 50
        self.targetFileInput.grid(row=1, column=1, padx=4, pady=4)
        
        self.targetFileButton = tk.Button(self.master)
        self.targetFileButton["text"] = "Browse"
        self.targetFileButton["command"] = self.chooseTargetFile
        self.targetFileButton.grid(row=1, column=2, columnspan=3, padx=4, pady=4)
        
        # -------------------------Third row-----------------------------------
        self.latLabel = tk.Label(self.master)
        self.latLabel["text"] = "Latitude:"
        self.latLabel.grid(row=2, column=0, padx=4, pady=4)
        
        self.latInput = tk.Entry(self.master)
        self.latInput["width"] = 50
        self.latInput.insert(0, "50.0")
        self.latInput.grid(row=2, column=1, padx=4, pady=4)
        
        self.latDimLabel = tk.Label(self.master)
        self.latDimLabel["text"] = "Deg"
        self.latDimLabel.grid(row=2, column=2, padx=4, pady=4)
        
        # -------------------------Fourth row----------------------------------
        self.longLabel = tk.Label(self.master)
        self.longLabel["text"] = "Longitude:"
        self.longLabel.grid(row=3, column=0, padx=4, pady=4)
        
        self.longInput = tk.Entry(self.master)
        self.longInput["width"] = 50
        self.longInput.insert(0, "25.0")
        self.longInput.grid(row=3, column=1, padx=4, pady=4)
        
        self.longDimLabel = tk.Label(self.master)
        self.longDimLabel["text"] = "Deg"
        self.longDimLabel.grid(row=3, column=2, padx=4, pady=4)
                
        # -------------------------Fith row------------------------------------        
        self.levelLabel = tk.Label(self.master)
        self.levelLabel["text"] = "Level:"
        self.levelLabel.grid(row=4, column=0, padx=4, pady=4)
        
        self.levelInput = tk.Entry(self.master)
        self.levelInput["width"] = 50
        self.levelInput.insert(0, "10.0")
        self.levelInput.grid(row=4, column=1, padx=4, pady=4)
        
        self.levelDimLabel = tk.Label(self.master)
        self.levelDimLabel["text"] = "mBar"
        self.levelDimLabel.grid(row=4, column=2, padx=4, pady=4)

        # ------------------------Sixth row------------------------------------
        self.statusLabel = tk.Label(self.master)
        self.statusLabel["text"] = "Select path with NetCDF files and output filename"
        self.statusLabel.grid(row=5, column=0, columnspan=3, padx=4, pady=4)

        # --------------------------Seventh row--------------------------------
        self.parseButton = tk.Button(self.master)
        self.parseButton["text"] = "Parse Data"
        self.parseButton["command"] = self.parseData
        self.parseButton.grid(row=6, column=0, columnspan=3, padx=4, pady=4)
        
    def chooseTargetFile(self):
        selectedFile = filedialog.asksaveasfilename(defaultextension=".csv", filetypes = (("CSV file","*.csv"),("all files","*.*")))
        if(selectedFile != ""):
            self.targetFileInput.delete(0, tk.END)
            self.targetFileInput.insert(0, selectedFile)    
            
    def chooseSourcePath(self):
        selectedPath = filedialog.askdirectory()
        if(selectedPath != ""):
            self.sourcePathInput.delete(0, tk.END)
            self.sourcePathInput.insert(0, selectedPath)
    
    def parseData(self):
        # Validation of source path
        sourcePath = self.sourcePathInput.get() + "\\"
        if (sourcePath.lstrip() == "\\"):
            messagebox.showwarning("Wrong path to source", "Please select valid source path")
            return
        
        # Validation of target file
        targetFile = self.targetFileInput.get()
        if (targetFile.lstrip() == ""):
            messagebox.showwarning("Wrong target file", "Please select target file")
            return
        
        # Validation latitude
        try:
            lat = float(self.latInput.get())
        except:
            messagebox.showwarning("Wrong latitude", "Please enter valid latitude")
            self.latInput.delete(0, tk.END)
            return
        
        # Validation longitude
        try:
            long = float(self.longInput.get())
        except:
            messagebox.showwarning("Wrong longitude", "Please enter valid longitude")
            self.longInput.delete(0, tk.END)
            return
        
        # Validation level
        try:
            level = float(self.levelInput.get())
        except:
            messagebox.showwarning("Wrong level", "Please enter valid level")
            self.levelInput.delete(0, tk.END)
            return
        
        try:
            routineOverAllFilesInPath(sourcePath, targetFile, lat, long, level)
            messagebox.showinfo("Parsing was finished", "Parsing was finished and result was saving to " + targetFile)
        except KeyError:
            messagebox.showwarning("Key Error", "Please check lat, long and level and available for values")

def getFilesInFolder(pathToFolder, fileFormat):
    query = pathToFolder + "*." + fileFormat
    result = glob.glob(query)
    
    return result

def replaceStringInFile(targetFile, oldString, newString):
    filedata = []
    with open(targetFile, "r") as file:
        filedata = file.readlines()
        
    for line in filedata:    
        line.replace(oldString, newString)
    
    with open(targetFile, "w") as file:
        file.write(filedata)

def selectDataAndSave(fin, lat, long, level, fout):
    # Open dataset
    ds = xr.open_dataset(fin)
        
    # Select air data by time with constant lat, long and level
    dsloc = ds.sel(lat=lat, lon=long, level=level)
    
    # Resample dataset to day mean values
    dsday = dsloc.resample("D", dim="time", how="mean")
    
    time = dsday['time'].data
    air = dsday['air'].data

    # There is some tricky moment. If file is exist then data will append to file
    # Append data to file
    with open(fout, 'a') as file:
        dlm = "    "
        #csvWriter = csv.writer(csvfile, delimiter=";", lineterminator="\n")
        for i in range(len(time)):
            # When we use CSV we can't use delimeter with several chars
            # So in this case we use "bare-metal" write
            file.write(str(time[i]) + 
                       dlm + 
                       format(air[i], ".3f") + 
                       dlm +
                       str(level) + 
                       dlm +
                       str(lat) +
                       dlm + 
                       str(long) +
                       "\n"
                       )
    
def routineOverAllFilesInPath(sourcePath, targetFile, lat, long, level):
    # Get list in files
    files = getFilesInFolder(sourcePath, "nc")
    
    # Iteration over all files
    for file in files:
        selectDataAndSave(fin=file, 
                          lat=lat, 
                          long=long, 
                          level=level, 
                          fout=targetFile)
    
def main():
    root = tk.Tk()
    root.title('NetCDF Air Parser')
    root.resizable(False, False)
    app = Application(master=root)
    app.mainloop()

    
if __name__=="__main__":
    main()
    
    