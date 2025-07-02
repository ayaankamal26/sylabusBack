from sqlmodel import SQLModel, create_engine, Session
import os

engine = create_engine("sqlite:///./app.db")

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
