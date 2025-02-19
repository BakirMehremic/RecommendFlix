from typing import List

from fastapi import APIRouter, HTTPException
import recommender.recommender as recommender
import app.exceptions as exceptions
import app.dtos as dtos
from app.utils import format_movie_json, format_movie_json_list

recommender_router = APIRouter()

# some routes use post instead of get so they can have a body 
# because they will only be called from the .net api

@recommender_router.get("/movie/details/{title}", response_model = dtos.MovieDetails)
async def get_movie_details(title: str):
    try:
        pandas_json = recommender.get_movie_details(title).to_json()
        return format_movie_json(pandas_json)
    except exceptions.MovieNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    

@recommender_router.get("/movie/title/{title}", response_model=dtos.MovieName)
async def get_movie_title(title: str):
    try:
        title = recommender.get_movie_title(title)
        return {"title": title}
    except exceptions.MovieNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    

@recommender_router.get("/random", response_model = dtos.MovieDetails)
async def get_random_movie():
    pandas_json = recommender.get_random_movie().to_json()
    return format_movie_json(pandas_json)


@recommender_router.get("/random/{category}", response_model = dtos.MovieDetails)
async def get_random_movie_by_category(category: str):
    formated = category.capitalize()
    try:
        pandas_json = recommender.get_random_movie_by_genre(formated).to_json()
        return format_movie_json(pandas_json)
    except exceptions.IncorrectCategory as e:
        raise HTTPException(status_code=400, detail=e.message)


@recommender_router.post("/recommend", response_model = List[dtos.MovieDetails])
async def recommend_movie(req: dtos.RequestRecommendation):
    try:
        recommendations = recommender.get_recommendations_sorted(req.favourite_movie_index,
                                                                 req.exclude_indexes).to_json()
    except exceptions.MovieNotFoundException as e:
        raise HTTPException(status_code=400, detail=e.message)
    
    return format_movie_json_list(recommendations)
