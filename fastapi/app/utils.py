import json
from typing import List
from app import dtos


# used because padas df.to_json() returns a weirdly formatted json string

def format_movie_json_list(pandas_json_str: str) -> List[dtos.MovieDetails]:
    data = json.loads(pandas_json_str)

    row_ids = list(data["index"].keys())
    movies = []
    
    for row_id in row_ids:
        movie_dict = {
            "index": data["index"].get(row_id),
            "Movie_Title": data["Movie_Title"].get(row_id),
            "Year": data["Year"].get(row_id),
            "Director": data["Director"].get(row_id),
            "Actors": data["Actors"].get(row_id),
            "Rating": data["Rating"].get(row_id),
            "Runtime_Mins": data["Runtime(Mins)"].get(row_id),
            "Censor": data["Censor"].get(row_id),
            "Total_Gross": data["Total_Gross"].get(row_id),
            "main_genre": data["main_genre"].get(row_id),
            "side_genre": data["side_genre"].get(row_id),
        }
        movie = dtos.MovieDetails(**movie_dict)
        movies.append(movie)
    return movies

def format_movie_json(pandas_json_str: str) -> dtos.MovieDetails:
    data = json.loads(pandas_json_str)

    row_ids = list(data["index"].keys())

    row_id = row_ids[0]
    
    movie_dict = {
        "index": data["index"].get(row_id),
        "Movie_Title": data["Movie_Title"].get(row_id),
        "Year": data["Year"].get(row_id),
        "Director": data["Director"].get(row_id),
        "Actors": data["Actors"].get(row_id),
        "Rating": data["Rating"].get(row_id),
        "Runtime_Mins": data["Runtime(Mins)"].get(row_id),
        "Censor": data["Censor"].get(row_id),
        "Total_Gross": data["Total_Gross"].get(row_id),
        "main_genre": data["main_genre"].get(row_id),
        "side_genre": data["side_genre"].get(row_id),
    }
    
    movie = dtos.MovieDetails(**movie_dict)
    return movie