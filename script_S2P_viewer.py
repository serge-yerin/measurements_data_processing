# Python 3
# Program intended to analyze measurements data from NanoVNA
Software_version = '2020.01.21'
Software_name = 'S2P files reader'
# *************************************************************
#                         PARAMETERS                          *
# *************************************************************
directory = 'DATA/'

# *************************************************************
#                    IMPORT LIBRARIES                         *
# *************************************************************
import matplotlib.pyplot as plt
import numpy as np
import pylab
import time
import os

from f_phase_data_linearization import phase_linearization
from f_find_files_only_in_current_folder import find_files_only_in_current_folder

# *************************************************************
#                        MAIN PROGRAM                         *
# *************************************************************

print ('\n\n\n\n\n\n   **************************************************************')
print ('   *            ', Software_name,'  v.',Software_version,'              *    (c) YeS 2020')
print ('   ************************************************************** \n\n')

currentTime = time.strftime("%H:%M:%S")
currentDate = time.strftime("%d.%m.%Y")
print('  Today is ', currentDate, ' time is ', currentTime, '\n')

# Creating a folder where all pictures and results will be stored (if is doesn't exist)
newpath = "S2P_viewer_results"
if not os.path.exists(newpath):
    os.makedirs(newpath)

# Find files in folder
file_name_list = find_files_only_in_current_folder(directory, '.s2p', 1)

files_no = len(file_name_list)
frequency_matrix = []
labels = ['S11 Amplitude', 'S11 Power', 'S11, dB', 'S11 Phase, deg', 'S11 Phase linear, deg', 'S11 VSWR',
          'S21 Amplitude', 'S21 Power', 'S21, dB', 'S21 Phase, deg', 'S21 Phase linear, deg']  #  'R + jX'

for file in range(files_no):
    fname = directory + file_name_list[file]
    handle = open(fname, 'r')

    print('\n Analyzing file:', fname, ' ')

    # Reading datafile and filling the matrices of values
    frequency = []
    data = []

    for line in handle:  # Loop by all lines in file
        if line.startswith("#"):  # Searching comments
            print('  ' + line.rstrip())
        elif line.startswith("!"):  # Searching comments
            print('  ' + line.rstrip())
        else:
            words_in_line = line.split()
            frequency.append(np.float(words_in_line[0]))
            float_list = [np.float(words_in_line[1]), np.float(words_in_line[2]),
                          np.float(words_in_line[3]), np.float(words_in_line[4])]
            data.append(float_list)   # reading date and time of file creation

    frequency = np.array(frequency)
    data = np.array(data)
    data_length = len(data)
    data = data.transpose()
    set_num = len(data)
    frequency[:] = frequency[:] / 1000000  # Hz -> MHz

    print('  Number of frequency points: ', data_length)

    if file == 0:
        # Making complex S-parameters matrices
        S_11 = np.zeros((data_length), dtype=complex)
        S_21 = np.zeros((data_length), dtype=complex)
        full_data = np.zeros((len(labels) * files_no, data_length))
        impedance = np.zeros((files_no, data_length), dtype=complex)

    frequency_matrix.append(frequency)
    S_11[:] = data[0][:] + 1j * data[1][:]
    S_21[:] = data[2][:] + 1j * data[3][:]

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

del data, float_list, S_11, S_21

print('\n\n    Making figures... \n ')

for i in range(len(labels)):
    plt.figure()
    for file in range(files_no):
        plt.plot(frequency_matrix[file], full_data[file * len(labels) + i][:], linewidth='1.50', label=file_name_list[file])
    if labels[i] == 'S11 VSWR':
        plt.ylim(1, 3)
    plt.xlabel('Frequency, MHz')
    plt.ylabel(labels[i])
    #plt.suptitle('Measurement results', fontsize=12, fontweight='bold')
    plt.grid(b=True, which='both', color='0.65', linestyle='--')
    plt.legend(loc='upper right', fontsize=5) # , bbox_to_anchor=(1, 0.5)
    plt.text(0.73, 0.02, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5, transform=plt.gcf().transFigure)
    pylab.savefig(newpath + '/' + ''.join("{:02.0f}".format(i)) + '_' + labels[i] + '.png', bbox_inches='tight', dpi=200)
    plt.close('all')

# Plot of input impedance
fig, ax1 = plt.subplots()
for file in range(files_no):
    ax1.plot(frequency_matrix[file], np.real(impedance[file])[:] * 50, linewidth='1.50', label=file_name_list[file])
ax1.set_xlabel('Frequency, MHz')
ax1.set_ylabel('R input')
fig.suptitle('Measurement results', fontsize=12, fontweight='bold')
ax1.grid(b=True, which='both', color='0.65', linestyle='--')
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
for file in range(files_no):
    ax2.plot(frequency_matrix[file], np.imag(impedance[file])[:] * 50, linewidth='1.50', linestyle='--', label=file_name_list[file])
ax2.set_ylabel('X input')
fig.legend(loc='center left', fontsize=5, bbox_to_anchor=(1, 0.5))
fig.text(0.73, 0.02, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ''.join("{:02.0f}".format(len(labels))) + '_Input impedance.png', bbox_inches='tight', dpi=200)
plt.close('all')


# Plot of input impedance module
fig, ax1 = plt.subplots()
for file in range(files_no):
    ax1.plot(frequency_matrix[file], np.abs(impedance[file])[:] * 50, linewidth='1.50', label=file_name_list[file])
ax1.set_xlabel('Frequency, MHz')
ax1.set_ylabel('|Z| input')
fig.suptitle('Measurement results', fontsize=12, fontweight='bold')
ax1.grid(b=True, which='both', color='0.65', linestyle='--')
fig.legend(loc='center left', fontsize=5, bbox_to_anchor=(0.9, 0.5))
fig.text(0.73, 0.02, 'Processed ' + currentDate + ' at ' + currentTime, fontsize=5, transform=plt.gcf().transFigure)
pylab.savefig(newpath + '/' + ''.join("{:02.0f}".format(len(labels)+1)) + '_Input impedance module.png', bbox_inches='tight', dpi=200)
plt.close('all')


print('\n\n    *** Program finished ***   \n\n\n')
