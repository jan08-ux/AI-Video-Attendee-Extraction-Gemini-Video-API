import time
import os
from pydantic import BaseModel, Field
from google import genai
from google.genai import types, errors

# 1. Define Structured Output Schema
class Attendee(BaseModel):
    name: str = Field(description="Full name of the attendee")
    date: str = Field(description="Check-in date in dd/mm/yyyy format")

class AttendeeList(BaseModel):
    attendees: list[Attendee]

# 2. Configuration
# Note: Use 'gemini-2.5-flash' for the best balance of speed and quota in 2026.
MODEL_ID = "gemini-2.5-flash" 
VIDEO_FILE = "attendee_checkin_23f3003756.webm"
API_KEY = "AIzaSyB97ZwHTA51u0w0x-sksitu04Iy84kjYDw"

client = genai.Client(api_key=API_KEY)

def extract_attendees():
    print(f"--- Step 1: Uploading {VIDEO_FILE} ---")
    video_upload = client.files.upload(file=VIDEO_FILE)
    
    # Wait for Google to process the video frames
    while video_upload.state.name == "PROCESSING":
        print("Processing video frames...", end="\r")
        time.sleep(3)
        video_upload = client.files.get(name=video_upload.name)

    if video_upload.state.name == "FAILED":
        raise ValueError("Video processing failed.")

    print(f"\n--- Step 2: Analyzing with {MODEL_ID} ---")

    # Retry Logic for 429 Resource Exhausted
    max_retries = 3
    retry_delay = 30  # Start with 30 seconds

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=MODEL_ID,
                contents=[
                    video_upload,
                    "Extract the list of 20 attendees. Return only JSON matching the schema."
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AttendeeList,
                    temperature=0.1,
                ),
            )
            
            print("--- Extraction Successful ---")
            print(response.text)
            break # Exit loop on success

        except errors.ClientError as e:
            if "429" in str(e):
                print(f"\n[QUOTA EXCEEDED] Attempt {attempt + 1}/{max_retries}")
                print(f"Waiting {retry_delay} seconds before retrying...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"An error occurred: {e}")
                break
        finally:
            # Clean up the file from Google Cloud storage
            if attempt == max_retries - 1 or 'response' in locals():
                client.files.delete(name=video_upload.name)
                print("--- Cleaned up temporary files ---")

if __name__ == "__main__":
    extract_attendees()