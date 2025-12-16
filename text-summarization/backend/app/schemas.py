# schemas.py - Pydantic schemas for request/response validation
from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    text: str = Field(..., description="Text to summarize")
    max_length: int = Field(default=60, ge=10, le=200, description="Maximum length of summary")
    min_length: int = Field(default=10, ge=5, le=100, description="Minimum length of summary")


class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="Generated summary")
    input_length: int = Field(..., description="Length of input text")
    execution_time: float = Field(..., description="Time taken to generate summary in seconds")
