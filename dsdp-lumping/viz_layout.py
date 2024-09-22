from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import os
import ast
import dash_cytoscape as cyto
cyto.load_extra_layouts()
import dash_bootstrap_components as dbc
import networkx as nx
import json
from pathlib import Path

import plotly.graph_objs as go


'''
This script is a Dash application that allows users to visualize and 
analyze network data (graphs).
The application supports both user-uploaded data and preloaded datasets.

Libraries:

Dash, Dash Bootstrap Components, and Cytoscape: Used to create a web-based interactive dashboard.
NetworkX: For graph representation and manipulation.
Plotly: To generate interactive graphs.

'''

# Setting up the base path using Pathlib for cleaner path management
current_file_path = Path(__file__).resolve()
base_path = current_file_path.parents[1]

def read_user_net(filepath):
    """
    Reads the user-uploaded network data from a CSV file.

    Parameters:
    filepath (str or Path): The path to the CSV file containing user network data.

    Returns:
    pd.DataFrame: A DataFrame containing the source and target columns of the network.
    """

    df = pd.read_csv(filepath,sep=' ',header=None) 
    
    colnames = ['sources', 'targets', 'weights', 'timestamps']
    df_width = df.shape[1]
    
    # Assign the appropriate column names based on the input
    df.columns = colnames[:df_width]
    print(df.head())
    df = df[['sources', 'targets']]
    
    # Return the resulting dataframe containing only 'sources' and 'targets'
    return df

def read_preloaded_nets(filename):
    """
    Reads preloaded network data from a CSV file.

    Parameters:
    filename (str): The name of the file containing the preloaded network data.

    Returns:
    pd.DataFrame: A DataFrame containing the source and target columns of the network.
    """
    
    # Construct the full file path
    file_path = base_path / 'data' / 'interim' / 'batch_viz_files' / filename
    
    # Read the CSV file from the constructed file path
    df = pd.read_csv(file_path, sep=' ', header=0)
    colnames = ['sources', 'targets', 'weights', 'timestamps']
    df_width = df.shape[1]
    
    df.columns = colnames[:df_width]
    df = df[['sources', 'targets']]
    return df

def get_preloaded_dataset():
    """
    Retrieves a list of preloaded dataset options for the dropdown menu.

    Returns:
    list: A list of dictionaries, each containing the label and value of a preloaded dataset.
    """

    # Retrieve a list of files from batch_viz_files
    preloaded_path = base_path / 'data' / 'interim' / 'batch_viz_files'
    files = os.listdir(preloaded_path)

    # Create a list of dictionaries with filenames as both label and value
    dataset_options = [{'label': file, 'value': file} for file in files]

    # Sort the dataset options alphabetically by the 'label' key
    dataset_options = sorted(dataset_options, key=lambda x: x['label'])

    # Return the sorted list of dataset options
    return dataset_options

def read_netdat(filepath):
    """
    Reads network statistics from a JSON file.

    Parameters:
    filepath (str or Path): The path to the JSON file containing network data.

    Returns:
    dict: A dictionary with the network statistics if the file exists, otherwise None.
    """

    # Read and load a JSON file from the specified filepath
    # Returns the parsed JSON content
    try:
        with open(filepath) as f:
            net_row = json.load(f)
        return net_row
    except FileNotFoundError:
        return None

def DashStats(net_row):
    """
    Formats network statistics for display in the dashboard.

    Parameters:
    net_row (dict): A dictionary containing network statistics.

    Returns:
    dict: A dictionary with formatted strings for display in the dashboard.
    """

    if net_row is None:
        return {} #Return empty dictionary if nothing is passed.
    
    return {
        'name': f"Network Name: {net_row['graph_name']}",
        'Automporphism group order': f"Automporphism group order: {net_row['aut_grp_order']}",
        'node': f"Nodes: {net_row['n_nodes']}",
        'edge': f"Edges: {net_row['M_edges']}",
        'rho': f"Rho: {net_row['rho']:.2e}",
        'reduction': f"{10**net_row['delta']}",
        # 'reduction': f"{10**net_row['delta']:.2e}",
        'delta': f"Δ: {net_row['delta']}"
    }

