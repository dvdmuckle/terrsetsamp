#Code to create a stratified random sample
#The data has to be in the IDRISI working folder
#Florencia Sangermano - August 2015

import win32com.client
import os
import sys
IDRISI32 = win32com.client.Dispatch('IDRISI32.IdrisiAPIServer')

path = IDRISI32.GetWorkingDir()
InputStrata = raw_input("Enter input strata file (without extension): ")
InputLC = InputStrata+'.rst'
outsample = raw_input("Enter output sample file (without extension): ")
samplesize = raw_input("Enter number of samples to be taken by strata: ")
numsample = int(samplesize)
listtop = []
listgrp = []


#check if output file exist in folder before running
for files in os.listdir(path):
    if files == outsample+'.rst':
        from Tkinter import *  #PythonGUI
        import tkMessageBox
        window = Tk()
        window.wm_withdraw()
        #center screen message
        window.geometry("1x1+"+str(window.winfo_screenwidth()/2)+"+"+str(window.winfo_screenheight()/2))
        tkMessageBox.showinfo(title="ERROR", message="File already exists please change output name",parent=window)
        raise SystemExit()
               
IDRISI32.RunModule('BREAKOUT','1*'+InputLC+'*idrtmp*1',1,'','','','',1)
with open(path+'idrtmp.rgf', 'r') as f:  # open text file and call it f
    inputrgf = [line.strip() for line in f] # for each line in f strip it and save it in a list [] called inputfile
    inputfile = inputrgf[1:] #ignores first item in the list (first row in rgf)
    for input in inputfile:
        intop = str(input)
        outtop = 'idrtmp4'+intop
        IDRISI32.RunModule('TOPRANK',intop+'*none*1*'+str(numsample)+'*'+outtop+'*2',1,'','','','',1)
        listtop.append(outtop)
start = 0
for item in listtop: 
    if item != listtop[0]:#ignores class0
        ingroup = str(item)
        outgroup = 'idrtmp3'+ingroup
        IDRISI32.RunModule('RANK', ingroup+'*none*idrtmp0*d',1,'','','','',1)
        IDRISI32.RunModule('RECLASS', 'I*idrtmp0*idrtmp*2*0*'+str(numsample+1)+'*<*-9999*1',1,'','','','',1)
        IDRISI32.RunModule('SCALAR', 'idrtmp*idrtmp2*1*'+str(start),1,'','','','',1)
        IDRISI32.RunModule('RECLASS', 'I*idrtmp2*'+outgroup+'*2*0*'+str(start)+'*'+str(start+1)+'*-9999*1',1,'','','','',1)
        start = start+numsample
        listgrp.append(outgroup)
numbfiles = len(listgrp)
n = 0 
a = 0
input1 = listgrp[n]
#combine samples for all strata
while n <= numbfiles-2:
    a= a+1
    input2 = listgrp[n+1]
    output2 = 'idrtmp5'
    IDRISI32.RunModule('OVERLAY', '7*'+input1+'*'+input2+'*'+output2 + str(a),1,'','','','',1)
    input1 = output2 + str(a)
    n = n+1
finalimg = output2+str(numbfiles-1)

#Rename final sample image
for images in os.listdir(path):
    if images == finalimg+'.RDC':
        inrenrdc = finalimg+'.RDC'
        outrenrdc = outsample+'.RDC'
        os.rename(path+inrenrdc,path+outrenrdc)
    elif images == finalimg+'.rst':
        inrenamerst = finalimg+'.rst'
        outrenamerst = outsample+'.rst'
        os.rename(path+inrenamerst,path+outrenamerst)
IDRISI32.RunModule('RASTERVECTOR','2*1*'+outsample+'*'+outsample+'_pt',1,'','','','',1)
#Remove idrtmp files       
for file in os.listdir(path):
    test = file[0:6]
    if test=='idrtmp':
        os.remove(path+file)
        
