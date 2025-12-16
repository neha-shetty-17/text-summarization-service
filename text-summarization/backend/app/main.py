# main.py - FastAPI app
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import insert, select

from app.db import SessionLocal
from app.models import logs, init_db
from app.schemas import SummarizeRequest, SummarizeResponse

# transformers
from transformers import pipeline

app = FastAPI(title="Text Summarization Service")

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize database
init_db()

# Load model
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

print("Loading summarization model... (this may take a moment)")
summarizer = pipeline(
    task="summarization",
    model=MODEL_NAME,
    tokenizer=MODEL_NAME,
    device=-1  # CPU
)
print("Model loaded successfully.")


@app.post("/summarize", response_model=SummarizeResponse)
def summarize(req: SummarizeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    start = time.time()

    # run summarizer
    result = summarizer(
        req.text,
        max_length=req.max_length,
        min_length=req.min_length,
        do_sample=False,
    )

    exec_time = time.time() - start
    summary_text = result[0]["summary_text"]

    # Save to DB
    db = SessionLocal()
    try:
        stmt = insert(logs).values(
            input_length=len(req.text),
            execution_time=exec_time,
            summary=summary_text,
            input_text=req.text
        )
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")
    finally:
        db.close()

    return SummarizeResponse(
        summary=summary_text,
        input_length=len(req.text),
        execution_time=exec_time
    )


@app.get("/history")
def get_history(limit: int = 50):
    db = SessionLocal()
    try:
        query = (
            select(
                logs.c.id,
                logs.c.timestamp,
                logs.c.input_length,
                logs.c.execution_time,
                logs.c.summary
            )
            .order_by(logs.c.id.desc())
            .limit(limit)
        )

        rows = db.execute(query).fetchall()

        return [
            {
                "id": r.id,
                "timestamp": r.timestamp,
                "input_length": r.input_length,
                "execution_time": r.execution_time,
                "summary": r.summary,
            }
            for r in rows
        ]
    finally:
        db.close()
