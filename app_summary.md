# Call Quality Agent Application Summary

The **Call Quality Agent** is a Sales Call Quality Assurance (QA) pipeline built primarily with Python and FastAPI. Its purpose is to process sales call recordings, transcribe them, clean the text, analyze the conversation for quality and compliance using an LLM, and finally generate structured reports (JSON and HTML).

## How the Application Works (Pipeline Workflow)

1. **Transcription (`src/transcribe.py`)**
   - The system takes audio recordings and transcribes them using Google Cloud Speech-to-Text (STT).
   - This generates a raw, diarized transcript (identifying different speakers).
2. **Transcript Cleaning (`src/clean.py`)**
   - The raw transcript (which can be in JSON, plain text, SRT, or VTT format) is processed.
   - It normalizes speaker tags to standard roles like `SALES_REP` and `CUSTOMER`.
   - It applies phonetic spelling corrections (e.g., for difficult-to-transcribe institute names) using `config/corrections.json`.
   - It strips zero-content filler words (e.g., "um", "uh") to improve the LLM's understanding.
3. **Analysis & Assessment (FastAPI / OpenRouter)**
   - The cleaned transcript is evaluated against specific sales guidelines and course data.
   - It utilizes an LLM via OpenRouter (prompted by `config/analysis_prompt.md`) to evaluate sales pitch coverage, compliance, and objection handling.
   - The LLM detects incidents (e.g., misselling, compliance violations) based on criteria defined in `config/incident_levels.md` and the `incident-definition/` directory.
4. **Reporting (`src/report_html.py`)**
   - The analysis results are compiled into a structured JSON QA report.
   - An HTML report is then generated, presenting a beautiful UI with call statistics, talk ratios, incident summaries, a QA checklist, sales intelligence metrics, and an overall call score.
5. **Data Persistence (`src/api/db.py`)**
   - Analysis results, pipeline job statuses, and metadata are persisted in a local SQLite database (`db/call_quality.db`).

---

## File Structure

```text
sales-quality-agent-app/
├── config/
│   ├── analysis_prompt.md      # The LLM prompt instructions for analyzing transcripts
│   ├── corrections.json        # Dictionary of transcript corrections & filler words
│   └── incident_levels.md      # Definitions of incident severity levels (L1, L2, L3)
├── data/
│   ├── input/                  # Folder for input audio or transcript files
│   └── output/                 # Destination for processed data and intermediate files
├── db/
│   └── call_quality.db         # SQLite database storing pipeline states and metrics
├── src/                        # Core Python source code
│   ├── api/                    # FastAPI web application
│   │   ├── main.py             # Entry point (initializes FastAPI, mounts routers)
│   │   ├── db.py               # Database initialization and connection logic
│   │   ├── models/             # Pydantic/SQLAlchemy data models
│   │   ├── routes/             # API endpoints (analyze, clean, pipeline, report, stt)
│   │   └── services/           # Business logic and external service integrations
│   ├── clean.py                # Script to sanitize and format diarized transcripts
│   ├── report_html.py          # Script to generate HTML dashboards from JSON reports
│   └── transcribe.py           # Script to run Google Cloud STT on audio files
├── .env                        # Environment variables (API keys, DB URLs)
├── requirements.txt            # Python dependencies (FastAPI, uvicorn, etc.)
```

## Key Technologies Used
- **Backend Framework**: FastAPI
- **Database**: SQLite
- **Transcription**: Google Cloud Speech-to-Text
- **AI/LLM**: OpenRouter (for analyzing sales transcripts)
- **Frontend / Reporting**: Vanilla HTML/CSS generation via Python scripts
