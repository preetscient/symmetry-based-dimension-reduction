import os
import pandas as pd
import numpy as np
import json

current_file_path   = os.path.abspath(__file__)

base_path = os.path.join(current_file_path, '..','..')
base_path = os.path.normpath(base_path)

dot_gap_path = os.path.join(base_path,'data','interim','batch_gap_output')
scy_path = os.path.join(base_path,'data','external','1_network_data','networkrepository')
graph_dat_path = os.path.join(base_path,'data','interim','batch_lumping_output','rowdat')
stubs = os.listdir(dot_gap_path)

def extract_graph_dat(datpath):
    # Initialize a list to store the extracted data
    data = []

    # Loop over all files in the folder
    for filename in os.listdir(datpath):
        # Check if the file has a .json extension
        if filename.endswith('.json'):
            file_path = os.path.join(datpath, filename)
            
            # Open and load the JSON file
            with open(file_path, 'r') as json_file:
                json_data = json.load(json_file)
                
                # Extract "n_nodes" and "rho" if they exist in the JSON data
                n_nodes = json_data.get('n_nodes')
                rho = json_data.get('rho')
                
                # Append the extracted values and filename to the list
                data.append({
                    # 'filename': filename,
                    'n_nodes': n_nodes,
                    'rho': rho
                })

    # Convert the list into a pandas DataFrame for better visualization
    df = pd.DataFrame(data)
    
    # Convert the second column to numeric, setting invalid parsing to NaN
    df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')

    # Replace zero or negative values with NaN to avoid log errors
    df.iloc[:, 1] = df.iloc[:, 1].replace(0, np.nan)
    df.iloc[:, 1] = df.iloc[:, 1].apply(lambda x: np.nan if x <= 0 else np.log(x))
    
    outpath = os.path.join(base_path,'data','interim','batch_lumping_output','graph_data.csv')
    df.to_csv(outpath,index=False)
    return
    
def main():
    # for stub in stubs:
    # print(stub)
    # scy_fname = stub[:-4] + '.scy'
    # scy_fname_path = os.path.join(scy_path,scy_fname)

    # newfname = stub[:-4] + '.csv'
    # newpath = os.path.join(base_path,'data','interim','batch_viz_files',newfname)

    # df = pd.read_csv(scy_fname_path,sep = ' ',usecols=[0, 1], header=None)
    # df = df.drop(index=df.index[0], axis=0)
    # df.columns = ['sources', 'targets']
    # df += 1

    # df.to_csv(newpath,sep = ' ',index=False)

    extract_graph_dat(graph_dat_path)
    return

if __name__ == '__batch_run':
    main()