def normalize_node_id(node_id):
    """
    Normalizes the node ID by converting it to lowercase and stripping whitespace.

    Parameters:
    node_id (str or int): The ID of the node to normalize.

    Returns:
    str: The normalized node ID.
    """
    return str(node_id).lower().strip()

def assign_colours(G, filename=None):
    """
    Assigns colors to nodes in a graph based on their orbit groups. 
    If no filename is provided, it defaults to a predefined orbit colours file.
    
    Parameters:
    G (networkx.Graph): The graph whose nodes will be colored.
    filename (str, optional): Path to the file containing orbit information. Defaults to None.

    Returns:
    dict: A dictionary mapping each node to an assigned color in hexadecimal RGB format.
    """

    if filename is None: # Set default filename if none is provided
        filename = base_path / 'data' / 'processed' / 'lumping_output' / 'orbitcolours.txt'

    try:
        with open(filename) as coloursf: # Read orbit colour file.
            orbits_in = coloursf.read().strip()
        lines = ast.literal_eval(orbits_in)
    except FileNotFoundError:  #return an empty dictionary if the orbit colour file is not found.
        return {}

    # Initialize an empty dictionary to store node-color mappings
    colourdict = {}
    colcount = 1 # Counter to assign color groups

    # Loop through each orbit group and assign a color group ID to each node in that orbit
    for x, orbit in enumerate(lines):
        colcount += 1 # Increment the color group count
        for node_id in orbit:
            normalized_id = normalize_node_id(node_id) # Normalize node ID (lowercase, trimmed)
            colourdict[normalized_id] = colcount # Assign color group ID to the node

    # Predefined RGB color codes (hex values) for color mapping
    rgb_codes = ['#FF0000', '#FF8700', '#FFD300', '#DEFF0A', '#A1FF0A', 
                 '#0AFF99', '#0AEFFF', '#147DF5', '#580AFF', '#BE0AFF']
    
    # Initialize the final color map for the graph nodes
    colour_map = {}

    # Iterate through each node in the graph
    for node in G.nodes:
        normalized_node = normalize_node_id(node)
        if normalized_node in colourdict:
             # Assign an RGB color based on the color group, cycling through the rgb_codes list
            rgb_place = colourdict[normalized_node] % 10 #Keeping index within bounds
            colour_map[node] = rgb_codes[rgb_place] # Assign the corresponding color
        else:
            # If the node is not found in the color dictionary, assign a default color (light gray)
            colour_map[node] = '#f3f3f3'
    
    # Return the final color map
    return colour_map

def GenCytoElements(G, colour_map, pos):
    """
    Generates Cytoscape-compatible elements for nodes and edges in a graph, 
    including position and color information.

    Parameters:
    G (networkx.Graph): The graph whose nodes and edges are to be converted.
    colour_map (dict): A dictionary mapping nodes to their assigned colors.
    pos (dict): A dictionary containing the x and y positions of each node.

    Returns:
    list: A list of Cytoscape-compatible elements representing both nodes and edges.
    """

    cyto_nodes = [
        {
            'data': {'id': str(node), 'label': str(node), 'color': colour_map.get(node, '#f3f3f3')},
            'position': {'x': pos[node][0] * 500, 'y': pos[node][1] * 500}
        }
        for node in G.nodes()
    ]

    cyto_edges = [
        {'data': {'source': str(edge[0]), 'target': str(edge[1]), 'color': '#f3f3f3'}}
        for edge in G.edges()
    ]

    return cyto_nodes + cyto_edges

