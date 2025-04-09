import os
import re
from langchain_tavily import TavilySearch
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
os.environ['TAVILY_API_KEY'] = os.getenv("TAVILY_API_KEY")
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

def get_llm():
    try:
        return ChatGroq(
            temperature=0.7,
            model="gemma2-9b-it"
        )
    except Exception as e:
        raise Exception(f"Failed to initialize AI model: {str(e)}")

def get_embed_code(video_url):
    video_id = re.search(r"v=([^&]+)", video_url)
    if video_id:
        # return f'<iframe width="360" height="315" src="https://www.youtube.com/embed/{video_id.group(1)}" frameborder="0" allowfullscreen></iframe>'
        return video_id.group(1)
    return None

def is_youtube_url(url: str) -> bool:
    youtube_patterns = [
        r'^https?://(www\.)?youtube\.com/watch\?v=.+',
        r'^https?://youtu\.be/.+'
    ]
    
    return any(re.match(pattern, url) for pattern in youtube_patterns)

def get_youtube_urls(query="machine learning"):
    tool = TavilySearch(max_results=50)
    response = tool.invoke({'query': f"give me links of {query} videos in youtube. you must provide only youtube urls. url format: https://www.youtube.com/"})
    youtube_urls = []
    for i in response["results"]:
        if is_youtube_url(i['url']):
            youtube_urls.append(i['url'])
    return youtube_urls

def embed_codes(urls):
    return [get_embed_code(url) for url in urls]

def chat(query="hello"):
    llm = ChatGroq(model="gemma2-9b-it")
    return llm.invoke(query).content