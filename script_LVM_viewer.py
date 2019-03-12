# Python 3
# Program intended to analyze data from measurements with OBZOR-103

#*************************************************************
#                   IMPORT LIBRARIES                         *
#*************************************************************

import matplotlib.pyplot as plt   # Importing MATPLOTLIB library 
import numpy as np
import pylab
import time
import os

from f_text_manipulations import find_between, float_convert


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
directory = 'DATA/'
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


# *** Calculations of amplitude ratios ***
amplitude_ratio = np.zeros((3, len(filename)))
for i in range(len(filename)):
    amplitude_ratio[0, i] = 20*np.log10(array_ADC_values[2949,i] / array_ADC_values[3049,i])
    amplitude_ratio[1, i] = 20*np.log10(array_ADC_values[8949,i] / array_ADC_values[9049,i])
    amplitude_ratio[2, i] = 20*np.log10(array_ADC_values[14949,i] / array_ADC_values[15049,i])

# Shortening file names
for i in range(len(filename)):
    filename[i] = filename[i][5:-4]


# *** Saving amplitude ratio to TXT file ***
TXTfile = open('LVM_viewer_results/Amplitude_ratio_'+ filename[0] + ' - ' + filename[len(filenamelist)-1] +'.txt', "w")
for i in range(len(filename)):
    TXTfile.write(filename[i].rstrip() + '   ' + '   '.join(format(amplitude_ratio[j, i], "20.16f") for j in range(3)) + ' \n')
TXTfile.close() 




print ('\n\n    Building figures... \n ')




# Deleting underscores in file names
for i in range(len(filename)):
    filename[i] = filename[i].replace('_',' ')



# *** Plotting the graphs ***

for i in range (len(filenamelist)):
    fig, ax = plt.subplots()
    plt.plot(array_ADC_counts[:, i], array_ADC_values[:, i], linewidth = '1.50', label = filename[i])
    plt.xlim((0, 19000))
    plt.ylim((-0.05, 1.3))
    ax.set_yticks([0, 0.1, 0.2, 0.3, 0.40, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3], minor=False)
    ax.set_yticks([0, 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05, 1.15, 1.25], minor=True)
    ax.set_xticks([3000, 6000, 9000, 12000, 15000, 18000], minor=False)
    ax.set_xticks([1500, 4500, 7500, 10500, 13500, 16500], minor=True)
    plt.text(1850, - 0.045, '20 MHz', fontsize=10, fontweight = 'bold', color = 'r')
    plt.text(7850, - 0.045, '30 MHz', fontsize=10, fontweight = 'bold', color = 'g')
    plt.text(13850, - 0.045, '60 MHz', fontsize=10, fontweight = 'bold', color = 'b')   
    plt.xlabel('Points in time')
    plt.ylabel('Amplitude, V')
    plt.suptitle('Ground parameters measurements', fontsize = 12, fontweight = 'bold')
    plt.grid(b = True, which = 'both', color = '0.65', linestyle = '--')
    plt.legend(loc = 'upper right', fontsize = 6)
    plt.text(0.1,  0.02, 'yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
    plt.text(0.73, 0.02,'Processed '+currentDate+ ' at '+currentTime, fontsize = 5, transform = plt.gcf().transFigure)
    pylab.savefig(newpath + '/' + filename[i] + '.png', bbox_inches='tight', dpi = 200)
    #plt.show()
    plt.close('all')


# *** Plotting the graphs ***



fig, ax = plt.subplots()
for i in range(len(filenamelist)):
    plt.plot(array_ADC_counts[:, i], array_ADC_values[:, i], linewidth = '1.50', label = filename[i])

plt.ylim((-0.05, 1.5))
plt.xlabel('Points in time')
plt.ylabel('Amplitude, V')
plt.suptitle('Ground parameters measurements', fontsize = 12, fontweight = 'bold')
plt.grid(b = True, which = 'both', color = '0.65', linestyle = '--')
plt.xlim((0, 19000))
plt.ylim((-0.05, 1.3))
ax.set_yticks([0, 0.1, 0.2, 0.3, 0.40, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3], minor=False)
ax.set_yticks([0, 0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.05, 1.15, 1.25], minor=True)
ax.set_xticks([3000, 6000, 9000, 12000, 15000, 18000], minor=False)
ax.set_xticks([1500, 4500, 7500, 10500, 13500, 16500], minor=True)
plt.text(1850, - 0.045, '20 MHz', fontsize=10, fontweight = 'bold', color = 'r')
plt.text(7850, - 0.045, '30 MHz', fontsize=10, fontweight = 'bold', color = 'g')
plt.text(13850, - 0.045, '60 MHz', fontsize=10, fontweight = 'bold', color = 'b')
plt.legend(loc='center left', fontsize = 5, bbox_to_anchor=(1, 0.5))
plt.text(0.1,  0.02, 'yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
plt.text(0.73, 0.02,'Processed '+currentDate+ ' at '+currentTime, fontsize = 5, transform = plt.gcf().transFigure)
pylab.savefig(newpath + '/01_All_measurements_' + filename[0] + ' - ' + filename[len(filenamelist)-1] +'.png', bbox_inches='tight', dpi = 200)
#plt.show()
plt.close('all')



frequencies = [20, 30, 60]
colors = ['r', 'g', 'b']

# Shortening file names once more
for i in range(len(filename)):
    filename[i] = filename[i][0:-4]

fig, ax = plt.subplots(figsize=(8.0, 4.5))
for i in range(3):
    plt.plot(filename[:], amplitude_ratio[i, :], linewidth = '1.50', label = str(frequencies[i]) + ' MHz', color = colors[i])
plt.ylim((-15.0, 15.0))
plt.xlabel('Measurement sessions')
plt.ylabel('Amplitude ratio, dB')
plt.xticks(rotation = 60, fontsize = 6)
ax.set_yticks([-15, -10, -5, 0, 5, 10, 15], minor=False)
ax.set_yticks([-14, -13, -12, -11, -9, -8, -7, -6, -4, -3, -2, -1, 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14], minor=True)
plt.suptitle('Ground parameters measurements', fontsize = 12, fontweight = 'bold')
plt.grid(b = True, which = 'both', color = '0.65', linestyle = '--')
plt.legend(loc = 'lower right', fontsize = 8)
plt.text(0.1,  -0.07, 'yerin.serge@gmail.com, IRA NASU', fontsize=5, transform=plt.gcf().transFigure)
plt.text(0.73, -0.07,'Processed '+currentDate+ ' at '+currentTime, fontsize = 5, transform = plt.gcf().transFigure)
pylab.savefig(newpath + '/00_Amplitude_ratio_' + filename[0] + ' - ' + filename[len(filenamelist)-1] +'.png', bbox_inches='tight', dpi = 200)
#plt.show()
plt.close('all')



print ('\n\n    *** Program finished ***   \n\n\n')