def DashboardLayout(elements, app, dash_stats, preloaded_options):
    """
    Defines the layout of the Dash application.

    Parameters:
    elements (list): Cytoscape elements representing the network.
    app (Dash): The Dash application instance.
    dash_stats (dict): Network statistics formatted for display.
    preloaded_options (list): Options for preloaded datasets.

    Returns:
    dash.html.Div: The layout of the application.
    """
    # Define the layout of the app using Bootstrap container for responsiveness

    app.layout = dbc.Container(
        [
            # First row: Displaying the title of the application
            dbc.Row(dbc.Col(html.Div("Dimension Reduction through Symmetry-based Lumping"),
                            className="text-center", # Center the text
                            style={'fontSize': 50})), # Large font size for the title
            
            # Second row: Main content, split into two columns
            dbc.Row(
                [
                     # Left column (4 units wide): Controls and statistics
                    dbc.Col(
                        [
                            # Radio buttons to choose between "User Uploaded Data" and "Preloaded Data"
                            dcc.RadioItems(
                                id='data-source-choice',
                                options=[ # Options for the radio buttons
                                    {'label': 'User Uploaded Data', 'value': 'uploaded'},
                                    {'label': 'Preloaded Data', 'value': 'preloaded'}
                                ],
                                value='preloaded', # Default selected value is 'preloaded'
                                inline=True # Display options inline (horizontally)
                            ),
                            
                            # A div that will dynamically display the preloaded dataset dropdown when needed
                            html.Div(id='preloaded-dataset-selection', style={'display': 'none'}),
                            
                            # Static text explaining the impact of symmetry-based lumping
                            html.Div('Symmetry-based lumping can reduce the state space of your network by:',
                                     style={'fontSize': 20, 'text-align': 'right'}), # Set font size and align right
                            
                            # A div to dynamically display the delta statistic (larger font size)
                            html.Div(id='reduction-stat', style={'fontSize': 20, 'text-align': 'right'}),
                            html.Div(id='delta-stat', style={'fontSize': 40, 'text-align': 'right'}),
                            
                            # Tabs to switch between network statistics and a graph
                            dbc.Tabs(
                                [ 
                                    # First tab: Displaying network statistics (graph name, nodes, edges, etc.)
                                    dbc.Tab(
                                        [
                                            # Dynamic divs to display different network statistics
                                            html.Div(id='graph-name-stat', style={'fontSize': 20, 'text-align': 'right'}),
                                            html.Div(id='node-stat', style={'fontSize': 20, 'text-align': 'right'}),
                                            html.Div(id='edge-stat', style={'fontSize': 20, 'text-align': 'right'}),
                                            html.Div(id='rho-stat', style={'fontSize': 20, 'text-align': 'right'})
                                        ], label="Network Statistics" # Tab label
                                    ),
                                    
                                    # Second tab: Displaying a graph (rho vs nodes)
                                    dbc.Tab(
                                        dcc.Graph(id='rho-nodes-graph'), # Plotly graph component
                                        label="Graph", # Tab label
                                        style = {'height': '200px'} # Set height for the graph area
                                    )
                                ]
                            ),
                        ],
                        width=4 # Left column takes 4 out of 12 grid columns
                    ),
                    
                    # Right column (8 units wide): Cytoscape graph visualization
                    dbc.Col(
                        cyto.Cytoscape(
                            id='cytoscape', # ID of the Cytoscape component
                            elements=elements, # Network elements (nodes and edges) passed as a parameter
                            style={'width': '800px', 'height': '600px'}, # Size of the Cytoscape canvas
                            layout={'name': 'cose'}, # Layout algorithm for node positioning
                            stylesheet=[{ # Custom styles for nodes and edges
                                'selector': 'node', # Style for nodes
                                'style': {
                                    'label': 'data(id)', # Display node label using its 'id' field
                                    'background-color': 'data(color)', # Color nodes based on the 'color' data
                                    'text-valign': 'center', # Center the text vertically
                                    'text-halign': 'center', # Center the text horizontally
                                }
                            }, {
                                'selector': 'edge',  # Style for edges
                                'style': {
                                    'line-color': 'light-grey', # Light grey color for edges
                                    'width': 2 # Set edge width
                                }
                            }]
                        ),
                        width=8, # Right column takes 8 out of 12 grid columns
                        align="end" # Align the Cytoscape graph to the end of the column (vertically)
                    )
                ]
            )
        ]
    )
    return app.layout

