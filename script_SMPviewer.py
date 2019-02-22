# Python 3
# Program intended to analyze data from measurements with OBZOR-103

#*************************************************************
#                        PARAMETERS                          *
#*************************************************************

FilesOrFolder = 1      # To analyze particular files (0) or all files in folder (1)
directory = 'DATA/'
make_phase_linear = 1  # For phase data make linearization instead of jumps from -180 to 180
filename = []


#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************

import matplotlib.pyplot as plt   # Importing MATPLOTLIB library 
import numpy as np
import pylab
import time
import os

from f_text_manipulations import float_convert, find_between
from f_phase_data_linearization import phase_linearization

 


#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************        

for i in range (0,5) : print (' ')
print ('   ****************************************************')
print ('   *         Obzor-103 data file viewer  v1.0         *      (c) YeS 2018')
print ('   ****************************************************')
for i in range (0,2) : print (' ')

currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')

# *** Creating a folder where all pictures and results will be stored (if is doen't exist) ***

newpath = "SMPviewer Results" 
if not os.path.exists(newpath):
    os.makedirs(newpath)
    

# *** Choosing files ***

if FilesOrFolder == 1:
    
    # *** Search SMP files in the directory ***
    filename = []
    filenamelist=[]
    i = 0
    print ('  Directory: ', directory, '\n')
    print ('  List of files to be analyzed: ')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.smp'):
                i = i + 1
                print ('         ', i, ') ', file)
                filename.append(str(file))
                filenamelist.append(str(os.path.join(root, file)))
else:
    filenamelist = directory + filename


# *** Reading data from files ***

parameters = []
for file in range (len(filenamelist)):   # Loop by files in list

    # *** Opening datafile ***
    fname = filenamelist[file]
    handle = open(fname, 'r')
    
    print ('\n\n Analyzing file:', filename[file], ' \n')
    
    #   *** Reading datafile and filling the matices of values ***
    frequency = []
    list_01 = []
    list_02 = []
    freqSteps = 0
    setNo = 0
    param_names = []
    param_names_01 = []
    param_names_02 = []
    
    
    for line in handle:                        # Loop by all lines in file
        if line.startswith(";") :              # Searching comments
            print (line.rstrip())
            if line.startswith("; Obzor-102 Network analyzer data file.") : 
                words_in_line = line.split()
                fileDate = words_in_line[6]    # reading date and time of file creation
                fileTime = words_in_line[7]
            if line.startswith("; View="):
                setNo = setNo + 1              # counting the number of data sets (views)
            if line.startswith("; Fmin"):
                words_in_line = line.split()
                Num_of_steps = int(words_in_line[3][8:])
            if line.startswith("; Parameter1="):
                param_names_01.append(find_between(line, '"', '"'))
            if line.startswith("; Parameter2="):
                param_names_02.append(find_between(line, '"', '"'))
            else: continue
        else:
            for column in range(0, 3):
                num = line[0 + column*14 : 14 + column*14]
                floatnum = float_convert (num)
                if (column == 0 and setNo == 1): frequency.append(floatnum)
                if column == 1: list_01.append(floatnum)
                if column == 2: list_02.append(floatnum)
            freqSteps = freqSteps + 1
    
    # *** Rearranging data to single array ***        
    parameters = np.append(parameters, list_01, axis=0)
    parameters = np.append(parameters, list_02, axis=0)
    param_names = np.append(param_names, param_names_01, axis=0)
    param_names = np.append(param_names, param_names_02, axis=0)

parameters = np.reshape(parameters, [Num_of_steps, 2*setNo, len(filenamelist)], order='F')
    
del param_names_01, param_names_02, list_01, list_02


# *** Printing information about data ***        

print (' \n\n Parameters of file: \n ')
print ('      Number of frequency steps in file is', Num_of_steps)
print ('\n      Measured parameters:')
for i in range (2*setNo):   
    print ('      * ', param_names[i])
print (' \n\n ')

print ('\n\n    Building figures... \n ')


# *** Plotting the graphs ***

for i in range (2*setNo):
    plt.figure()
    for k in range(len(filenamelist)):
        plt.plot(frequency, parameters[:, i, k], linewidth = '1.50', label = filename[k])
    
    plt.xlabel('Frequency, MHz')
    plt.ylabel(param_names[i])
    plt.suptitle(param_names[i], fontsize = 12, fontweight = 'bold')
    plt.title( 'Measured: ' + fileDate + ' at ' + fileTime, fontsize = 8)
    plt.grid(b = True, which = 'both', color = '0.65', linestyle = '--')
    #plt.legend(loc = 'lower right', fontsize = 5) # upper right
    plt.legend(loc='center left', fontsize = 5, bbox_to_anchor=(1, 0.5))
    plt.text(0.73, 0.02,'Processed '+currentDate+ ' at '+currentTime, fontsize = 5, transform = plt.gcf().transFigure)
    pylab.savefig('SMPviewer Results/' + str(i) + '_' + param_names[i] + '.png', bbox_inches='tight', dpi = 200)
    #plt.show()
    plt.close('all')

    
    
'''    
plt.figure()

for k in range(len(filenamelist)):
    plt.plot(frequency, parameters[:, 3, k] - parameters[:, 2, k], linewidth = '1.50', label = filename[k])

plt.xlabel('Frequency, MHz')
plt.ylabel(param_names[i])
plt.suptitle(param_names[i], fontsize=12, fontweight='bold')
plt.title( 'Measured: ' + fileDate + ' at ' + fileTime, fontsize = 10)
plt.grid(b = True, which = 'both', color = '0.00',linestyle = '--')
#plt.legend(loc = 'upper right', fontsize = 5)
pylab.savefig('SMPviewer Results/S21_difference.png', bbox_inches='tight', dpi = 160)
#pylab.savefig('SMPviewer Results/' + param_names[i] + '_' + fname + '_' + fileDate +'.png', bbox_inches='tight', dpi = 160)
#plt.show()
plt.close('all')
'''
    
    
if make_phase_linear == 1:
    for i in range (2*setNo):
        if param_names[i] == "S21 Phase" or param_names[i] == "S21 Фаза":
            
                
    
            plt.figure()
            for k in range(len(filenamelist)):
            
                parameters_lin = parameters[:, i, k]
                parameters_lin = phase_linearization(parameters_lin)
                
                plt.plot(frequency, parameters_lin, linewidth = '1.50', label = filename[k])
                
            plt.xlabel('Frequency, MHz')
            plt.ylabel(param_names[i])
            plt.suptitle(param_names[i], fontsize = 12, fontweight = 'bold')
            plt.title( 'Measured: ' + fileDate + ' at ' + fileTime, fontsize = 8)
            plt.grid(b = True, which = 'both', color = '0.65', linestyle = '--')
            #plt.legend(loc = 'lower left', fontsize = 5) # upper right
            plt.legend(loc='center left', fontsize = 5, bbox_to_anchor=(1, 0.5))
            plt.text(0.73, 0.02,'Processed '+currentDate+ ' at '+currentTime, fontsize = 5, transform = plt.gcf().transFigure)
            pylab.savefig('SMPviewer Results/' + str(i) + '_' + param_names[i] + '_linear.png', bbox_inches='tight', dpi = 200)
            #plt.show()
            plt.close('all')
    
    
    

print ('\n\n    *** Program finished ***   \n\n\n')
