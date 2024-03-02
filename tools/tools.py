
from langchain.serpapi import SerpAPIWrapper

def get_profile_url(text: str) -> str:
    """
    Search for linkedin profile Page.
    """
    # here we use the SerpApi that is a google search api to get the linkedin profile page.
    # we can use the google search api to get the linkedin profile page.
    search = SerpAPIWrapper()
    search_results = search.run(f"{text}")

    return search_results