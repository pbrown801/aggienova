#!/usr/bin/env python
# coding: utf-8

# In[8]:


from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import sys


# In[9]:


def new_LinearR(file,uvw2start,uvw2end,uvm2start,uvm2end,uvw1start,uvw1end,ustart,uend,vstart,vend,bstart,bend): 
    #file needs to be in quotes
    #portion that sets up the arrays to plot the light curve using file and filtername
    filename = file
    data = open(filename, 'r')
    # Reading the data in from the photometry file
    for line in data:
        if not line[0] == "#":
            continue
        fil, mjd, mag, magerr = np.loadtxt(data, dtype=str, usecols = (0,1,2,3), unpack=True) #unpack lets you assign columns names
    for m in range(len(mag)):
        if mag[m]=='NULL':
            mag[m]='nan'
    for me in range(len(magerr)):
        if magerr[me]=="NULL":
            magerr[me]='nan'
    mjd1 = [float(date) for date in mjd]
    mag1 = [float(magnitude) for magnitude in mag]
    magerr1 = [float(magnitudeerr) for magnitudeerr in magerr]
    filters1 = fil
    # I needed to get rid of the NULL values in the ...15.1.dat files, so the next several lines are to make sure the 
    # program doesn't shut down because of them
    filterslist = []
    mjdlist  = []
    maglist = []
    magerrlist = []
    for ii in range(len(filters1)):
        if not np.isnan(mag1[ii]):
            filterslist.append(filters1[ii])
            maglist.append(mag1[ii])
            mjdlist.append(mjd1[ii])
            magerrlist.append(magerr1[ii])
    filters = np.array(filterslist)
    mjd = np.array(mjdlist) #modified julian date
    mag = np.array(maglist) #magnitude
    magerr = np.array(magerrlist) #magnitude error
    # Initializing lists needed to plot the different filters separately
    #making empty lists so they are ready to be filled
    uvw2mjd = []
    uvw2mag = []
    uvw2magerr = []
    uvw2_mjd_lr = [] 
    uvw2_mag_lr = []
    uvm2mjd = []
    uvm2mag = []
    uvm2magerr = []
    uvm2_mjd_lr = [] 
    uvm2_mag_lr = []
    uvw1mjd = []
    uvw1mag = []
    uvw1magerr = []
    uvw1_mjd_lr = [] 
    uvw1_mag_lr = []
    umjd = []
    umag = []
    umagerr = []
    u_mjd_lr = [] 
    u_mag_lr = []
    bmjd = []
    bmag = []
    bmagerr = []
    b_mjd_lr = [] 
    b_mag_lr = []
    vmjd = []
    vmag = []
    vmagerr = []
    v_mjd_lr = [] 
    v_mag_lr = []
    
    # breaking up the filters, mjd, mag, and magerr arrays into separate arrays to make plotting easier
    for i in range(len(filters)):
        if filters[i] == 'UVW2':
            uvw2mjd.append(mjd[i]) #i means which row
            uvw2mag.append(mag[i])
            uvw2magerr.append(magerr[i])
            #the following code is making it to where the program wont shut down 
            #if all the values are NULL for this filter
            uvw2magtest = []
            if uvw2mag[i] == 'NULL':
                uvw2magtest.append(uvw2mag[i])
            if len(uvw2mag) == len(uvw2magtest):
                print('UVW2 filter magnitude values are all NULL')
            else:
                #portion that makes the cuts for the linear regression
                for i in range(len(uvw2mjd)):
                    if uvw2mjd[i] > uvw2start and uvw2mjd[i] < uvw2end:
                        uvw2_mjd_lr.append(uvw2mjd[i])
                        uvw2_mag_lr.append(uvw2mag[i])
                #uvw2 LR
                X1 = np.array(uvw2_mjd_lr)
                Y1 = np.array(uvw2_mag_lr)
                x1 = X1.reshape(-1, 1) 
                y1 = Y1.reshape(-1, 1)  
                linear_regressor = LinearRegression()  
                linear_regressor.fit(x1,y1)  
                y1_pred = linear_regressor.predict(x1)
                
                #plotting code
                plt.ion() #turns on interactive plotting
                fig = plt.figure()
                ax = fig.add_subplot(111)
    
                if len(uvw2mag) > 0:
                    ax.scatter(uvw2mjd, uvw2mag, linewidth=1,marker='o', facecolors='none', edgecolors='r', s=30, label='uvw2', color = 'r')
                    #ax.errorbar(uvw2mjd, uvw2mag, yerr=uvw2magerr, elinewidth=2, capthick = 2, color = 'r') #red
                ax.legend(bbox_to_anchor=(1.32,0.83))
                ax.set_xlabel('Modified Julian Date')
                ax.set_ylabel('Observed Magnitude')
                #ax.set_title('UVOT Light Curves', fontsize = 16)
                ax.axis([int(min(uvw2mjd))-1, math.ceil(np.amax(uvw2mjd))+1,math.ceil(np.amax(mag)+np.amax(magerr)), int(mag.min())-0.25])
                plt.xlim(uvw2mjd[0]-1,uvw2mjd[-1]+1)
                plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
                plt.plot(x1,y1_pred,color='black')
                plt.title("Linear Regression and Light Curve for " + " " + file + ' ' + 'UVW2')
                #plt.savefig(file+filtername+'SN_Linear Regression.png',dpi=72, bbox_inches='tight')
                plt.show()
                
        if filters[i] == 'UVM2':
            uvm2mjd.append(mjd[i])
            uvm2mag.append(mag[i])
            uvm2magerr.append(magerr[i])
            uvm2magtest = []
            if uvm2mag[i] == 'NULL':
                uvm2magtest.append(uvm2mag[i])
            if len(uvm2mag) == len(uvm2magtest):
                print('UVM2 filter magnitude values are all NULL')
            else:
                #portion that makes the cuts for the linear regression
                for i in range(len(uvm2mjd)):
                    if uvm2mjd[i] > uvm2start and uvm2mjd[i] < uvm2end:
                        uvm2_mjd_lr.append(uvm2mjd[i])
                        uvm2_mag_lr.append(uvm2mag[i])
                #uvm2 LR
                X2 = np.array(uvm2_mjd_lr) 
                Y2 = np.array(uvm2_mag_lr)
                x2 = X2.reshape(-1, 1)  
                y2 = Y2.reshape(-1, 1)  
                linear_regressor = LinearRegression()  
                linear_regressor.fit(x2,y2)  
                y2_pred = linear_regressor.predict(x2) 
                
                #plotting code
                plt.ion() #turns on interactive plotting
                fig = plt.figure()
                ax = fig.add_subplot(111)
                if len(uvm2mag) > 0:
                    ax.scatter(uvm2mjd, uvm2mag, linewidth=1,marker='o',facecolors='none', edgecolors='m', s=30, label='uvm2', color= 'm')
                    #ax.errorbar(uvm2mjd, uvm2mag, yerr=uvm2magerr, elinewidth=2, capthick = 2, color='m') #magenta
                ax.legend(bbox_to_anchor=(1.32,0.83))
                ax.set_xlabel('Modified Julian Date')
                ax.set_ylabel('Observed Magnitude')
                #ax.set_title('UVOT Light Curves', fontsize = 16)
                ax.axis([int(mjd.min())-1, math.ceil(np.amax(uvw2mjd))+1,math.ceil(np.amax(mag)+np.amax(magerr)), int(mag.min())-0.25])
                plt.xlim(uvm2mjd[0]-1,uvm2mjd[-1]+1)
                plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
                plt.plot(x2,y2_pred,color='black')
                plt.title("Linear Regression and Light Curve for " + " " + file + ' ' + 'UVM2')
                #plt.savefig(file+filtername+'SN_Linear Regression.png',dpi=72, bbox_inches='tight')
                plt.show()
                
        if filters[i] == 'UVW1':
            uvw1mjd.append(mjd[i])
            uvw1mag.append(mag[i])
            uvw1magerr.append(magerr[i])
            uvw1magtest = []
            if uvw1mag[i] == 'NULL':
                uvw1magtest.append(uvw1mag[i])
            if len(uvw1mag) == len(uvw1magtest):
                print('UVW1 filter magnitude values are all NULL')
            else:
                for i in range(len(uvw1mjd)):
                    if uvw1mjd[i] > uvw1start and uvw1mjd[i] < uvw1end:
                        uvw1_mjd_lr.append(uvw1mjd[i])
                        uvw1_mag_lr.append(uvw1mag[i])
                #uvw1 LR 
                X = np.array(uvw1_mjd_lr) #gotta make it an array
                Y = np.array(uvw1_mag_lr)
                x = X.reshape(-1, 1)  # values converts it into a numpy array
                y = Y.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column
                linear_regressor = LinearRegression()  # create object for the class
                linear_regressor.fit(x,y)  # perform linear regression
                y_pred = linear_regressor.predict(x)  # make predictions
                
                #plotting code
                plt.ion() #turns on interactive plotting
                fig = plt.figure()
                ax = fig.add_subplot(111)
                if len(uvw1mag) > 0:
                    ax.scatter(uvw1mjd, uvw1mag, linewidth=1, marker='o', facecolors='none', edgecolors='k', s=30, label='uvw1', color= 'k')
                    #ax.errorbar(uvw1mjd, uvw1mag, yerr=uvw1magerr, elinewidth=2, capthick = 2, color='k') # black
                ax.legend(bbox_to_anchor=(1.32,0.83))
                ax.set_xlabel('Modified Julian Date')
                ax.set_ylabel('Observed Magnitude')
                #ax.set_title('UVOT Light Curves', fontsize = 16)
                ax.axis([int(mjd.min())-1, math.ceil(np.amax(uvw2mjd))+1,math.ceil(np.amax(mag)+np.amax(magerr)), int(mag.min())-0.25])
                plt.xlim(uvw1mjd[0]-1,uvw1mjd[-1]+1) #had to expand x-axis b/c data wasnt graphing right
                plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
                plt.plot(x,y_pred,color='red')
                plt.title("Linear Regression and Light Curve for " + " " + file + ' ' + 'UVW1')
                #plt.savefig(file+filtername+'SN_Linear Regression.png',dpi=72, bbox_inches='tight')
                plt.show() 
                
        if filters[i] == 'U':
            umjd.append(mjd[i])
            umag.append(mag[i])
            umagerr.append(magerr[i])
            umagtest = []
            if umag[i] == 'NULL':
                umagtest.append(umag[i])
            if len(umag) == len(umagtest):
                print('U filter magnitude values are all NULL')
            else:
                for i in range(len(umjd)):
                    if umjd[i] > ustart and umjd[i] < uend:
                        u_mjd_lr.append(umjd[i])
                        u_mag_lr.append(umag[i])
                #U LR
                X3 = np.array(u_mjd_lr) 
                Y3 = np.array(u_mag_lr)
                x3 = X3.reshape(-1, 1)  
                y3 = Y3.reshape(-1, 1)  
                linear_regressor = LinearRegression()  
                linear_regressor.fit(x3,y3)  
                y3_pred = linear_regressor.predict(x3)
                
                #plotting code
                plt.ion() #turns on interactive plotting
                fig = plt.figure()
                ax = fig.add_subplot(111)
                if len(umag) > 0:
                    ax.scatter(umjd, umag, linewidth=1, marker='o', facecolors='none', edgecolors='c', s=30, label='uvot u', color= 'c')
                    #ax.errorbar(umjd, umag, yerr=umagerr, elinewidth=2, capthick = 2, color='c') #cyan
                ax.legend(bbox_to_anchor=(1.32,0.83))
                ax.set_xlabel('Modified Julian Date')
                ax.set_ylabel('Observed Magnitude')
                #ax.set_title('UVOT Light Curves', fontsize = 16)
                ax.axis([int(min(umjd))-1, math.ceil(np.amax(uvw2mjd))+1,math.ceil(np.amax(mag)+np.amax(magerr)), int(mag.min())-0.25])
                plt.xlim(umjd[0]-1,umjd[-1]+1)
                plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
                plt.plot(x3,y3_pred,color='black')
                plt.title("Linear Regression and Light Curve for " + " " + file + ' ' + 'U')
                #plt.savefig(file+filtername+'SN_Linear Regression.png',dpi=72, bbox_inches='tight')
                plt.show()
                
        if filters[i] == 'B':
            bmjd.append(mjd[i])
            bmag.append(mag[i])
            bmagerr.append(magerr[i])
            bmagtest = []
            if bmag[i] == 'NULL':
                bmagtest.append(bmag[i])
            if len(bmag) == len(bmagtest):
                print('B filter magnitude values are all NULL')
            else:
                for i in range(len(bmjd)):
                    if bmjd[i] > bstart and bmjd[i] < bend:
                        b_mjd_lr.append(bmjd[i])
                        b_mag_lr.append(bmag[i])
                #B LR
                X5 =np.array(b_mjd_lr) 
                Y5 =np.array(b_mag_lr)
                x5 = X5.reshape(-1, 1)  
                y5 = Y5.reshape(-1, 1) 
                linear_regressor = LinearRegression()  
                linear_regressor.fit(x5,y5)  
                y5_pred = linear_regressor.predict(x5)  
                
                #plotting code
                plt.ion() #turns on interactive plotting
                fig = plt.figure()
                ax = fig.add_subplot(111)
                if len(bmag) > 0:
                    ax.scatter(bmjd, bmag, linewidth=1,marker='o',facecolors='none', edgecolors='b', s=50, label='uvot b', color= 'b')
                    #ax.errorbar(bmjd, bmag, yerr=bmagerr, elinewidth=2, capthick = 2, color='b') #blue
                ax.legend(bbox_to_anchor=(1.32,0.83))
                ax.set_xlabel('Modified Julian Date')
                ax.set_ylabel('Observed Magnitude')
                #ax.set_title('UVOT Light Curves', fontsize = 16)
                ax.axis([int(min(bmjd))-1, math.ceil(np.amax(uvw2mjd))+1,math.ceil(np.amax(mag)+np.amax(magerr)), int(mag.min())-0.25])
                plt.xlim(bmjd[0]-1,bmjd[-1]+1)
                plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
                plt.plot(x5,y5_pred,color='black')
                plt.title("Linear Regression and Light Curve for " + " " + file + ' ' + 'B')
                #plt.savefig(file+filtername+'SN_Linear Regression.png',dpi=72, bbox_inches='tight')
                plt.show()
                
        if filters[i] == 'V':
            vmjd.append(mjd[i])
            vmag.append(mag[i])
            vmagerr.append(magerr[i])
            vmagtest = []
            if vmag[i] == 'NULL':
                vmagtest.append(vmag[i])
            if len(vmag) == len(vmagtest):
                print('V filter magnitude values are all NULL')
            else:
                for i in range(len(vmjd)):
                    if vmjd[i] > vstart and vmjd[i] < vend:
                        v_mjd_lr.append(vmjd[i])
                        v_mag_lr.append(vmag[i])
                #V LR
                X4 = np.array(v_mjd_lr) 
                Y4 = np.array(v_mag_lr)
                x4 = X4.reshape(-1, 1)  
                y4 = Y4.reshape(-1, 1)  
                linear_regressor = LinearRegression()  
                linear_regressor.fit(x4,y4)  
                y4_pred = linear_regressor.predict(x4) 
                
                #plotting code
                plt.ion() #turns on interactive plotting
                fig = plt.figure()
                ax = fig.add_subplot(111)
                if len(vmag) > 0:
                    ax.scatter(vmjd, vmag, linewidth=1,marker='o',facecolors='none', edgecolors='g', s=30, label='uvot v', color= 'g')
                    #ax.errorbar(vmjd, vmag, yerr=vmagerr, elinewidth=2, capthick = 2, color='g') #green
                ax.legend(bbox_to_anchor=(1.32,0.83))
                ax.set_xlabel('Modified Julian Date')
                ax.set_ylabel('Observed Magnitude')
                #ax.set_title('UVOT Light Curves', fontsize = 16)
                ax.axis([int(min(vmjd))-1, math.ceil(np.amax(uvw2mjd))+1,math.ceil(np.amax(mag)+np.amax(magerr)), int(mag.min())-0.25])
                plt.xlim(vmjd[0]-1,vmjd[-1]+1)
                plt.gca().get_xaxis().get_major_formatter().set_useOffset(False)
                plt.plot(x4,y4_pred,color='black')
                plt.title("Linear Regression and Light Curve for " + " " + file + ' ' + 'V')
                #plt.savefig(file+filtername+'SN_Linear Regression.png',dpi=72, bbox_inches='tight')
                plt.show()      


# In[5]:


#int(min(uvm2mjd))-1


# In[ ]:


#extra code:
if filtername == "U": 
        xvalue = umjd
        yvalue = umag
    elif filtername == "V":
        xvalue = vmjd
        yvalue = vmag
    elif filtername == "B":
        xvalue = bmjd
        yvalue = bmag
    elif filtername == "UVW2":
        xvalue = uvw2mjd
        yvalue = uvw2mag
    elif filtername == "UVM2":
        xvalue = uvm2mjd
        yvalue = uvm2mag
    elif filtername == "UVW1":
        xvalue = uvw1mjd
        yvalue = uvw1mag
    else:
        print('pls enter a valid filter name')

