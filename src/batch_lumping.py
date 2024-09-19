import numpy as np
import ast
from pathlib import Path
import math
import time

import os
import re
import networkx as nx

import pandas as pd
from gappy import gap

import subprocess
import glob

import json

current_file_path   = os.path.abspath(__file__)
base_path = os.path.join(current_file_path, '..','..')
base_path = os.path.normpath(base_path)

lumpsout_path = os.path.join(base_path,'data','interim','batch_lumping_output')

# Set GAP options with increased memory (e.g., GB)
# gap.eval('SetUserPref("GAP_MEM_LIMIT", 4000000000);')  # 4GB

def read_am(aut_filename):
    #Reads in the automorphism data for a given network from a .gap file.
    aut_in = []
    with open(aut_filename, 'r') as file: #Open file in read mode
        for line in file:
                aut_in.append(line.strip()) # Remove leading/trailing whitespace and add to list
    return  aut_in

def read_log(log_filename):
    # Reads and extracts specific data from a log file.
    grp_kw = [
        'vertices',
        'edges',
        'up size',
        'levels',
        'nodes',
        'generators',
        'total support',
        'average support',
        'nodes per generator',
        'bad nodes',
        'cpu time (s)'
        ]
    
    extracted_data = {}

    with open(log_filename,'r') as file:
        for line in file:
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

            if key in grp_kw:
                extracted_data[key] = value #Store key-value pairs if key is in grp_kw
    return extracted_data

def aut_processing(aut_in,autstub):
    # Processes the automorphism data extracted from the .gap file.
    
    # Example of aut_in:
    # ['N:=18;;', 'z:=[(5,6),(5,8),(13,15),(1,2),(1,3)];;', 'g:=Group(z);']
    
    n_pattern = r'N:=([^;]+);;' # Pattern to extract the number of nodes
    z_pattern = r'z=([^;]+);;' # Pattern to extract automorphism group generators
    
    nstring = aut_in[0]
    nstring = nstring.replace('N:=','')
    nstring = nstring.replace(';;','')
    network_n = int(ast.literal_eval(nstring)) # Convert nstring to integer

    if network_n >= 100000000: # If network size is too large
        flag = -1 # Return a flag value
        return flag
    else:

        zout = aut_in[1]

        if zout.count(';') > 1:
            zout = zout.replace(';;',';')
    
        #zaut = gap.eval(zout)
        zaut = zout

        # Write the automorphism group data to a test file
        ztestpath = os.path.join(lumpsout_path,'zaut_test',autstub+'.txt')
        txt_file = open(ztestpath,"a")
        txt_file.write(zout)
        txt_file.close()
        return zaut

# Order() is order of the group
# Does Group() results in the same output as GroupWithGenerators()?

def norbits(zin, N, rho_method):
    #  Calculates the number of orbits in a graph using different methods.

    z = gap.eval(zin)
    G = gap.eval('zgroup:=GroupWithGenerators(z);')
    
    if rho_method == 'tuple':
        zorbits = gap.OrbitsDomain(G, Tuples([0,1], 3), Permuted)
        orbit_count = len(zorbits)

    elif rho_method == 'polya':
        zorbits = -1
        orbit_count = polya_enum(G, N)

        # If polya_enum returned infinity, handle it safely
        if math.isinf(orbit_count):
            print("Polya enumeration returned infinity. Setting orbit count to a default value.")
            orbit_count = -1  # Use a fallback value for orbit_count if necessary
        zorbits = list(gap.Orbits(G))

    zorder = int(gap.Size(G)) # Get the size of the group

    return orbit_count, zorder, zorbits


def cycle_number(p,n):
    #Calculates the cycle number of a permutation.
    cs = gap.CycleStructurePerm(p) # Get cycle structure of permutation
    m = gap.NrMovedPoints(p) # Get number of moved points
    cyc_tot = 0

    for x in cs:
        if x is int:
            tot += x
    return cyc_tot+n-m

def rationals_fix(rational):
    # Converts a rational string into a float value.

    if '/' in rational:
        num, denom = rational.split('/',1)
        num = num.strip()
        denom = num.strip()
        quot = int(num)/int(denom)
        return quot

    else:
        return float(rational)

def polya_enum(G, N):
    #Implements polya enumeration of a group to count the number of distinct objects.
    cl = gap.ConjugacyClasses(G)
    tot = 0
    clist = sorted(cl)
    
    for item in clist:
        rep = gap.Representative(item)
        cn = cycle_number(rep, N)
        size = gap.Size(item)
        
        try:
            # Safely calculate the increment and handle overflow
            increment = size * 2**cn
            if math.isinf(increment):
                raise OverflowError(f"Overflow in increment calculation: size={size}, cn={cn}")
            tot += increment
        except OverflowError as e:
            print(f"OverflowError: {e}. Skipping this term.")
            continue

    try:
        order_g = gap.Order(G)

        # Ensure neither total nor order is infinite
        gorder = rationals_fix(str(order_g))
        tot = rationals_fix(str(tot))

        if math.isinf(tot) or math.isinf(gorder):
            raise OverflowError("Infinity encountered in total or group order.")

        quot = tot / gorder
    except ZeroDivisionError:
        print("Division by zero in Polya enumeration. Returning infinity.")
        return float('inf')
    except OverflowError as e:
        print(f"OverflowError during Polya enumeration: {e}. Returning infinity.")
        return float('inf')

    return quot

