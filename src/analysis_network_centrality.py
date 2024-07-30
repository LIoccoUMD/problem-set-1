"""
PART 1: NETWORK CENTRALITY METRICS

Using the imbd_movies dataset
- Build a graph and perform some rudimentary graph analysis, extracting centrality metrics from it. 
- Below is some basic code scaffolding that you will need to add to. 
- Tailor this code scaffolding and its structure to however works to answer the problem
- Make sure the code is in line with the standards we're using in this class 
"""

import json
import pandas as pd
import networkx as nx
from datetime import datetime


def build_graph(data):
    # Builds a graph from the movie dataset
    g = nx.Graph()
    
    for movie in data:
        actors = movie['actors']
        for i, (left_actor_id, left_actor_name) in enumerate(actors):
            for right_actor_id, right_actor_name in actors[i+1:]:
                if g.has_edge(left_actor_name, right_actor_name):
                    g[left_actor_name][right_actor_name]['weight'] += 1
                else:
                    g.add_edge(left_actor_name, right_actor_name, weight=1)
    
    return g


def calculate_centrality_metrics(g):
    # Calculates and returns centrality metrics for the graph
    centrality = nx.degree_centrality(g)
    sorted_centrality = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_centrality


def save_to_csv(g):
   # Saves the graph data to a CSV file
    rows = []
    for left_actor, right_actor, data in g.edges(data=True):
        rows.append({'left_actor_name': left_actor, '<->': '<->', 'right_actor_name': right_actor, 'weight': data['weight']})
    
    df = pd.DataFrame(rows)
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    df.to_csv(f'data/network_centrality_{current_datetime}.csv', index=False)


def perform_analysis(data):
    # Performs the network centrality analysis
    g = build_graph(data)
    centrality_metrics = calculate_centrality_metrics(g)
    
    print("Nodes:", len(g.nodes))
    print("Top 10 most central nodes:")
    for actor, centrality in centrality_metrics[:10]:
        print(actor, centrality)
    
    save_to_csv(g)
