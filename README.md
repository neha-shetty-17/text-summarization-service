# Text Summarization Service (FastAPI + React)

This repository implements the Case Study: Text Summarization Service (backend + frontend).
Spec: uses a small Hugging Face summarization model locally, logs usage to SQLite, provides a React UI. (Spec uploaded by user.) :contentReference[oaicite:1]{index=1}

## Option A — Run locally (recommended for development)

### Backend
1. cd backend
2. Activate virtual environment:
   - Windows: `.\app\venv\Scripts\Activate.ps1`
   - Mac/Linux: `source app/venv/bin/activate`
3. Install dependencies (if needed): `pip install -r app/requirements.txt`
4. Start server: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Open http://localhost:8000/docs in your browser
   - The first run will download the HF model (may take 2-5 minutes depending on internet).
   
**For detailed instructions, see [HOW_TO_RUN.md](HOW_TO_RUN.md)**

### Frontend
1. cd frontend
2. npm install
3. npm start
4. Open http://localhost:3000

## Option B — Docker (recommended to replicate environment)
From the repository root:
1. docker-compose up --build
2. Open http://localhost:3000
   - Backend will be available at http://localhost:8000

## Endpoints

- POST /summarize
  - Body JSON: { "text": "...", "max_length": 60, "min_length": 10 }
  - Returns: { "summary": "...", "input_length": N, "execution_time": t }

- GET /history?limit=20
  - Returns recent summarization logs.

## Notes
- Model: `sshleifer/distilbart-cnn-12-6` (small summarization model).
- DB: SQLite file `summaries.db` created automatically in backend folder.
- To change model or use GPU, update `main.py` and install appropriate CUDA-enabled torch.

