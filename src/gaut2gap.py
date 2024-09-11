import os
import re

current_file_path = os.path.abspath(__file__)

base_path = os.path.join(current_file_path, '..','..')
base_path = os.path.normpath(base_path)

def readautomorphismgroup(fname):
    # fname should be the stub for the output from scy
    # You should therefore have two files:
    # fname.log, and
    # fname.gaut
    
    # Get the number of vertices from the log file
    flog = open(fname+'.log','r')
    for line in flog:
        if line[0:8]=='vertices':
            N=int(line.lstrip('vertices = '))
            break
    flog.close()

    # Store the generator permutations in a list
    generators=[]
    
    # Get generators from gaut file
    fgaut = open(fname+'.gaut','r')
    for gstring in fgaut:
        # Remove brackets and split up into twocycles
        gstringlist=gstring.lstrip('(').rstrip(')\n').split(')(')
        # Turn the cycle strings into lists
        g=[[int(num) for num in x.split()] for x in gstringlist]
        generators.append(g)
    fgaut.close()
    return N,generators

def main():
    # Running individual directories
    stub = os.path.join(base_path,'data','processed','saucy_output')
    
    count=1

    firstfile=True
    for dirpath, dirlist, files in os.walk(stub):
        dname = os.path.join(base_path,'data','processed','gap_output')        
        for file in files:
            foutname=os.path.join(dname,file[:-5])+'.gap'
            # Check file type and whether it exists already
            if file[-4:]=='gaut' and file[0]!='.' and not os.path.isfile(foutname):
                # Make directory if it doesn't exist
                if len(dname)>0 and not os.path.exists(dname):
                    print('Making directory: '+dname)
                    os.makedirs(dname)
                # Source file stubs
                fname=os.path.join(dirpath,file[:-5])
                        
                print(count,foutname)
                count+=1

                # Generators
                N,generators=readautomorphismgroup(fname)
                        
                # Write generators to file
                if len(generators)>0:
                    fout=open(foutname,'w')
                
                    fout.write('N:={0};;\n'.format(N))
                    fout.write('z:=[')

                    first=True
                    for generator in generators:    
                        if first:
                            first=False
                        else:
                            fout.write(',')
                    # Write cycle                
                        for cycle in generator:
                            fout.write('(')
                            firstvertex=True                    
                            for vertex in cycle:
                                if firstvertex:
                                    firstvertex=False
                                else:
                                    fout.write(',')
                                fout.write('{0}'.format(vertex+1))
                            fout.write(')')

                    fout.write('];;\n')
                    fout.write('g:=Group(z);')
                    fout.close()
    return

if __name__ == '__main__':
    main()