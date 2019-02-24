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

from f_text_manipulations import find_between, float_convert
from f_phase_data_linearization import phase_linearization


#*************************************************************
#                       FUNCTIONS                            *
#*************************************************************


#*************************************************************
#                       MAIN PROGRAM                         *
#*************************************************************        

for i in range (0,5) : print (' ')
print ('   *****************************************************************')
print ('   *  Ground parameters measurement system data file viewer  v1.0  *      (c) YeS 2019')
print ('   *****************************************************************')
for i in range (0,2) : print (' ')

currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print ('  Today is ', currentDate, ' time is ', currentTime)
print (' ')

# *** Creating a folder where all pictures and results will be stored (if is doen't exist) ***

newpath = 'LVM_viewer_results' 
if not os.path.exists(newpath):
    os.makedirs(newpath)
    


    
# *** Search LVM files in the directory ***
filename = []
filenamelist=[]
i = 0
print ('  Directory: ', directory, '\n')
print ('  List of files to be analyzed: ')
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith('.lvm'):
            i = i + 1
            print ('         ', i, ') ', file)
            filename.append(str(file))
            filenamelist.append(str(os.path.join(root, file)))





# *** Reading data from files ***

array_ADC_counts = []
array_ADC_values = []

for file in range (len(filenamelist)):   # Loop by files in list

    # *** Opening datafile ***
    fname = filenamelist[file]
    handle = open(fname, 'r')
    
    print ('\n Analyzing file:', filename[file])
    
    #   *** Reading datafile and filling the matices of values ***
    ADC_counts = []
    ADC_values = []



    no_of_counts = 0
        
    line_no = 0
    for line in handle:                       # Loop by all lines in file
        line_no = line_no + 1              # 
        if line_no > 22 and len(line.split()) > 0:
            no_of_counts = no_of_counts + 1
            ADC_counts.append(float(line.split()[0].replace(',','.')))
            ADC_values.append(float(line.split()[1].replace(',','.')))
    print ('   * Number of points: ', no_of_counts)

    
    # *** Rearranging data to single array ***        
    array_ADC_counts = np.append(array_ADC_counts, ADC_counts, axis=0)
    array_ADC_values = np.append(array_ADC_values, ADC_values, axis=0)
    
# Reshaping array as (counts * files)
array_ADC_counts = np.reshape(array_ADC_counts, [no_of_counts, len(filenamelist)], order='F')
array_ADC_values = np.reshape(array_ADC_values, [no_of_counts, len(filenamelist)], order='F')
    
del ADC_counts, ADC_values





print ('\n\n    Building figures... \n ')


for i in range(len(filename)):
    filename[i] = filename[i][5:-4].replace('_',' ')


# *** Plotting the graphs ***

for i in range (len(filenamelist)):
    plt.figure()
    plt.plot(array_ADC_counts[:, i], array_ADC_values[:, i], linewidth = '1.50', label = filename[i])
    plt.ylim((-0.05, 1.5))
    plt.xlabel('Points in time')
    plt.ylabel('Amplitude ratio')
    plt.suptitle('Ground parameters measurements', fontsize = 12, fontweight = 'bold')
    #plt.title( 'Measured: ' + fileDate + ' at ' + fileTime, fontsize = 8)
    plt.grid(b = True, which = 'both', color = '0.65', linestyle = '--')
    plt.legend(loc = 'upper right', fontsize = 5)
    plt.text(0.1,  0.02, 'yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
    plt.text(0.73, 0.02,'Processed '+currentDate+ ' at '+currentTime, fontsize = 5, transform = plt.gcf().transFigure)
    pylab.savefig(newpath + '/' + filename[i] + '.png', bbox_inches='tight', dpi = 200)
    #plt.show()
    plt.close('all')


# *** Plotting the graphs ***



plt.figure()
for i in range(len(filenamelist)):
    plt.plot(array_ADC_counts[:, i], array_ADC_values[:, i], linewidth = '1.50', label = filename[i])

plt.ylim((-0.05, 1.5))
plt.xlabel('Points in time')
plt.ylabel('Amplitude ratio')
plt.suptitle('Ground parameters measurements', fontsize = 12, fontweight = 'bold')
#plt.title( 'Measured: ' + fileDate + ' at ' + fileTime, fontsize = 8)
plt.grid(b = True, which = 'both', color = '0.65', linestyle = '--')
plt.legend(loc='center left', fontsize = 5, bbox_to_anchor=(1, 0.5))
plt.text(0.1,  0.02, 'yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
plt.text(0.73, 0.02,'Processed '+currentDate+ ' at '+currentTime, fontsize = 5, transform = plt.gcf().transFigure)
pylab.savefig(newpath + '/01_' + filename[0] + ' - ' + filename[len(filenamelist)-1] +'.png', bbox_inches='tight', dpi = 200)
#plt.show()
plt.close('all')



points_to_plot = [1800, 3000, 7500, 10000, 13000, 16000]




plt.figure()
for i in range(len(points_to_plot) - 1):
    plt.plot(filename[:], array_ADC_values[points_to_plot[i], :], linewidth = '1.50', label = 'Point = ' + str(points_to_plot[i]))
plt.ylim((-0.05, 1.5))
plt.xlabel('Points in time')
plt.ylabel('Amplitude ratio')
plt.xticks(rotation = 60, fontsize = 5)
plt.suptitle('Ground parameters measurements', fontsize = 12, fontweight = 'bold')
#plt.title( 'Measured: ' + fileDate + ' at ' + fileTime, fontsize = 8)
plt.grid(b = True, which = 'both', color = '0.65', linestyle = '--')
plt.legend(loc = 'lower right', fontsize = 5)
plt.text(0.1,  -0.07, 'yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
plt.text(0.73, -0.07,'Processed '+currentDate+ ' at '+currentTime, fontsize = 5, transform = plt.gcf().transFigure)
pylab.savefig(newpath + '/00_' + filename[0] + ' - ' + filename[len(filenamelist)-1] +'.png', bbox_inches='tight', dpi = 200)

#plt.show()
plt.close('all')



print ('\n\n    *** Program finished ***   \n\n\n')
