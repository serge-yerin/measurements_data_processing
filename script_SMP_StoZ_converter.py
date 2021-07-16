# Python 3
# Program intended to analyze data from measurements with OBZOR-103

# *************************************************************
#                         PARAMETERS                          *
# *************************************************************

FilesOrFolder = 1      # To analyze particular files (0) or all files in folder (1)
directory = 'DATA/'
make_phase_linear = 1  # For phase data make linearization instead of jumps from -180 to 180
filename = []

# *************************************************************
#                    IMPORT LIBRARIES                         *
# *************************************************************

import matplotlib.pyplot as plt   # Importing MATPLOTLIB library 
import numpy as np
import pylab
import time
import os

from f_text_manipulations import float_convert, find_between
from f_phase_data_linearization import phase_linearization

# *************************************************************
#                        MAIN PROGRAM                         *
# *************************************************************

print('\n\n\n\n\n   ****************************************************')
print('   *         Obzor-103 data file viewer  v1.0         *      (c) YeS 2018')
print('   **************************************************** \n\n')

currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, '\n')

# *** Creating a folder where all pictures and results will be stored (if is doen't exist) ***

newpath = "SMP_viewer_results" 
if not os.path.exists(newpath):
    os.makedirs(newpath)
    

# *** Choosing files ***

if FilesOrFolder == 1:
    
    # *** Search SMP files in the directory ***
    filename = []
    file_name_list = []
    i = 0
    print('  Directory: ', directory, '\n')
    print('  List of files to be analyzed: ')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.smp'):
                i = i + 1
                print('         ', i, ') ', file)
                filename.append(str(file))
                file_name_list.append(str(os.path.join(root, file)))
else:
    file_name_list = directory + filename


# *** Reading data from files ***

parameters = []
for file in range(len(file_name_list)):   # Loop by files in list

    # *** Opening datafile ***
    fname = file_name_list[file]
    handle = open(fname, 'r')
    
    print('\n\n Analyzing file:', filename[file], ' \n')
    
    #   *** Reading datafile and filling the matrices of values ***
    frequency = []
    list_01 = []
    list_02 = []
    freqSteps = 0
    setNo = 0
    param_names = []
    param_names_01 = []
    param_names_02 = []
    
    for line in handle:                        # Loop by all lines in file
        if line.startswith(";"):              # Searching comments
            print(line.rstrip())
            if line.startswith("; Obzor-102 Network analyzer data file."):
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
            else:
                continue
        else:
            for column in range(0, 3):
                num = line[0 + column*14: 14 + column*14]
                floatnum = float_convert (num)
                if column == 0 and setNo == 1:
                    frequency.append(floatnum)
                if column == 1:
                    list_01.append(floatnum)
                if column == 2:
                    list_02.append(floatnum)
            freqSteps = freqSteps + 1
    
    # *** Rearranging data to single array ***        
    parameters = np.append(parameters, list_01, axis=0)
    parameters = np.append(parameters, list_02, axis=0)
    param_names = np.append(param_names, param_names_01, axis=0)
    param_names = np.append(param_names, param_names_02, axis=0)

parameters = np.reshape(parameters, [Num_of_steps, 2*setNo, len(file_name_list)], order='F')
    
del param_names_01, param_names_02, list_01, list_02


# *** Printing information about data ***        

print(' \n\n Parameters of file: \n ')
print('      Number of frequency steps in file is', Num_of_steps)
print('\n      Measured parameters:')
for i in range(2 * setNo):
    print('      * ', param_names[i])
print('\n\n\n\n    Building figures... \n ')


# *** Plotting the graphs ***

