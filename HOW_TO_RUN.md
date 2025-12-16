# How to Run the Text Summarization Project

This guide provides step-by-step instructions to run the Text Summarization Service.

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Internet connection (for downloading the ML model on first run)
- Web browser (Chrome, Firefox, Edge, etc.)

## 🚀 Quick Start (Recommended)

### Option 1: Run Backend Only (Fastest)

1. **Navigate to the backend directory:**
   ```bash
   cd text-summarization/backend
   ```

2. **Activate the virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     .\app\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```cmd
     app\venv\Scripts\activate.bat
     ```
   - **Mac/Linux:**
     ```bash
     source app/venv/bin/activate
     ```

3. **Install/Update dependencies (if needed):**
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Start the server:**
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

5. **Wait for the model to load:**
   - First run: 2-5 minutes (downloads model from Hugging Face)
   - Subsequent runs: 30-60 seconds

6. **Open in browser:**
   - Go to: **http://localhost:8000/docs**
   - You'll see the interactive API documentation

### Option 2: Run with Docker (Recommended for Production)

1. **Navigate to project root:**
   ```bash
   cd text-summarization
   ```

2. **Build and start containers:**
   ```bash
   docker-compose up --build
   ```

3. **Wait for services to start:**
   - Backend: http://localhost:8000/docs
   - Frontend: http://localhost:3000 (if frontend is configured)

4. **To stop:**
   ```bash
   docker-compose down
   ```

## 📖 How to Use the API

### Using the Interactive Documentation (Easiest)

1. **Open:** http://localhost:8000/docs

2. **Test POST /summarize:**
   - Click on **POST /summarize**
   - Click **"Try it out"**
   - Enter your text in the Request body:
     ```json
     {
       "text": "Your text to summarize here. It can be as long as you want.",
       "max_length": 60,
       "min_length": 10
     }
     ```
   - Click **"Execute"**
   - See the summary in the Response body below

3. **Test GET /history:**
   - Click on **GET /history**
   - Click **"Try it out"**
   - (Optional) Set `limit` parameter (default: 50)
   - Click **"Execute"**
   - See all your past summaries

### Using Command Line (PowerShell)

**Test Summarize Endpoint:**
```powershell
$body = @{
    text = "Your text to summarize here"
    max_length = 60
    min_length = 10
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/summarize" -Method Post -Body $body -ContentType "application/json"
```

**Test History Endpoint:**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/history" -Method Get
```

### Using curl

**Test Summarize:**
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "max_length": 60, "min_length": 10}'
```

**Test History:**
```bash
curl "http://localhost:8000/history?limit=10"
```

## 📝 API Endpoints

### POST /summarize
Summarize text using AI model.

**Request Body:**
```json
{
  "text": "string (required)",
  "max_length": 60 (optional, 10-200),
  "min_length": 10 (optional, 5-100)
}
```

**Response:**
```json
{
  "summary": "Generated summary text",
  "input_length": 150,
  "execution_time": 2.5
}
```

### GET /history
Get all past summarization requests.

**Query Parameters:**
- `limit` (optional): Number of records to return (default: 50)

**Response:**
```json
[
  {
    "id": 1,
    "timestamp": "2024-01-15T10:30:00",
    "input_length": 150,
    "execution_time": 2.5,
    "summary": "Summary text here"
  }
]
```

## 🔧 Troubleshooting

### Server won't start

1. **Check if port 8000 is already in use:**
   ```powershell
   netstat -ano | findstr :8000
   ```
   If something is using it, either stop that process or change the port:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```

2. **Check Python version:**
   ```bash
   python --version
   ```
   Should be 3.11 or higher.

3. **Reinstall dependencies:**
   ```bash
   pip install --upgrade -r app/requirements.txt
   ```

### "Connection refused" error

- Wait 1-2 minutes after starting (model is loading)
- Check if server process is running
- Verify you're using the correct URL: http://localhost:8000/docs

### Model loading takes too long

- First run always takes 2-5 minutes (downloading ~200MB model)
- Subsequent runs are faster (30-60 seconds)
- Ensure stable internet connection

### Import errors

- Make sure you're in the correct directory
- Activate the virtual environment
- Reinstall requirements: `pip install -r app/requirements.txt`

## 📁 Project Structure

```
text-summarization/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI application
│   │   ├── db.py            # Database connection
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── requirements.txt # Python dependencies
│   ├── Dockerfile           # Docker configuration
│   └── summaries.db        # SQLite database (auto-created)
├── frontend/                # React frontend (if configured)
├── docker-compose.yml       # Docker Compose configuration
└── README.md               # Project overview
```

## 🎯 Quick Test Examples

### Example 1: Summarize a paragraph
```json
{
  "text": "Artificial intelligence is revolutionizing technology. Machine learning algorithms process vast amounts of data. This technology is used in healthcare, finance, and transportation.",
  "max_length": 30,
  "min_length": 15
}
```

### Example 2: Summarize news article
```json
{
  "text": "Scientists discovered a new planet in the habitable zone. The planet has water vapor and oxygen in its atmosphere. Researchers used advanced telescopes for detection.",
  "max_length": 40,
  "min_length": 20
}
```

## ✅ Verification Checklist

- [ ] Server starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] POST /summarize returns a summary
- [ ] GET /history returns past summaries
- [ ] Database file (summaries.db) is created

## 🆘 Need Help?

1. Check the server logs for error messages
2. Verify all dependencies are installed
3. Ensure Python version is 3.11+
4. Check firewall/antivirus isn't blocking port 8000

## 📌 Important Notes

- **First run:** Model download takes 2-5 minutes
- **Database:** Created automatically in `backend/summaries.db`
- **Port:** Default is 8000, change if needed
- **Model:** Uses `sshleifer/distilbart-cnn-12-6` from Hugging Face



