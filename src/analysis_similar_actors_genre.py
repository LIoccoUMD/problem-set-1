"""
PART 2: SIMILAR ACTORS BY GENRE
Using the imdb_movies dataset:
- Create a data frame, where each row corresponds to an actor, each column represents a genre, and each cell captures how many times that row's actor has appeared in that column’s genre 
- Using this data frame as your “feature matrix”, select an actor (called your “query”) for whom you want to find the top 10 most similar actors based on the genres in which they’ve starred 
- - As an example, select the row from your data frame associated with Chris Hemsworth, actor ID “nm1165110”, as your “query” actor
- Use sklearn.metrics.DistanceMetric to calculate the euclidean distances between your query actor and all other actors based on their genre appearances
- - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.DistanceMetric.html
- Output a CSV containing the top ten actors most similar to your query actor using cosine distance 
- - Name it 'similar_actors_genre_{current_datetime}.csv' to `/data`
- - For example, the top 10 for Chris Hemsworth are:  
        nm1165110 Chris Hemsworth
        nm0000129 Tom Cruise
        nm0147147 Henry Cavill
        nm0829032 Ray Stevenson
        nm5899377 Tiger Shroff
        nm1679372 Sudeep
        nm0003244 Jordi Mollà
        nm0636280 Richard Norton
        nm0607884 Mark Mortimer
        nm2018237 Taylor Kitsch
- Describe in a print() statement how this list changes based on Euclidean distance
- Make sure your code is in line with the standards we're using in this class
"""

import pandas as pd
from sklearn.metrics import DistanceMetric
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime


def create_feature_matrix(data):
    # Creates a feature matrix where each row is an actor and each column is a genre."""
    actor_genre_dict = {}
    all_genres = set()

    # First pass to collect all genres
    for movie in data:
        for genre in movie['genres']:
            all_genres.add(genre)
    
    for movie in data:
        genres = movie['genres']
        for actor_id, actor_name in movie['actors']:
            if actor_name not in actor_genre_dict:
                actor_genre_dict[actor_name] = {genre: 0 for genre in all_genres}
            for genre in genres:
                actor_genre_dict[actor_name][genre] += 1
    
    feature_matrix = pd.DataFrame.from_dict(actor_genre_dict, orient='index').fillna(0)
    return feature_matrix


def find_similar_actors(feature_matrix, query_actor):
    # Finds the top 10 actors most similar to the query actor based on genre appearances
    query_vector = feature_matrix.loc[query_actor].values.reshape(1, -1)
    cosine_similarities = cosine_similarity(feature_matrix, query_vector).flatten()
    similarity_scores = pd.Series(cosine_similarities, index=feature_matrix.index)
    top_10_similar = similarity_scores.sort_values(ascending=False).head(10)
    
    return top_10_similar


def save_to_csv(similar_actors, query_actor):
    # Saves the similar actors to a CSV file
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    similar_actors.to_csv(f'data/similar_actors_genre_{query_actor}_{current_datetime}.csv', header=False)


def perform_analysis(data):
    # Performs the similar actors by genre analysis
    feature_matrix = create_feature_matrix(data)
    query_actor = 'Liam Hemsworth'
    
    similar_actors = find_similar_actors(feature_matrix, query_actor)
    
    print(f"Top 10 actors most similar to {query_actor} based on genre appearances:")
    print(similar_actors)
    
    save_to_csv(similar_actors, query_actor)
    
    # Additional print statement for Euclidean distance (if needed)
    dist = DistanceMetric.get_metric('euclidean')
    euclidean_distances = dist.pairwise(feature_matrix)
    euclidean_distances_df = pd.DataFrame(euclidean_distances, index=feature_matrix.index, columns=feature_matrix.index)
    top_10_euclidean = euclidean_distances_df.loc[query_actor].sort_values().head(10)
    
    print(f"Top 10 actors most similar to {query_actor} based on Euclidean distance:")
    print(top_10_euclidean)
