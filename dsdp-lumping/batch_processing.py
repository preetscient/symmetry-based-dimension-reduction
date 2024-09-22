import numpy as np
import pandas as pd
import os
import glob

import networkx as nx

def read_in(input_dir):
# Reads in a filename and returns a nested list.
    lines = []
    for line in open(input_dir,'r'): # Open the file and iterate over each line
        newline = line.rstrip() # Remove any trailing newline characters
        lines.append(str(newline).split(' ')) # Split each line by spaces and add to list
    return lines

def shift_nodes(edgelist):
    newlist = []
    for x in range(0,len(edgelist)): # Iterate through each edge in the list
        newrow = []
        for y in range(0,len(edgelist[x])):  # Iterate through each node in the edge
            old_n = int(edgelist[x][y]) # Convert node to integer
            newrow.append(old_n - 1) # Decrement node index by 1
        newlist.append(newrow) # Append adjusted edge to new list
    return newlist

def build_net(edgelist): 
    # Builds a network from the edgelist using NetworkX.

    df = pd.DataFrame(edgelist)  # Create a dataframe from the edgelist
    df.drop(index=df.index[0], axis=0, inplace=True) # Drop the first row, assuming it's a header
    colnames = ['sources','targets','weights','timestamps'] # Define possible column names
    df_width = df.shape[1] # Get the number of columns in the dataframe
    df.columns = colnames[:df_width] # Set the dataframe column names based on its width
    df = df[['sources','targets']] # Keep only the 'sources' and 'targets' columns
    
    # Remove isolated nodes, directed edges, and duplicates
    df = rm_directions(df)
    df = rm_duplicates(df)

    # Create a NetworkX graph from the processed dataframe
    for x in edgelist:
        G = nx.from_pandas_edgelist(df,source='sources', target='targets',create_using =nx.Graph())

    return G, df # Return the graph and the processed dataframe

def rm_self_edges(df):  
    # Removes self-loops (edges where source and target are the same).

    for x in range(0,len(df)): # Iterate through each row in the dataframe
        if df['sources'][x] == df['targets'][x]: # Check if source equals target (self-loop)
            df = df.drop(x,axis=0) # Drop the row if it's a self-loop
        return df

def rm_directions(df):
    # Removes directionality from edges, keeping only one instance of (source, target) pairs.
    
    drop_indices = [] # List to track indices of rows to drop
    for i in range(0,len(df)):  # Iterate over each row in the dataframe
        source_i = df['sources'][i]
        target_i = df['targets'][i]
            
        for j in range(0,len(df)): # Compare each row with every other row

            if df['sources'][j] == target_i and df['targets'][j] == source_i: # Check for reverse direction
                df['sources'][j] == -1 # Mark as invalid
                df['targets'][j] == -1
    
    # Remove invalid rows and convert data types back to integer
    df = df[df>=0].dropna()
    df = df.astype('int')
    return df

def rm_duplicates(df):
    #Removes duplicate edges from the dataframe.
    for i in range(0,len(df)): # Iterate over each row

        source_i = df['sources'][i]
        target_i = df['targets'][i]
            
        for j in range(0,len(df)): # Compare each row with every other row
            source_j = df['sources'][j]
            target_j = df['targets'][j]
            if i != j:
                if source_j == source_i and target_j == target_i: # Check for duplicates
                    df['sources'][j] = -1 # Mark duplicate as invalid
                    df['targets'][j] = -1
    
    # Remove invalid rows and convert data types back to integer
    df = df[df>=0].dropna()
    df = df.astype('int')
    
    return df

def scy_formatting(G_in,edgelist_df,write_path):
#    Output file with edges in .scy format
    n_nodes = len(G_in.nodes()) # Get the number of nodes in the graph
    n_edges = len(G_in.edges()) # Get the number of edges in the graph
    colours = 1 # Assuming one color group for .scy format
    
     # Open the output file for appending
    f = open(write_path,"a")
    
    # Write the top line with node, edge, and color count
    topline = str(n_nodes) + ' ' + str(n_edges) + ' ' + str(colours) + '\n'
    f.write(topline)

    # Sort the edgelist by source nodes and write each edge to the file
    edgelist_df = edgelist_df.sort_values('sources',ignore_index=True)
    
    for j in range(0,len(edgelist_df)):
        source_node     = edgelist_df['sources'][j]
        target_node     = edgelist_df['targets'][j]
        newline         = str(source_node)+' '+str(target_node)
        f.write(newline+'\n')

    f.close() # Close the file after writing
    
    return

def main():
    current_file_path   = os.path.abspath(__file__)
    base_path = os.path.join(current_file_path, '..','..')
    base_path = os.path.normpath(base_path)
    
     # Define the path to the input .scy files
    stubpath = os.path.join(base_path,'data','external','1_network_data','networkrepository','*.scy')

    # Get a list of all .scy files in the specified directory
    stubs = glob.glob(stubpath)
    
    # Iterate through each .scy file
    for stub in stubs:
        input_list          = read_in(stub) # Read the input file into a nested list
        new_list            = shift_nodes(input_list) # Shift node indices by decrementing by 1
        new_net, edgelist   = build_net(new_list)  # Build the network and get the edgelist dataframe
        
        # Define output path for the processed edges
        newpath             = os.path.join(base_path,'data','interim','batch_processing_output')
        edges_fname         = os.path.basename(stub).strip('.scy') + '.edges'
        outpath             = os.path.join(newpath,edges_fname)        
        
        # Format and write the edges in .scy format
        scy_formatting(new_net,edgelist,outpath)
    
    return

# Execute the main function if the script is run as a batch process    
if __name__ == "__batch_run__":
    main()