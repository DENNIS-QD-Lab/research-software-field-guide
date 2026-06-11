#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: maximomateo
"""

import pandas as pd
import os
import h5py as h5
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor
import statistics
import matplotlib.colors as colors

single_directory = ''
cmap = 'viridis'

def OnClick(event):
    global ClickCount 
    if event.inaxes == ax1:
            xValue, yValue = round(event.xdata), round(event.ydata)
            print(xValue)
            ax1.plot(xValue, yValue, 'wo', markersize=3, alpha=0.6)
            fig1.canvas.draw()
            PointSelected[0,ClickCount] = int(xValue)
            PointSelected[1,ClickCount] = int(yValue)
            print(PointSelected)
            ClickCount += 1
            
            if ClickCount >= 3:
                fig1.canvas.mpl_disconnect(cid)
             

for file in os.listdir(single_directory):
    
    ClickCount = 0
    if file.endswith(".h5"):
        print(file)
        FullPath = os.path.join(single_directory, file)
        
        Image         = h5.File(os.path.join(FullPath))['Cube']['Images'][0]
        TimeExposure  = h5.File(os.path.join(FullPath))['Cube']['TimeExposure']
        TimeStamp     = h5.File(os.path.join(FullPath))['Cube']['Timestamp']
        Wavelength    = h5.File(os.path.join(FullPath))['Cube']['Wavelength']
        
        #convert to numpy
        ImageAsNumpy       = np.array(Image)
        TimeExposureNumpy  = np.array(TimeExposure)
        TimeStampNumpy     = np.array(TimeStamp)
        WavelengthNumpy    = np.array(Wavelength)
        print(TimeStamp)

        fig1, ax1 = plt.subplots(figsize=(12, 8))
        ax1.imshow(Image, cmap)
        cursor = Cursor(ax1, useblit=True, color='white', linewidth=0.4)
        #PointSelected stores the x and y values of all the points taken. The first row are all x-values, and the second row are all y-values
        PointSelected  = np.zeros((2,3))
        
        
        cid = fig1.canvas.mpl_connect('button_press_event', OnClick)
        plt.show(block=True)  
        
        #Method for determining the max intensities
        #XY-values are inverted from the .imshow() method
        ImageAsNumpyT = ImageAsNumpy.T
        #Number of points desired to output
        ImageDimensions = ImageAsNumpyT.shape
        NumberofRows = ImageDimensions[1]
       
        
        #The last point (3rd point on the graph) is taken for analysis
        XO = int(PointSelected[1,2])
        YO = int(PointSelected[0,2])
        
        #the bounds are taken from the 1st and 2nd point. 
        InnerBound = int(PointSelected[0,0])
        OuterBound = int(PointSelected[0,1])
        
        DataPoints = NumberofRows-XO

        
        XYValues  = np.zeros((3,DataPoints))
        fig2, ax2 = plt.subplots(figsize=(12, 8))
        
        #Next approach would be to rotate the image with the origin starting at the top #later!
        for i in range(DataPoints):
                ReducedColumn      = ImageAsNumpyT[InnerBound:OuterBound,XO]
                ColumnMaxIndex     = np.argmax(ReducedColumn)
                ColumnMaxIntensity = ReducedColumn[ColumnMaxIndex]
                #print(ColumnMaxIntensity)
                MaxIndex = ColumnMaxIndex + InnerBound
                #print(ImageAsNumpyT[MaxIndex,XO])
                
                #print(MaxIndex)
                MaxIntensity = ImageAsNumpyT[MaxIndex, XO]
                print(MaxIntensity)
                
                XYValues[0,i] = MaxIndex
                XYValues[1,i] = XO
                XYValues[2,i] = MaxIntensity
                #print(XYValues)
            
                ax2.plot(MaxIndex, XO, marker='o', color="white", markersize=0.95)
                #SaveDataPoints(SelectedPoint)
                ColumnMaxIndex = 0 
                MaxIntensity = 0
                XO += 1  #determines how far apart you want the poMouseints to be from each other
        
        ax2.imshow(Image, cmap)    
        plt.show(block=True) 
        
        fig3, ax3 = plt.subplots(figsize=(12, 8))
        meanValue = statistics.mean(XYValues[2,:])
        print('the mean of the data is: ', meanValue)
        print('the SD:', statistics.stdev(XYValues[2,:]))
        ax3.set_title(file)
        ax3.scatter(range(DataPoints),XYValues[2,:])
        ax3.axhline( y = meanValue, color = 'red')
        plt.show(block=True) 

        
        # Save data with dynamic pixel-based structure
        filename1 = 'gettingtimes2.xlsx'
        
        # Create a list of dictionaries, one row per pixel
        data_rows = []
        for pixel_idx in range(DataPoints):
            row = {
                'Pixel_Index': pixel_idx,
               # 'X_Coordinate': int(XYValues[0, pixel_idx]),
               # 'Y_Coordinate': int(XYValues[1, pixel_idx]),
                'Intensity': XYValues[2, pixel_idx],
                'File_Name': file,
                'Exposure_Time': TimeExposureNumpy,
                'Wavelength': WavelengthNumpy,
                'Time_Stamp': TimeStampNumpy,
                'Mean_Intensity': statistics.mean(XYValues[2, :]),
                'SD_Intensity': statistics.stdev(XYValues[2, :])
            }
            data_rows.append(row)
        
        # Create DataFrame from list of dictionaries
        new_data_df = pd.DataFrame(data_rows)
        
        # Append to existing file or create new one
        if os.path.exists(filename1):
            existing_df = pd.read_excel(filename1)     
            combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)
            combined_df.to_excel(filename1, index=False)
        else:
            new_data_df.to_excel(filename1, index=False)