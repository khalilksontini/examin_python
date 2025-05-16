import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from database import SessionLocal, engine
import models, schemas

from llm import generate_with_tinyllama  # ta fonction TinyLlama

# Charger les variables d'environnement depuis .env
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/movies/", response_model=schemas.MoviePublic)
def create_movie(movie: schemas.MovieBase, db: Session = Depends(get_db)):
    db_movie = models.Movie(
        title=movie.title,
        year=movie.year,
        director=movie.director
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    for actor_data in movie.actors:
        db_actor = models.Actor(
            actor_name=actor_data.actor_name,
            movie_id=db_movie.id
        )
        db.add(db_actor)

    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/random/", response_model=schemas.MoviePublic)
def get_random_movie(db: Session = Depends(get_db)):
    movie = db.query(models.Movie).options(joinedload(models.Movie.actors)).order_by(func.random()).first()
    if not movie:
        raise HTTPException(status_code=404, detail="No movies found")
    return movie

@app.post("/generate_summary/", response_model=schemas.SummaryResponse)
def generate_summary(request: schemas.SummaryRequest, db: Session = Depends(get_db)):
    movie = (
        db.query(models.Movie)
        .options(joinedload(models.Movie.actors))
        .filter(models.Movie.id == request.movie_id)
        .first()
    )
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    actor_names = ", ".join(actor.actor_name for actor in movie.actors)

    prompt = (
        f"Generate a short, engaging summary for the movie '{movie.title}' ({movie.year}), "
        f"directed by {movie.director} and starring {actor_names}."
    )

    # Utiliser TinyLlama local
    summary_text = generate_with_tinyllama(prompt, max_length=150)

    return schemas.SummaryResponse(summary_text=summary_text)
