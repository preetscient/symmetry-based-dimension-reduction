import numpy as np
import pandas as pd
from pathlib import Path

import networkx as nx

def read_in(input_file):
    """
    Reads an input file and returns its contents as a nested list.
    
    Parameters:
    input_file (str or Path): The file path to the input file.

    Returns:
    list: A nested list where each sublist represents a line split by spaces.
    """

    print(input_file)
    lines = []
    for line in open(input_file,'r'):
        newline = line.rstrip()  # Remove trailing spaces or newlines
        lines.append(str(newline).split(' '))  # Split the line by space and append as list
    return lines

def shift_nodes(edgelist):
    """
    Shifts the node indices in an edge list by subtracting 1 from each node's index for zero-based indexing.
    
    Parameters:
    edgelist (list): A nested list representing the edge list where each sublist is an edge.

    Returns:
    list: A nested list with node indices shifted by 1.
    """
    newlist = []
    for x in range(len(edgelist)):
        newrow = []
        for y in range(len(edgelist[x])):
            old_n = int(edgelist[x][y])  # Convert node to integer
            newrow.append(old_n - 1)  # Shift node index by 1
        newlist.append(newrow)
    return newlist

def build_net(edgelist):
    """
    Builds a network graph using NetworkX from the given edge list and removes duplicate and directional edges.
    
    Parameters:
    edgelist (list): A nested list representing the edge list.

    Returns:
    tuple: A NetworkX graph object and a DataFrame of the processed edge list.
    """
    df = pd.DataFrame(edgelist)  # Create DataFrame from edgelist
    colnames = ['sources', 'targets', 'weights', 'timestamps']
    df_width = df.shape[1]  # Get number of columns
    df.columns = colnames[:df_width]  # Assign columns names to DataFrame
    df = df[['sources', 'targets']]  # Keep only source and target columns
    
    # Remove directionality and duplicate edges
    df = rm_directions(df)
    df = rm_duplicates(df)

    # Save processed edge list to CSV
    output_csv = Path.cwd() / 'data/processed/processing_output/source_target_view.csv'
    df.to_csv(output_csv, header=False, index=False)
    
    # Build a graph from the DataFrame
    for x in edgelist:
        G = nx.from_pandas_edgelist(df, source='sources', target='targets', create_using=nx.Graph())
    return G, df

def rm_self_edges(df):
    """
    Removes self-loop edges from the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing source and target columns.

    Returns:
    pd.DataFrame: DataFrame with self-loop edges removed.
    """
    for x in range(len(df)):
        if df['sources'][x] == df['targets'][x]:
            df = df.drop(x, axis=0)  # Drop self-loop edge
    return df


def rm_directions(df):
    """
    Removes directionality by marking and removing reverse edges.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing source and target columns.

    Returns:
    pd.DataFrame: DataFrame with directionality removed.
    """
    for i in range(len(df)):
        source_i = df['sources'][i]
        target_i = df['targets'][i]
        for j in range(len(df)):
            if df['sources'][j] == target_i and df['targets'][j] == source_i:
                # Mark reverse edge for removal
                df['sources'][j] = -1
                df['targets'][j] = -1
    
    # Remove marked edges (-1) and drop NaN values
    df = df[df >= 0].dropna()
    df = df.astype('int')  # Convert columns back to integers
    return df

def rm_duplicates(df):
    """
    Removes duplicate edges from the given DataFrame.
    
    Parameters:
    df (pd.DataFrame): A DataFrame containing source and target columns.

    Returns:
    pd.DataFrame: DataFrame with duplicate edges removed.
    """
    for i in range(len(df)):
        source_i = df['sources'][i]
        target_i = df['targets'][i]
        for j in range(len(df)):
            if i != j:
                # Mark duplicate edges for removal
                if df['sources'][j] == source_i and df['targets'][j] == target_i:
                    df['sources'][j] = -1
                    df['targets'][j] = -1
    
    # Remove marked edges (-1) and drop NaN values
    df = df[df >= 0].dropna()
    df = df.astype('int')  # Convert columns back to integers
    return df

def scy_formatting(G_in, edgelist_df, write_path):
    """
    Writes the graph to a file in .scy format, including nodes, edges, and additional formatting.
    
    Parameters:
    G_in (nx.Graph): A NetworkX graph object.
    edgelist_df (pd.DataFrame): A DataFrame representing the edge list.
    write_path (Path): The file path to write the .scy formatted file.
    """
    # Function to write the graph to a file in .scy format
    n_nodes = len(G_in.nodes())  # Number of nodes in the graph
    n_edges = len(G_in.edges())  # Number of edges in the graph
    colours = 1  # Placeholder for colors, set to 1
    
    with write_path.open("a") as f:
        topline = f"{n_nodes} {n_edges} {colours}\n"
        f.write(topline)
        
        # Sort the DataFrame by 'sources' and iterate over each row to write edges
        edgelist_df = edgelist_df.sort_values('sources', ignore_index=True)
        
        for j in range(len(edgelist_df)):
            source_node = edgelist_df['sources'][j]
            target_node = edgelist_df['targets'][j]
            newline = f"{source_node} {target_node}\n"
            f.write(newline)
    
    return

def main():
    """
    Main function to execute the workflow of reading, processing, building, and formatting a network graph.
    """
    CURRENT_FILE_PATH = Path(__file__).resolve()
    BASE_PATH = CURRENT_FILE_PATH.parents[1]

    # # File paths for input and output files
    input_dir = BASE_PATH / 'data' / 'external' / '5_user_data'
    
    # input_file = list(input_dir.glob('*.edges'))[0]  # Get the first .edges file
    input_file = list(input_dir.glob('*.*'))[0]  # Get the first .edges file
    input_list = read_in(input_file)  # Read input file as a nested list
    new_list = shift_nodes(input_list)  # Shift node indices by -1
    new_net, edgelist = build_net(new_list)  # Build network graph and get edge list
    
    outstub = input_file.stem + '.scy'
    outpath = BASE_PATH / 'data' / 'processed' / 'processing_output' / outstub

    # print('Path exists? ',outpath.exists())
    # print('Stub: ',outstub)

    # # Format the network data and write to .scy file
    scy_formatting(new_net, edgelist, outpath)
    return

if __name__ == "__main__":
    main()