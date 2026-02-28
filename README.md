
# AI Video Attendee Extractor 

An automated tool that uses **Gemini 2.5 Flash** to extract structured attendee data (Names and Dates) directly from check-in video files.

## Features
- **Multimodal Extraction**: Processes `.webm` and `.mp4` files using the Google GenAI Files API.
- **Structured Output**: Uses Pydantic for guaranteed JSON formatting.
- **Resilient Logic**: Implements exponential backoff to handle 429 Rate Limits automatically.

## Setup Instructions

### 1. Prerequisites
- Python 3.11+
- A Google Gemini API Key from [AI Studio](https://aistudio.google.com/)

### 2. Installation
```bash
git clone [https://github.com/your-username/video-extraction-ai.git](https://github.com/your-username/video-extraction-ai.git)
cd video-extraction-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
