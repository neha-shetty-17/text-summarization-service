# models.py - Database models
from sqlalchemy import Table, Column, Integer, Float, DateTime, Text, MetaData
from sqlalchemy.sql import func
from app.db import engine

# Create metadata object
metadata = MetaData()

# Define the logs table
logs = Table(
    "logs",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("timestamp", DateTime, server_default=func.now()),
    Column("input_length", Integer),
    Column("execution_time", Float),
    Column("summary", Text),
    Column("input_text", Text),
)


def init_db():
    """Initialize the database by creating all tables."""
    metadata.create_all(engine)
