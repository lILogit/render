from fastapi import FastAPI, HTTPException, Query
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional

app = FastAPI(title="YouTube Subtitle API", description="An API to download subtitles from YouTube videos.")


def get_video_id(url: str) -> str:
    """Extract video ID from YouTube URL."""
    if 'youtu.be' in url:
        return url.split('/')[-1]
    elif 'youtube.com' in url:
        return url.split('v=')[1].split('&')[0]
    else:
        return url  # Assume it's already a video ID


@app.get("/subtitles")
async def get_subtitles(
        video_url: str = Query(..., description="YouTube video URL"),
        language: str = Query("en", description="Language code for subtitles (e.g., en, es)"),
):
    """Download subtitles for a given YouTube video URL."""
    try:
        video_id = get_video_id(video_url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        if not transcript:
            raise HTTPException(
                status_code=404, detail="Subtitles not found for this video or language.")
        return transcript
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download subtitles: {str(e)}")

