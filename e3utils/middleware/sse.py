import json
from ..cnxns.reddit import RedditWrapper
from typing import Generator
from fastapi import Request
from loguru import logger
from collections import defaultdict

async def generate_reddit_search(request: Request) -> Generator[str, None, None]:
    """
    Generate reddit search as an sse stream. Yields a json formatted 
    listing upon each event
    """
    reddit = RedditWrapper()
    logger.info("Connecting new reddit sse stream")
    params = defaultdict(lambda: None, **request.query_params)
    listing_generator = reddit.generate_searches(
        search_term=params["search_term"],
        subreddit=params["subreddit"],
        period=params["period"],
        limit=params["limit"],
        sort=params["sort"]
    )
    first_post = None
    for listing in listing_generator:
        if await request.is_disconnected():
            logger.debug("Disconnected reddit sse stream")
            break
        if first_post != listing[0]['data']['name']:
            # only yield if there has been an update to the stream
            first_post = listing[0]['data']['name']
            yield json.dumps({"data": listing})

