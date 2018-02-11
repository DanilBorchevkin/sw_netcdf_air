# -*- coding: utf-8 -*-
"""
NetCDF parser for air temperature by time with constant level, lat and long

@author: Danil Borchevkin
"""

import xarray as xr
import csv
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
        # First row
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
        
        # Second row
        self.targetPathLabel = tk.Label(self.master)
        self.targetPathLabel["text"] = "Targer file:"
        self.targetPathLabel.grid(row=1, column=0, padx=4, pady=4)

        self.targetPathInput = tk.Entry(self.master)
        self.targetPathInput["width"] = 50
        self.targetPathInput.grid(row=1, column=1, padx=4, pady=4)
        
        self.targetPathButton = tk.Button(self.master)
        self.targetPathButton["text"] = "Browse"
        self.targetPathButton["command"] = self.chooseTargetFile
        self.targetPathButton.grid(row=1, column=2, columnspan=3, padx=4, pady=4)
        
        # Third row
        #self.prefixLabel = tk.Label(self.master)
        #self.prefixLabel["text"] = "Prefix for files:"
        #self.prefixLabel.grid(row=2, column=0, padx=4, pady=4)
        
        #self.prefixInput = tk.Entry(self.master)
        #self.prefixInput["width"] = 50
        #self.prefixInput.grid(row=2, column=1, padx=4, pady=4)

        # Fouth row
        self.statusLabel = tk.Label(self.master)
        self.statusLabel["text"] = "Select path with NetCDF files and output filename"
        self.statusLabel.grid(row=3, column=0, columnspan=3, padx=4, pady=4)

        # Fifth row
        self.parseButton = tk.Button(self.master)
        self.parseButton["text"] = "Parse Data"
        self.parseButton["command"] = self.parseData
        self.parseButton.grid(row=4, column=0, columnspan=3, padx=4, pady=4)
        
    def chooseTargetFile(self):
        selectedPath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes = (("CSV file","*.csv"),("all files","*.*")))
        if(selectedPath != ""):
            self.targetPathInput.delete(0, tk.END)
            self.targetPathInput.insert(0, selectedPath)    
            
    def chooseSourcePath(self):
        selectedPath = filedialog.askdirectory()
        if(selectedPath != ""):
            self.sourcePathInput.delete(0, tk.END)
            self.sourcePathInput.insert(0, selectedPath)
    
    def parseData(self):
        targetFile = self.targetPathInput.get()
        sourcePath = self.sourcePathInput.get() + "\\"
        
        if (targetFile == "") and (sourcePath == ""):
            messagebox.showwarning("Empty paths", "Selected paths are empty. Please select it properly")
            return
        
        routineOverAllFilesInPath(sourcePath, targetFile)
        messagebox.showinfo("Parsing was finished", "Parsing was finished and result was saving to " + targetFile)

def getFilesInFolder(pathToFolder, fileFormat):
    query = pathToFolder + "*." + fileFormat
    result = glob.glob(query)
    
    return result

def selectDataAndSave(fin, lat, long, level, fout):
    # Open dataset
    ds = xr.open_dataset(fin)
    
    # Select air data by time with constant lat, long and level
    dsloc = ds.sel(lat=lat, lon=long, level=level)
    time = dsloc['time'].data
    air = dsloc['air'].data
    level = dsloc['level'].data
    lat = dsloc['lat'].data
    long = dsloc['lon'].data
       
    # Append data to CSV file
    with open(fout, 'a') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=",", lineterminator="\n")
        for i in range(len(time)):
            csvWriter.writerow([time[i], format(air[i], ".1f"), level, lat, long])
            
def routineOverAllFilesInPath(sourcePath, targetFile):
    # Get list in files
    files = getFilesInFolder(sourcePath, "nc")
    
    # Iteration over all files
    for file in files:
        selectDataAndSave(fin=file, lat=90.0, long=0.0, level=10.0, fout=targetFile)
    
def main():
    root = tk.Tk()
    root.title('NetCDF Air Parser')
    root.resizable(False, False)
    app = Application(master=root)
    app.mainloop()

    
if __name__=="__main__":
    main()
    
    