'''
'''

import numpy as np

# Linearization of data     
def phase_linearization(matrix):
    '''
    Makes a vector of phase values linear without 360 deg subtraction
    '''
    const = 0
    matrix_lin = np.zeros((len(matrix)))
    matrix_lin[:] = matrix[:]
    for elem in range(1, len(matrix)):
        if (matrix[elem] - matrix[elem-1]) > 300:
            const = const + 360
        matrix_lin[elem] = matrix_lin[elem] - const
    return matrix_lin