def delta_gen(log_extract, rho):
    #  Calculates the delta parameter for a network.
    N = int(log_extract['vertices'])
    M = int(log_extract['edges'])
    nrho = int(rho)
    
    if M <= 0 or nrho <= 0:  # Ensure that M and nrho are not zero or negative
        print(f"Invalid values for log calculation: M={M}, nrho={nrho}. Skipping delta calculation.")
        return float('inf')  # Or some default/fallback value
    
    try:
        num = N * math.log10(M)
        denom = math.log10(nrho)
        delta = round(num / denom)
    except (ValueError, OverflowError) as e:
        print(f"Error during delta calculation: {e}. Using default value.")
        delta = float('inf')  # Or some default/fallback value

    return delta

def gen_row(stubpath):
    print(stubpath)
    new_row = dict()
    
    rowstub = os.path.basename(stubpath)[:-4]
        
    aut_directory = os.path.join(base_path,'data','interim','batch_gap_output')
    log_directory = os.path.join(base_path,'data','interim','batch_saucy_output')

    aut_filename = os.path.join(aut_directory,rowstub+'.gap')
    log_filename = os.path.join(log_directory,rowstub+'.log')

    if os.path.exists(log_filename):
        log_extract = read_log(log_filename)

    if os.path.exists(aut_filename):
        aut_in = read_am(aut_filename)
        zaut = aut_processing(aut_in,rowstub)

        n_orbits, zorder, zorbits = norbits(zaut,int(log_extract['vertices']),'polya')

        #colours = colour_gen(zorbits)
        new_row = {
            'graph_name'    : rowstub,
            'n_nodes'       : log_extract['vertices'],
            'M_edges'       : log_extract['edges'],
            'aut_grp_order' : zorder,
            'rho'           : n_orbits,
            'avg_support'   : log_extract['total support'],
            'tot_support'   : log_extract['average support'],
            #'colours'       : colours,
            'orbits'        : str(zorbits),
            'delta'         : delta_gen(log_extract,n_orbits)
            }
        
        datpath = os.path.join(lumpsout_path,'rowdat',rowstub+'.json')
        
        with open(datpath,'w') as fp:
            json.dump(new_row,fp)

        colourspath = os.path.join(lumpsout_path,'orbit_colours',rowstub+'.txt')

        coloursf = open(colourspath,"a")
        coloursf.write(str(zorbits))
        coloursf.close()
    return new_row

def stub_gen(directory):
    files = []
    stub_pattern = r'.gap'

    for entry in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, entry)):
            if '.gap' in entry:
                stub = re.sub(stub_pattern,'',entry)
                files.append(stub)

    return sorted(files), len(files)

def main():
    current_file_path   = os.path.abspath(__file__)
    base_path = os.path.join(current_file_path, '..','..')
    base_path = os.path.normpath(base_path)

    lumpsout_path = os.path.join(base_path,'data','interim','batch_lumping_output')

    stubpath = os.path.join(base_path,'data','interim','batch_gap_output','*')
    stubs = sorted(glob.glob(stubpath))

    inter_table = []
    
    txtbase = os.path.join(base_path,'data','interim','batch_lumping_output','zaut_test')
    
    for stub in stubs:
        txt_file = os.path.basename(stub)[:-4] + 'txt'
        txt_path = os.path.join(txtbase,txt_file)
        if os.path.exists(txt_file):
            print(f"Skipping file: {txt_path}. '{txt_file}' already exists.")
        else:
            rowi = []
            start_time = time.time()
            rowi = gen_row(stub)
            elapsed_time = time.time() - start_time

            if elapsed_time > 120:
                print(f"{stub}took more than 120s to complete")
                continue
            inter_table.append(rowi)

    output_table = pd.DataFrame(inter_table)

    out_colnames = [
        'graph_name',
        'n_nodes',
        'M_edges',
        'aut_grp_order',
        'rho',
        'avg_support',
        'tot_support',
        'delta']
        #'colours']
        
    output_table = pd.DataFrame(inter_table)
    output_table = output_table.drop(index=df.index[0], axis=0, inplace=True)
    tablepath = os.path.join(lumpsout_path,'lumps_out.csv')
    
    output_table.to_csv(tablepath,index=False)
    return

if __name__ == '__batch_run__':
    main()