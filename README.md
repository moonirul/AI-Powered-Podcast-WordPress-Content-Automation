# AI-Powered Podcast & WordPress Content Automation

An end-to-end automation system built with **n8n**, **FastAPI**, **OpenAI Whisper**, and **OpenAI GPT** to streamline podcast transcription and WordPress content repurposing. The workflow automatically generates marketing assets and stores them in Google Sheets and Google Drive for human review before publication.

---

## Features

### Podcast Automation

* Detects new podcast videos uploaded to Google Drive
* Extracts audio from video files
* Transcribes audio using OpenAI Whisper via a FastAPI backend
* Generates Episode Title, Show Notes, Blog Draft, social captions, Newsletter Copy, Quote Ideas, and Short-form Clip Timestamps
* Renames processed files with a `done_` prefix to prevent duplicate processing

### WordPress Blog Automation

* Detects newly published WordPress blog posts
* Pulls the blog title and content using the WordPress REST API
* Generates Facebook Caption, Instagram Caption, TikTok Talking-Head Prompt, Email Newsletter Blurb, Three Short Video Hooks, Three Quote Graphic Ideas, and One Soft Call-to-Action
* Saves generated content to Google Sheets and Google Drive
* Sends content via email for human review before publication

---

## Tech Stack

* Python 3.14+
* FastAPI
* Uvicorn
* Faster-Whisper
* OpenAI API
* n8n
* Docker
* FFmpeg
* Google Drive API
* Google Sheets API
* WordPress REST API
* uv (Python package manager)

---

## Project Structure

```
AI-Powered-Podcast-WordPress-Content-Automation/
├── .venv/
├── n8n-workflows/
│   ├── SLE Blog to Social Content Agent.json
│   └── Video to Audio to Transcript.json
├── whisper-server/
│   └── main.py
├── pyproject.toml
├── uv.lock
├── README.md
└── .gitignore
```

---

## Installation Using uv

### Prerequisites

Make sure you have the following installed:

* Python 3.14 or higher
* uv package manager
* FFmpeg
* Docker (for running n8n locally)

### Clone the Repository

```bash
git clone https://github.com/your-username/AI-Powered-Podcast-WordPress-Content-Automation.git
cd AI-Powered-Podcast-WordPress-Content-Automation
```

### Install Dependencies

Since this project uses **uv**, install all dependencies with:

```bash
uv sync
```

This will create the virtual environment and install all dependencies defined in `pyproject.toml`.

### Activate the Virtual Environment

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
source .venv/bin/activate
```

### Run the FastAPI Whisper Server

From the project root directory, run:

```bash
uv run --directory whisper-server uvicorn main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

## Dependencies

The project dependencies are managed through `pyproject.toml`:

```toml
[project]
requires-python = ">=3.14"
dependencies = [
    "fastapi>=0.139.0",
    "faster-whisper>=1.2.1",
    "python-multipart>=0.0.32",
    "uvicorn>=0.51.0",
]
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_DRIVE_CREDENTIALS=path_to_credentials.json
GOOGLE_SHEETS_CREDENTIALS=path_to_credentials.json
```

---

## Google Cloud Setup

To use Google Drive and Google Sheets integrations, ensure that:

1. A Google Cloud project is created.
2. Google Drive API is enabled.
3. Google Sheets API is enabled.
4. OAuth2 or Service Account credentials are generated.
5. The credentials are configured in n8n.

---

## Running n8n with Docker

Start n8n locally using Docker:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  docker.n8n.io/n8nio/n8n
```

Then open:

```
http://localhost:5678
```

Import the workflow files from the `n8n-workflows/` folder.

---

## Workflow Overview

### Podcast Workflow

```
Google Drive Video
        ↓
Extract Audio
        ↓
Whisper Transcription
        ↓
OpenAI Content Generation
        ↓
Google Sheets / Google Drive
        ↓
Email Review
```

### WordPress Workflow

```
New WordPress Blog Post
        ↓
Fetch Title & Content
        ↓
OpenAI Brand Voice Content Generation
        ↓
Google Sheets / Google Drive
        ↓
Email Review
```

---

## Duplicate Protection

After a podcast video is successfully processed, the original file is renamed by adding the `done_` prefix.

Example:

```
SLE SNF POD.mp4 → done_SLE SNF POD.mp4
```

On future scheduled runs, any file starting with `done_` is skipped, preventing duplicate transcription and content generation.

---

## Review Process

All generated content is sent for **human review** before any public publication. The workflow does not automatically publish content to social media or WordPress.

---

## License

This project is provided for educational and portfolio purposes. Feel free to adapt it for your own automation workflows.

---

## Author

**Md. Monirul Islam**

AI Automation Engineer | Python Developer | n8n Workflow Specialist
