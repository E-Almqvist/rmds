import sys

def get_value_of_key(key): # get the value of an input key, example: -c {VALUE}
    for i in sys.argv:
        if( i == key ):
            return sys.argv[sys.argv.index(key) + 1]
    return None # if no value was found return -1

def key_valid(key):
    return key in sys.argv
