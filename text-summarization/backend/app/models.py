# models.py - SQLAlchemy models
from sqlalchemy import Table, Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from .db import metadata, engine

logs = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("timestamp", DateTime(timezone=True), server_default=func.datetime('now')),
    Column("input_length", Integer),
    Column("execution_time", Float),
    Column("summary", Text),
    Column("input_text", Text)
)

def init_db():
    metadata.create_all(bind=engine)
