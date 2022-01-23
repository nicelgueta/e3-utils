from fastapi import APIRouter, Request
from ..middleware.sse import generate_reddit_search
from sse_starlette.sse import EventSourceResponse

import json
from typing import List
import time

router = APIRouter()


@router.get("/sse/redditSearch")
async def reddit_search(request: Request):
    listings_generator = generate_reddit_search(request)
    return EventSourceResponse(listings_generator)
