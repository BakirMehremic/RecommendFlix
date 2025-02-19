from fastapi import FastAPI
from app.controller import recommender_router
app = FastAPI()

app.include_router(recommender_router)