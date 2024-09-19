'''
Runs saucy on a single network contained in a source file written in the format readable by saucy:

#nodes #edges #colours
edgenode edgenode
...

The output from saucy is written to two files, one containing the automorphism generators (.gaut) and the other containing the output log (.log). 
'''

import subprocess
import os
import glob

def auts_gen(fname,logstub):
    p=subprocess.Popen(['saucy-3.0/saucy','-s',fname],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output, error = p.communicate()

    # Write output to file
    scy_fname = os.path.basename(fname)[:-4]
    gautsout = os.path.join(logstub,scy_fname)
    logsout = os.path.join(logstub,scy_fname)

    fgaut=open(gautsout+'.gaut','w')
    flog=open(logsout+'.log','w')
                    
    fgaut.write(output.decode("utf-8"))
    flog.write(error.decode("utf-8"))

    fgaut.close()
    flog.close()
    return

def main():
    current_file_path   = os.path.abspath(__file__)
    base_path = os.path.join(current_file_path, '..','..')
    base_path = os.path.normpath(base_path)
    print(base_path)
    logsout = os.path.join(base_path,'data','interim','batch_saucy_output')
    
    netrepo_path = os.path.join(base_path,'data','external','1_network_data','networkrepository','*')
    
    stubs = glob.glob(netrepo_path)
    
    auts_gen(stubs[0],logsout)
    
    
    for stub in stubs:
        auts_gen(stub,logsout)
    return

if __name__ == '__batch_run__':
    main()