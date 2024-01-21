import pandas as pd 
import sys 

print(sys.argv)    #Result --> ['name_of_the_file', 'command_line_argument']

# sys.argv[0]   #name of the file
day=sys.argv[1]   #command line argument
 
print(f"Job finished successfully for day = {day}")