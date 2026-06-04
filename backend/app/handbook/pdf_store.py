"""Temporary Redis storage for uploaded handbook PDFs.

Mirrors the pattern in students/pdf_store.py.  The PDF bytes are stashed here
by the HTTP controller so the Celery worker can retrieve them by job id.
"""

from __future__ import annotations

import redis.asyncio as aioredis

_HANDBOOK_PDF_TTL_SECONDS = 3600


def _key(job_id: str) -> str:
    return f"handbook_pdf:{job_id}"


async def store_handbook_pdf(redis_url: str, job_id: str, data: bytes) -> None:
    client = aioredis.from_url(redis_url)
    try:
        await client.set(_key(job_id), data, ex=_HANDBOOK_PDF_TTL_SECONDS)
    finally:
        await client.aclose()


async def fetch_handbook_pdf(redis_url: str, job_id: str) -> bytes | None:
    client = aioredis.from_url(redis_url)
    try:
        return await client.get(_key(job_id))
    finally:
        await client.aclose()


async def delete_handbook_pdf(redis_url: str, job_id: str) -> None:
    client = aioredis.from_url(redis_url)
    try:
        await client.delete(_key(job_id))
    finally:
        await client.aclose()
