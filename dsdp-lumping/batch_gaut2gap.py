import os
import re
import glob

current_file_path = os.path.abspath(__file__)

base_path = os.path.join(current_file_path, '..','..')
base_path = os.path.normpath(base_path)

def readautomorphismgroup(fname):
    # fname should be the stub for the output from scy
    # You should therefore have two files:
    # fname.log, and
    # fname.gaut
    
    N = None  # Initialize N to handle cases where it's not found
    
    # Get the number of vertices from the log file
    with open(fname+'.log','r') as flog:
        for line in flog:
            if line.startswith('vertices'):
                try:
                    N = int(line.lstrip('vertices = '))
                except ValueError:
                    raise ValueError(f"Failed to extract number of vertices from line: {line}")
                break
    
    if N is None:
        raise ValueError(f"Number of vertices not found in {fname}.log")

    # Store the generator permutations in a list
    generators = []
    
    # Get generators from gaut file
    with open(fname+'.gaut','r') as fgaut:
        for gstring in fgaut:
            # Remove brackets and split up into twocycles
            gstringlist = gstring.lstrip('(').rstrip(')\n').split(')(')
            # Turn the cycle strings into lists
            g = [[int(num) for num in x.split()] for x in gstringlist]
            generators.append(g)

    return N, generators


def gaut2gap(stub):
        
    count = 1

    for dirpath, dirlist, files in os.walk(stub):
        dname = os.path.join(base_path, 'data', 'interim', 'batch_gap_output')        
        for file in files:
            foutname = os.path.join(dname, file[:-5]) + '.gap'
            # Check file type and whether it exists already
            if file[-4:] == 'gaut' and file[0] != '.' and not os.path.isfile(foutname):
                # Make directory if it doesn't exist
                if len(dname) > 0 and not os.path.exists(dname):
                    print('Making directory: ' + dname)
                    os.makedirs(dname)
                # Source file stubs
                fname = os.path.join(dirpath, file[:-5])
                        
                print(count, foutname)
                count += 1

                # Try to get generators and handle errors if they occur
                try:
                    N, generators = readautomorphismgroup(fname)
                except ValueError as e:
                    # Print a warning and skip to the next file
                    print(f"Skipping {fname}. Reason: {e}")
                    continue  # Move to the next file

                # Write generators to file if there are any
                if len(generators) > 0:
                    with open(foutname, 'w') as fout:
                        fout.write('N:={0};;\n'.format(N))
                        fout.write('z:=[')

                        first = True
                        for generator in generators:    
                            if first:
                                first = False
                            else:
                                fout.write(',')
                            # Write cycle                
                            for cycle in generator:
                                fout.write('(')
                                firstvertex = True                    
                                for vertex in cycle:
                                    if firstvertex:
                                        firstvertex = False
                                    else:
                                        fout.write(',')
                                    fout.write('{0}'.format(vertex + 1))
                                fout.write(')')

                        fout.write('];;\n')
                        fout.write('g:=Group(z);')
    
    return

def main():
    # Running individual directories
    stubpath = os.path.join(base_path,'data','interim','batch_saucy_output')

    gaut2gap(stubpath)
        
    return

if __name__ == '__batch_run__':
    main()