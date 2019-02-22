'''
'''


# Searching of a line part between quotes (or any other symbols)
def find_between(string, start, stop):
    '''
    Finds a text between two characters (symbols)
    '''
    try:
        begin = string.index(start) + len(start)
        end = string.index(stop, begin)
        return string[begin:end]
    except ValueError:
        return "Error!"
        
        
        
# Conversion string to float with replacing come to point    
def float_convert (string):
    '''
    Converts string to float format and replaces coma with point 
    If impossible to convert returns zero and print error to command line
    '''
    try:
        floatnum = float(string.replace(',','.'))
    except:
        print ("Error converting to float!")
        floatnum = 0
        quit()
    return floatnum    