# Callback to toggle the preloaded dataset dropdown visibility
@callback(
    Output('preloaded-dataset-selection', 'style'),
    Output('preloaded-dataset-selection', 'children'),
    Input('data-source-choice', 'value')
)

def toggle_preloaded_selection(data_source_choice):
    """
    Toggles the visibility of the preloaded dataset dropdown based on user selection.

    Parameters:
    data_source_choice (str): The selected data source ('uploaded' or 'preloaded').

    Returns:
    tuple: The display style and children elements of the preloaded dataset dropdown.
    """

    # Check if the user has selected the 'preloaded' data source option
    if data_source_choice == 'preloaded':
    # If 'preloaded' is selected, make the dropdown visible and return a dropdown for preloaded datasets
        return {'display': 'block'}, dcc.Dropdown(
            id='preloaded-dataset-dropdown',
            options=get_preloaded_dataset(), # Get available preloaded dataset options
            value=None, # No dataset is selected by default
            placeholder="Select a preloaded dataset", # Placeholder text for the dropdown
            style = {'color': 'darkgrey'} #Set dropdown text colour to dark grey.
        )
    
    # If 'preloaded' is not selected, hide the dropdown by returning 'display: none' and an empty string
    return {'display': 'none'}, ""

# Callback to update the network graph elements
@callback(
    Output('cytoscape', 'elements'),
    Input('data-source-choice', 'value'),
    Input('preloaded-dataset-dropdown', 'value')
)
def update_elements(data_source_choice, selected_dataset):
    """
    Updates the network graph elements based on the selected data source and dataset.

    Parameters:
    data_source_choice (str): The selected data source ('uploaded' or 'preloaded').
    selected_dataset (str): The selected preloaded dataset filename.

    Returns:
    list: A list of Cytoscape-compatible elements representing the network graph.
    """
    if data_source_choice == 'preloaded' and selected_dataset:
        df = read_preloaded_nets(selected_dataset)
        colour_file = base_path / 'data' / 'interim' / 'batch_lumping_output' / 'orbit_colours' / f"{selected_dataset[:-3]}txt"
    elif data_source_choice == 'uploaded':
        usernetpath = base_path / 'dsdp-lumping' / 'visedges.csv'
        df = read_user_net(usernetpath) 
        colour_file = base_path / 'data' / 'processed' / 'lumping_output' / 'orbitcolours.txt'
    else:
        return []

    G = nx.from_pandas_edgelist(df, source='sources', target='targets')
    pos = nx.spring_layout(G)
    colour_map = assign_colours(G, filename=colour_file)
    elements = GenCytoElements(G, colour_map, pos)
    return elements

# Callback to update network statistics
@callback(
    Output('graph-name-stat', 'children'),
    Output('node-stat', 'children'),
    Output('edge-stat', 'children'),
    Output('rho-stat', 'children'),
    Output('reduction-stat', 'children'),
    Output('delta-stat', 'children'),
    Input('data-source-choice', 'value'),
    Input('preloaded-dataset-dropdown', 'value')
)
def update_network_statistics(data_source_choice, selected_dataset):
    """
    Updates the network statistics displayed in the dashboard.

    Parameters:
    data_source_choice (str): The selected data source ('uploaded' or 'preloaded').
    selected_dataset (str): The selected preloaded dataset filename.

    Returns:
    tuple: A tuple of formatted strings for displaying network statistics.
    """

    if data_source_choice == 'preloaded' and selected_dataset:
        netdat_path = base_path / 'data' / 'interim' / 'batch_lumping_output' / 'rowdat' / f"{selected_dataset[:-4]}.json"
        net_row = read_netdat(netdat_path)
    elif data_source_choice == 'uploaded':
        netdat_path = base_path / 'data' / 'processed' / 'lumping_output' / 'rowdat.json'
        net_row = read_netdat(netdat_path)
    else:
        return "No network selected", "", "", "", "", ""

    dash_stats = DashStats(net_row)
    return dash_stats['name'], dash_stats['node'], dash_stats['edge'], dash_stats['rho'], dash_stats['reduction'], dash_stats['delta']

