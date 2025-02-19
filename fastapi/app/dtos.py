from pydantic import BaseModel
from typing import List


class MovieName(BaseModel):
    title: str 


class RequestRecommendation(BaseModel):
    favourite_movie_index: int
    exclude_indexes: List[int]


class MovieDetails(BaseModel):
    index: int
    Movie_Title: str
    Year: int
    Director: str
    Actors: str
    Rating: float
    Runtime_Mins: int
    Censor: str
    Total_Gross: str
    main_genre: str
    side_genre: str

class Genre(BaseModel):
    genre: str

class RecommendResponse(BaseModel):
    recommendations: List[MovieDetails]

