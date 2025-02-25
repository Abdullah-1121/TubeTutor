from crewai import Crew , Agent , Task , LLM
from crewai.tools import BaseTool
from youtube_transcript_api import YouTubeTranscriptApi
# Defining the Custom tool we will be using to get the content from a youtube video
class Transcript_getter(BaseTool):
    name: str ="Transcript_getter"
    description: str = ("Fetches the transcript of the Youtube Videos")

    def _run(self, video_id: str) -> str:
      transcript = YouTubeTranscriptApi.get_transcript(video_id)
      for entry in transcript:
          return entry['text']