if len(param_names) > 2:

    if param_names[0] == 'S11 Real' and param_names[2] == 'S11 Imag' and \
            param_names[1] == 'S21 Real' and param_names[3] == 'S21 Imag':

        files_no = len(file_name_list)
        frequency_matrix = []
        labels = ['S11 Amplitude', 'S11 Power', 'S11, dB', 'S11 Phase, deg', 'S11 Phase linear, deg', 'S11 VSWR',
                  'S21 Amplitude', 'S21 Power', 'S21, dB', 'S21 Phase, deg', 'S21 Phase linear, deg']  # 'R + jX'

        data_length = len(frequency)

        S_11 = np.zeros((data_length), dtype=complex)
        S_21 = np.zeros((data_length), dtype=complex)
        full_data = np.zeros((len(labels) * files_no, data_length))
        impedance = np.zeros((files_no, data_length), dtype=complex)

        for file in range(files_no):

            S_11[:] = parameters[:, 0, file] + 1j * parameters[:, 2, file]
            S_21[:] = parameters[:, 1, file] + 1j * parameters[:, 3, file]

            full_data[file * len(labels) + 0][:] = np.abs(S_11)[:]
            full_data[file * len(labels) + 1][:] = np.power(np.abs(S_11), 2)[:]
            full_data[file * len(labels) + 2][:] = 10 * np.log10(np.power(np.abs(S_11), 2))[:]
            full_data[file * len(labels) + 3][:] = np.angle(S_11, deg=True)[:]
            full_data[file * len(labels) + 4][:] = phase_linearization(np.angle(S_11, deg=True)[:])
            full_data[file * len(labels) + 5][:] = (1 + np.abs(S_11)[:]) / (1 - np.abs(S_11)[:])
            full_data[file * len(labels) + 6][:] = np.abs(S_21)[:]
            full_data[file * len(labels) + 7][:] = np.power(np.abs(S_21), 2)[:]
            full_data[file * len(labels) + 8][:] = 10 * np.log10(np.power(np.abs(S_21), 2))[:]
            full_data[file * len(labels) + 9][:] = np.angle(S_21, deg=True)[:]
            full_data[file * len(labels) + 10][:] = phase_linearization(np.angle(S_21, deg=True)[:])
            impedance[file][:] = ((1 + S_11[:]) / (1 - S_11[:]))


if len(param_names) > 2:

    if param_names[0] == 'S11 Real' and param_names[1] == 'S11 Ampl Log' and \
            param_names[2] == 'S11 SWR' and param_names[3] == 'S11 Imag'and \
            param_names[4] == 'S11 Phase' and param_names[5] == 'S11 SWR':

        files_no = len(file_name_list)
        frequency_matrix = []
        labels = ['S11 Amplitude', 'S11 Power', 'S11, dB', 'S11 Phase, deg', 'S11 Phase linear, deg', 'S11 VSWR']

        data_length = len(frequency)

        S_11 = np.zeros((data_length), dtype=complex)
        full_data = np.zeros((len(labels) * files_no, data_length))
        impedance = np.zeros((files_no, data_length), dtype=complex)

        for file in range(files_no):

            S_11[:] = parameters[:, 0, file] + 1j * parameters[:, 3, file]

            full_data[file * len(labels) + 0][:] = np.abs(S_11)[:]
            full_data[file * len(labels) + 1][:] = np.power(np.abs(S_11), 2)[:]
            full_data[file * len(labels) + 2][:] = 10 * np.log10(np.power(np.abs(S_11), 2))[:]
            full_data[file * len(labels) + 3][:] = np.angle(S_11, deg=True)[:]
            full_data[file * len(labels) + 4][:] = phase_linearization(np.angle(S_11, deg=True)[:])
            full_data[file * len(labels) + 5][:] = (1 + np.abs(S_11)[:]) / (1 - np.abs(S_11)[:])
            impedance[file][:] = ((1 + S_11[:]) / (1 - S_11[:]))


if len(param_names) == 2:
    if param_names[0] == 'S11 Real' and param_names[1] == 'S11 Imag':

        files_no = len(file_name_list)
        frequency_matrix = []
        labels = ['S11 Amplitude', 'S11 Power', 'S11, dB', 'S11 Phase, deg', 'S11 Phase linear, deg', 'S11 VSWR']

        data_length = len(frequency)

        S_11 = np.zeros((data_length), dtype=complex)
        full_data = np.zeros((len(labels) * files_no, data_length))
        impedance = np.zeros((files_no, data_length), dtype=complex)

        for file in range(files_no):
            S_11[:] = parameters[:, 0, file] + 1j * parameters[:, 1, file]

            full_data[file * len(labels) + 0][:] = np.abs(S_11)[:]
            full_data[file * len(labels) + 1][:] = np.power(np.abs(S_11), 2)[:]
            full_data[file * len(labels) + 2][:] = 10 * np.log10(np.power(np.abs(S_11), 2))[:]
            full_data[file * len(labels) + 3][:] = np.angle(S_11, deg=True)[:]
            full_data[file * len(labels) + 4][:] = phase_linearization(np.angle(S_11, deg=True)[:])
            full_data[file * len(labels) + 5][:] = (1 + np.abs(S_11)[:]) / (1 - np.abs(S_11)[:])
            impedance[file][:] = ((1 + S_11[:]) / (1 - S_11[:]))

