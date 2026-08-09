import re
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate


def get_video_id(url):
    patterns = [
        r"youtu\.be/([^?&]+)",
        r"youtube\.com/watch\?v=([^?&]+)",
        r"youtube\.com/shorts/([^?&]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")


def get_transcript(url):
    video_id = get_video_id(url)

    api = YouTubeTranscriptApi()
    languages = ["en", "hi"]
    transcript = api.fetch(video_id,languages)

    return " ".join(item.text for item in transcript)

t=get_transcript("https://www.youtube.com/shorts/xcimtu5jcWo")
print(t)