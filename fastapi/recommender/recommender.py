import os
from typing import List
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import difflib
from sklearn.metrics.pairwise import cosine_similarity
import app.exceptions as exceptions

# imdb top 5000 dataset
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "dataset.csv"))

# add index column
df = df.reset_index()

# combine data into all_features
all_features = df.apply(lambda row: ' '.join(row.values.astype(str)), axis=1)

# convert data to feature vectors
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(all_features)

# get similarity scores for all movies
similarity = cosine_similarity(feature_vectors)

def get_movie_details(name: str) ->pd.Series:
  list_of_all_titles = df["Movie_Title"].tolist()
  find_close_match = difflib.get_close_matches(name, list_of_all_titles)

  if len(find_close_match)==0:
    raise exceptions.MovieNotFoundException(f"No movie found for input {name}")
  
  movie_title = find_close_match[0]

  # return the df row related to the movie
  movie_details = df[df["Movie_Title"] == movie_title]
  return movie_details # use movie_details.values[0] to get title


def get_movie_title(name: str) ->str:
  list_of_all_titles = df["Movie_Title"].tolist()
  find_close_match = difflib.get_close_matches(name, list_of_all_titles)

  if len(find_close_match)==0:
    raise exceptions.MovieNotFoundException(f"No movie found for input {name}")
  
  movie_title = find_close_match[0]

  print("fav movie --- " + movie_title)

  return movie_title


def get_recommendations_v1(movie_title: str) ->list:
  index = df[df.Movie_Title == movie_title]["index"].values[0]

  similar_movies =list(enumerate(similarity[index]))  
  sorted_similar_movies = sorted(similar_movies, key = lambda x:x[1], reverse = True) 
  sorted_similar_movies=sorted_similar_movies[:10]

  # tuples in sorted_similar_movies have (index, similarity score)
  for i in sorted_similar_movies:
    index=i[0]
    title_from_index = df[df.index==index]["Movie_Title"].values[0]
    print(title_from_index)
  print(type(sorted_similar_movies))

  return sorted_similar_movies
  

def get_recommendations_sorted(movie_index: int, exclude: List[int]) -> pd.DataFrame:
    filtered = df[df["index"] == movie_index]
    if filtered.empty:
        raise exceptions.MovieNotFoundException(f"Movie with index '{movie_index}' not found")
    
    movie_index = filtered["index"].values[0]
    similar_movies = list(enumerate(similarity[movie_index]))
    sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)[1:]

    filtered_recommendations = [t for t in sorted_similar_movies if t[0] not in exclude]
    
    recommended_tuples = filtered_recommendations[:10]
    recommended_indexes = [i[0] for i in recommended_tuples]
    recommended_df = df[df.index.isin(recommended_indexes)]
    recommended_df = recommended_df.set_index("index").loc[recommended_indexes].reset_index()
    return recommended_df


def get_recommendtations_w_exclude(movie_title:str,
                                    exclude_indexes: List[str]) -> List[str]:
  pass



def get_random_movie() ->pd.Series:
  return df.sample(n=1)


def get_random_movie_by_genre(genre: str) ->pd.Series:
    filtered_df = df[df['main_genre'] == genre]

    if filtered_df.empty:
      raise exceptions.IncorrectCategory(f"No movies under category -{genre}")

    return filtered_df.sample(n=1)

#get_recommendations_sorted(get_movie_details("wolf of wall street")["Movie_Title"].values[0])