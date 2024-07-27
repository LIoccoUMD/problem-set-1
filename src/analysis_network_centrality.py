'''
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its stucture to however works to answer the problem
- Make sure the code is line with the standards we're using in this class
'''
import json
import numpy as np
import pandas as pd
import networkx as nx
import requests
from datetime import datetime

# Build the graph
g = nx.Graph()

# Set up your dataframe(s) -> the df that's output to a CSV should include at least the columns 'left_actor_name', '<->', 'right_actor_name'
columns = ['left_actor_name', '<->', 'right_actor_name']
df = pd.DataFrame(columns=columns)

# URL of JSON file
url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
response = requests.get(url)
data = response.text.strip().split('\n')
filename = "imdb_movies_2000to2022.json"
# print(df.head(5))

with open(filename, 'r') as in_file:
    # Don't forget to comment your code
    for line in in_file:
        # Don't forget to include docstrings for all functions
        # Load the movie from this line
        this_movie = json.loads(line)
        # Create a node for every actor
        for actor_id,actor_name in this_movie['actors']:
            g.add_node(actor_id, name=actor_name)
        # add the actor to the graph    
        # Iterate through the list of actors, generating all pairs
        ## Starting with the first actor in the list, generate pairs with all subsequent actors
        ## then continue to second actor in the list and repeat
        
            i = 0 #counter
            for left_actor_id,left_actor_name in this_movie['actors']:
                for right_actor_id,right_actor_name in this_movie['actors'][i+1:]:
                # Get the current weight, if it exists
                    if g.has_edge(left_actor_id, right_actor_id):
                        g[left_actor_id][right_actor_id]["weight"] += 1
                # Add an edge for these actors
                    else:
                        g.add_edge(left_actor_id, right_actor_id, weight=1)
                
            i += 1 


# Print the info below
print("Nodes:", len(g.nodes))

#Print the 10 the most central nodes


# Output the final dataframe to a CSV named 'network_centrality_{current_datetime}.csv' to `/data`