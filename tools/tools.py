# from langchain_community.tools.tavily_search import TavilySearchResults
import os

from langchain_community.tools import TavilySearchResults
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()

def get_linkedin_profile_url_tavily(name: str):
    """Searches for LinkedIn or Twitter Profile Page."""
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res

def get_linkedin_profile_url_serp(name: str):
    """Searches for LinkedIn Profile Page."""
    params = {
        "api_key": f'{os.environ.get("SERPAPI_API_KEY")}',
        "engine": "google",
        "q": f"{name} linkedin",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    formatted_results = [
        {
            "title": result["title"],
            "url": result["link"],
            "content": result["snippet"]
        } for result in results["organic_results"] if "linkedin.com" in result["link"].lower()
    ]
    return formatted_results

def get_bluesky_profile_url(name: str):
    """Searches for BlueSky Profile Page."""
    params = {
        "api_key": f'{os.environ.get("SERPAPI_API_KEY")}',
        "engine": "google",
        "q": f"{name} bluesky profile",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    formatted_results = [
        {
            "title": result["title"],
            "url": result["link"],
            "content": result["snippet"]
        } for result in results["organic_results"] if "bsky" in result["link"].lower()
    ]

    return formatted_results
