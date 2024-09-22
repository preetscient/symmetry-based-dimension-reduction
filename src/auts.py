'''
Runs saucy on a single network contained in a source file written in the format readable by saucy:

#nodes #edges #colours
edgenode edgenode
...

The output from saucy is written to two files, one containing the automorphism generators (.gaut) and the other containing the output log (.log). 
'''

import subprocess
from pathlib import Path

def main():
    CURRENT_FILE_PATH = Path(__file__).resolve()
    BASE_PATH = CURRENT_FILE_PATH.parents[1]
    
    # Define the stub for output file naming
    input_dir = BASE_PATH / 'data' / 'external' / '5_user_data'
    input_file = list(input_dir.glob('*.*'))[0]
    stub = input_file.stem
    
    # Define the base path for the log and output files
    logstub = str(BASE_PATH / 'data' / 'processed' / 'saucy_output' / stub)
     
    # File containing the network in .scy format    
    fname = str(BASE_PATH / 'data' / 'processed' / 'processing_output' / stub) + '.scy'
    
    # Run the Saucy tool via a subprocess call, passing the input file
    # `-s` is the option to run saucy with a standard mode
    p=subprocess.Popen(['saucy-3.0/saucy','-s',fname],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    # Capture the standard output and error from Saucy execution
    output, error = p.communicate()

    # Write Saucy output (automorphism generators) to the .gaut file
    fgaut=open(logstub+'.gaut','w')
    
    # Write Saucy output (automorphism generators) to the .gaut file
    flog=open(logstub+'.log','w')
                    
    # Decode the binary output from the subprocess and write to respective files
    fgaut.write(output.decode("utf-8")) # Writing the actual output (if any)
    flog.write(error.decode("utf-8")) # Writing the error/log (if any)

    # Close the file streams after writing
    fgaut.close()
    flog.close()
    return

if __name__ == '__main__':
    main()