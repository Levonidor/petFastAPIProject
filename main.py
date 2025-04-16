import uvicorn
from fastapi import FastAPI
from models import models
from database.database import engine, SessionLocal
from routers.quiz_routers import router as quiz_router

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(quiz_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, workers=3)