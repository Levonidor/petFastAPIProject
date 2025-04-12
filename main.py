from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post("/questions/", tags=["Questions"])
async def create_question(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id,
        )
        db.add(db_choice)
    db.commit()
    return f"Question was successfully created!"


@app.get("/questions/{question_id}", tags=["Questions"])
async def get_question(question_id: int, db: db_dependency):
    result = (
        db.query(models.Questions).filter(models.Questions.id == question_id).first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")
    return result


@app.get("/choices/{question_id}", tags=["Choices"])
async def get_question_choices(question_id: int, db: db_dependency):
    result = (
        db.query(models.Choices).filter(models.Choices.question_id == question_id).all()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Question is not found")
    return result


@app.delete("/choices/{choice_id}", tags=["Choices"])
async def delete_choice(choice_id: int, db: db_dependency):
    db.query(models.Choices).filter(models.Choices.id == choice_id).delete()
    db.commit()
    return f"Choice with id: {choice_id} was successfully deleted!"


@app.put("/choices/{choice_id}", tags=["Choices"])
async def update_choice(
    text: str = None,
    is_correct: bool = None,
    choice_id: int = None,
    db: db_dependency = None,
):
    choice = db.query(models.Choices).filter(models.Choices.id == choice_id).first()
    if text != None:
        choice.choice_text = text
    if is_correct != None:
        choice.is_correct = is_correct
    db.add(choice)
    db.commit()
    db.refresh(choice)

@app.post("/choices/{question_id}", tags = ["Choices"])
async def create_choice(question_id: int, choice: ChoiceBase, db: db_dependency):
    db_choice = models.Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=question_id,
    )
    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)
    return f"Choice was successfully added to Question with id: {question_id}!"