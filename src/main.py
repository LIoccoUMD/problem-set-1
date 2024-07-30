
# Pull down the imdb_movies dataset here and save to /data as imdb_movies_2000to2022.prolific.json
# You will run this project from main.py, so need to set things up accordingly

import json
import os
import urllib.request
import analysis_network_centrality
import analysis_similar_actors_genre

DATA_URL = 'https://github.com/cbuntain/umd.inst414/blob/main/data/imdb_movies_2000to2022.prolific.json?raw=true'
DATA_PATH = 'data/imdb_movies_2000to2022.prolific.json'


def download_data(url, path):
    #Downloads the dataset from the specified URL to the given path
    if not os.path.exists('data'):
        os.makedirs('data')
    urllib.request.urlretrieve(url, path)


def load_data(path):
    # Loads the dataset from the given path
    with open(path, 'r') as file:
        data = [json.loads(line) for line in file]
    return data


def main():
    # Download and load the data
    download_data(DATA_URL, DATA_PATH)
    data = load_data(DATA_PATH)
    
    # Perform analysis
    analysis_network_centrality.perform_analysis(data)
    analysis_similar_actors_genre.perform_analysis(data)


if __name__ == "__main__":
    main()