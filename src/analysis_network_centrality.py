import json
import pandas as pd
import networkx as nx
import requests
from datetime import datetime

def download_data(url: str, filename: str):
    """Download and save the JSON data from the specified URL."""
    response = requests.get(url)
    with open(filename, 'w') as f:
        f.write(response.text)

def build_graph(data: list) -> nx.Graph:
    """Build a graph from the JSON data."""
    g = nx.Graph()
    for line in data:
        this_movie = json.loads(line)
        actors = this_movie.get('actors', [])
        for actor_id, actor_name in actors:
            g.add_node(actor_id, name=actor_name)
        
        for i, (left_actor_id, left_actor_name) in enumerate(actors):
            for right_actor_id, right_actor_name in actors[i+1:]:
                if g.has_edge(left_actor_id, right_actor_id):
                    g[left_actor_id][right_actor_id]['weight'] += 1
                else:
                    g.add_edge(left_actor_id, right_actor_id, weight=1)
    return g

def calculate_centrality(g: nx.Graph) -> pd.DataFrame:
    """Calculate centrality metrics for the graph and return as a DataFrame."""
    degree_centrality = nx.degree_centrality(g)
    centrality_df = pd.DataFrame.from_dict(degree_centrality, orient='index', columns=['degree_centrality'])
    return centrality_df

def save_to_csv(df: pd.DataFrame, filename: str):
    """Save the DataFrame to a CSV file."""
    df.to_csv(filename, index_label='actor_id')

def main():
    url = "https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true"
    filename = "imdb_movies_2000to2022.json"
    
    # Download the data if not already downloaded
    download_data(url, filename)
    
    # Load data from the JSON file
    with open(filename, 'r') as f:
        data = f.readlines()

    # Build the graph
    g = build_graph(data)
    
    # Print graph info
    print("Nodes:", len(g.nodes))
    print("Edges:", len(g.edges))
    
    # Calculate and print the 10 most central nodes
    centrality_df = calculate_centrality(g)
    top_10_central = centrality_df.sort_values(by='degree_centrality', ascending=False).head(10)
    print("Top 10 most central nodes:")
    print(top_10_central)
    
    # Save the final DataFrame to a CSV file
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"network_centrality_{current_datetime}.csv"
    save_to_csv(centrality_df, output_filename)
    print(f"Centrality metrics saved to {output_filename}")

if __name__ == "__main__":
    main()
