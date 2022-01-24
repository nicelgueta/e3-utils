import time
import os
from typing import Generator
import requests
import loguru

REDDIT_RATE_LIMIT = 2 # seconds
MAX_QUERY_LENGTH = 512
MAX_LISTING_LIMIT = 100
BASE_URL = "https://reddit.com"


class RedditWrapper:
    """
    Wrapper for very basic search API interaction
    """

    user_agent=f"Ubuntu(20.04):test-app:v0.1"
    
    def generate_searches(
        self, 
        search_term: str,
        subreddit: str = None,
        period: str = None,
        limit: int = None,
        sort: str = None
    ) -> Generator[dict, None, None]:
        """
        Generate a stream of 
        [listing](https://www.reddit.com/dev/api#listings) objects
        that match a given search term.

        Each time next() is called on the generator returned from
        this method, this componenta will search for an updated list
        of listings. If there is no update then the same list as before is 
        returned.
        """
        #defaults - not in func args to allow for defaultdict in sse
        period = "hour" if not period else period
        limit = 5 if not limit else limit
        sort = "new" if not sort else sort

        subredlnk = f"r/{subreddit}" if subreddit else ""
        url = f"{BASE_URL}/{subredlnk}/search.json"
        q = search_term
        if len(search_term) > MAX_QUERY_LENGTH:
            raise ValueError(
                f"Search term is too long - reduce to {MAX_QUERY_LENGTH}"
                " characters."
            )
        t = period
        limit = limit
        headers = {"User-Agent": self.user_agent}
        params = {
            "q": q,
            "t": t,
            "limit": limit,
            "sort": sort
        }
        last_called_time = time.time()
        while True:
            while time.time() - last_called_time < REDDIT_RATE_LIMIT:
                time.sleep(REDDIT_RATE_LIMIT - (time.time() - last_called_time))
            last_called_time = time.time()
            r = requests.get(
                url,
                headers=headers,
                params=params
            )
            api_ret = r.json()
            
            yield api_ret['data']['children']