@callback(
    Output('rho-nodes-graph', 'figure'),
    Input('data-source-choice', 'value'),
    Input('preloaded-dataset-dropdown', 'value')
)
def update_graph(data_source_choice, selected_dataset):
    """
    Updates the scatter plot of rho vs number of nodes.

    Parameters:
    data_source_choice (str): The selected data source ('uploaded' or 'preloaded').
    selected_dataset (str): The selected preloaded dataset filename.

    Returns:
    go.Figure: A Plotly figure object containing the scatter plot.
    """

    # Read the CSV file
    file_path = base_path / 'data' / 'interim' / 'batch_lumping_output' / 'graph_data.csv'
    
    # Check if the file exists
    if not file_path.exists():
        return go.Figure()  # Return an empty figure if the file is not found

    # Load the data into a DataFrame
    df = pd.read_csv(file_path)

    # Check if the necessary columns exist in the CSV
    if 'n_nodes' not in df.columns or 'rho' not in df.columns:
        return go.Figure()  # Return an empty figure if the required columns are missing

    # Create the scatter plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['n_nodes'],
        y=df['rho'],
        mode='markers',
        marker=dict(size=10, color='rgba(255, 0, 0, .8)'),
        name='Node vs log10(Rho) Plot'
    ))

    # Update the layout to match the dark theme
    fig.update_layout(
        plot_bgcolor='#1e1e1e',  # Dark background for the plot area
        paper_bgcolor='#1e1e1e',  # Dark background for the graph area
        font_color='white',       # White text color
        title_text="Scatter Plot of log10(ρ) vs Number of Nodes",  # Graph title
        xaxis=dict(title='Number of Nodes (n_nodes)', showgrid=True, gridcolor='gray', color='white'),  # X-axis title and styling
        yaxis=dict(title='log10(ρ)', showgrid=True, gridcolor='gray', color='white'),  # Y-axis title and styling
    )

    return fig

def main():

    """
    Main function to initialize and run the Dash application.
    Reads network data, generates Cytoscape elements, and sets up the application layout.
    """

    # Define the path to the user network data (edges) in the visualization directory

    usernetpath = base_path / 'dsdp-lumping' / 'visedges.csv'
     
    
    df = read_user_net(usernetpath) # Read the user network data from the CSV file into a DataFrame

    # Define the path to the network data (row data)
    netdat_path = base_path / 'data' / 'processed' / 'lumping_output' / 'rowdat.json'
    
    # Read network data from the JSON file
    net_row = read_netdat(netdat_path)

    # Format network data for display
    dash_stats = DashStats(net_row)

    # Create a graph G from the pandas DataFrame
    G = nx.from_pandas_edgelist(df, source='sources', target='targets')
    
    # Generate the layout for the nodes of the graph using a spring layout algorithm
    pos = nx.spring_layout(G)
    
    colour_map = assign_colours(G) # Assign colors to nodes
    elements = GenCytoElements(G, colour_map, pos) #Generate Cytoscape elements (nodes and edges) for visualization

    # Initialize the Dash application with the DARKLY theme from Dash Bootstrap Components
    app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    
    # Retrieve a list of preloaded dataset options for the dashboard
    preloaded_options = get_preloaded_dataset()
    
    # Define the layout for the dashboard
    app.layout = DashboardLayout(elements, app, dash_stats, preloaded_options)

    # Run the Dash application with debugging disabled
    app.run(debug=False)

if __name__ == "__main__":
    main()
