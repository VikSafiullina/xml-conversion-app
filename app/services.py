import logging

import httpx
import redis

from app.config import (
    CACHE_DURATION,
    DUMMY_ENDPOINT,
    REDIS_HOST,
    REDIS_PORT,
    ROSSUM_API_KEY,
    ROSSUM_BASE_URL,
)
from app.utils import log_request_as_curl

logger = logging.getLogger(__name__)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)


async def fetch_annotation_data(annotation_id: str, queue_id: str):
    cache_key = f"annotation_{annotation_id}_queue_{queue_id}"
    cached_data = redis_client.get(cache_key)
    logger.debug(cache_key)

    if cached_data:
        logger.info(
            "Returning cached data for annotation %s in queue %s",
            annotation_id,
            queue_id,
        )
        return cached_data.decode("utf-8")

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{ROSSUM_BASE_URL}/queues/{queue_id}/export",
            headers={"Authorization": f"Bearer {ROSSUM_API_KEY}"},
            params={"id": annotation_id, "format": "xml"},
        )
        curl_command = log_request_as_curl(response.request)
        logger.debug(curl_command)
        response.raise_for_status()
        data = response.content

        logger.debug(f"Fetched XML data: {data.decode('utf-8')}")

        redis_client.set(cache_key, data, ex=CACHE_DURATION)
        logger.info(
            "Fetched and cached new data for annotation %s in queue %s",
            annotation_id,
            queue_id,
        )
        return data.decode("utf-8")


async def post_converted_data(post_data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(DUMMY_ENDPOINT, json=post_data)
        logger.debug(post_data)
    return response.status_code == 200