for i in range(len(labels)):
    plt.figure()
    for file in range(files_no):
        plt.plot(frequency, full_data[file * len(labels) + i][:], linewidth='1.50', label=file_name_list[file])
    if labels[i] == 'S11 VSWR':
        plt.ylim(1, 3)
    plt.xlabel('Frequency, MHz')
    plt.ylabel(labels[i])
    # plt.suptitle('Measurement results', fontsize=12, fontweight='bold')
    plt.grid(b=True, which='both', color='0.65', linestyle='--')
    plt.legend(loc='upper right', fontsize=5)  # , bbox_to_anchor=(1, 0.5)
    plt.text(0.73, 0.02, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(newpath + '/' + ''.join("{:02.0f}".format(i)) + '_' + labels[i] + '.png', bbox_inches='tight',
                  dpi=200)
    plt.close('all')

# Plot of input impedance
fig, ax1 = plt.subplots()
for file in range(files_no):
    ax1.plot(frequency, np.real(impedance[file])[:] * 50, linewidth='1.50', label='R '+file_name_list[file])
ax1.set_xlabel('Frequency, MHz')
ax1.set_ylabel('R input')
fig.suptitle('Measurement results', fontsize=12, fontweight='bold')
ax1.grid(b=True, which='both', color='0.65', linestyle='--')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
for file in range(files_no):
    ax2.plot(frequency, np.imag(impedance[file])[:] * 50, linewidth='1.50',
             linestyle='--', label='X ' + file_name_list[file])
ax2.set_ylabel('X input')
fig.legend(loc='center left', fontsize=5, bbox_to_anchor=(1.05, 0.5))
fig.text(0.73, 0.02, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ''.join("{:02.0f}".format(len(labels))) + '_Input impedance.png',
              bbox_inches='tight', dpi=200)
plt.close('all')


# Plot of input resistance
fig, ax1 = plt.subplots()
for file in range(files_no):
    ax1.plot(frequency, np.real(impedance[file])[:] * 50, linewidth='1.50', label='R '+file_name_list[file])
ax1.set_yscale('log')
ax1.set_ylim(0.1, 1000)
ax1.set_xlabel('Frequency, MHz')
ax1.set_ylabel('R input')
fig.suptitle('Measurement results', fontsize=12, fontweight='bold')
ax1.grid(b=True, which='both', color='0.65', linestyle='--')
fig.legend(loc='center left', fontsize=5, bbox_to_anchor=(1.05, 0.5))
fig.text(0.73, 0.02, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ''.join("{:02.0f}".format(len(labels))) + '_Input resistance.png',
              bbox_inches='tight', dpi=200)
plt.close('all')

# Plot of input reactance
fig, ax1 = plt.subplots()
for file in range(files_no):
    ax1.plot(frequency, np.imag(impedance[file])[:] * 50, linewidth='1.50', label='R '+file_name_list[file])
# ax1.set_yscale('log')
ax1.set_ylim(-2500, 500)
ax1.set_xlabel('Frequency, MHz')
ax1.set_ylabel('X input')
fig.suptitle('Measurement results', fontsize=12, fontweight='bold')
ax1.grid(b=True, which='both', color='0.65', linestyle='--')
fig.legend(loc='center left', fontsize=5, bbox_to_anchor=(1.05, 0.5))
fig.text(0.73, 0.02, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ''.join("{:02.0f}".format(len(labels))) + '_Input reactance.png',
              bbox_inches='tight', dpi=200)
plt.close('all')


# Plot of input impedance module
fig, ax1 = plt.subplots()
for file in range(files_no):
    ax1.plot(frequency, np.abs(impedance[file])[:] * 50, linewidth='1.50', label=file_name_list[file])
ax1.set_xlabel('Frequency, MHz')
ax1.set_ylabel('|Z| input')
fig.suptitle('Measurement results', fontsize=12, fontweight='bold')
ax1.grid(b=True, which='both', color='0.65', linestyle='--')
fig.legend(loc='center left', fontsize=5, bbox_to_anchor=(0.9, 0.5))
fig.text(0.73, 0.02, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ''.join("{:02.0f}".format(len(labels)+1)) + '_Input impedance module.png',
              bbox_inches='tight', dpi=200)
plt.close('all')


print('\n\n    *** Program finished ***   \n\n\n')
