"""Chair website scraper: discovers team members and extracts their profiles.

Uses httpx for fetching and LLMPort (chat_structured) for extraction.
Returns plain ResearcherInfo dicts, leaving persistence to the caller.
"""

from __future__ import annotations

import logging

import httpx
from pydantic import BaseModel, Field

from app.llm.port import LLMPort
from app.papers.domain import ResearcherInfo
from app.scraper.interfaces import ResearcherDiscoveryClient

logger = logging.getLogger(__name__)


class EmployeeData(BaseModel):
    """Single employee extracted from chair website."""

    name: str
    title: str | None = None
    role: str | None = None
    email: str | None = None
    profile_url: str | None = None


class EmployeeListOutput(BaseModel):
    """LLM-structured output: list of employees."""

    employees: list[EmployeeData] = Field(default_factory=list)


class ChairDiscoveryAdapter(ResearcherDiscoveryClient):
    """Scrapes a chair website, extracts team members, and returns them as ResearcherInfo."""

    def __init__(self, llm_port: LLMPort, timeout_seconds: int = 10) -> None:
        self._llm = llm_port
        self._timeout = timeout_seconds
        self._session: httpx.AsyncClient | None = None

    async def discover_researchers(self, chair_website_url: str) -> list[ResearcherInfo]:
        """Fetch chair team page, extract employees via LLM, return as ResearcherInfo list."""
        # Fetch the page
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.get(chair_website_url)
                response.raise_for_status()
                html = response.text
        except Exception as e:
            logger.error("Failed to fetch %s: %s", chair_website_url, e)
            return []

        # Extract employees via structured LLM
        try:
            result = await self._llm.chat_structured(
                messages=[
                    {
                        "role": "user",
                        "content": f"""Extract all team members from this chair/department website.
For each person, extract: name, title, role, email, profile_url.

Return as JSON with structure: {{"employees": [{{"name": "...", "title": "...", "role": "...", "email": "...", "profile_url": "..."}}]}}

HTML:
{html}""",
                    }
                ],
                response_model=EmployeeListOutput,
            )
            employees = result["employees"] if isinstance(result, dict) else result.employees
        except Exception as e:
            logger.error("LLM extraction failed for %s: %s", chair_website_url, e)
            return []

        # Convert to ResearcherInfo, adding source_url
        researchers = []
        for emp in employees:
            emp_dict = emp if isinstance(emp, dict) else emp.model_dump()
            researcher = ResearcherInfo(
                name=emp_dict["name"],
                title=emp_dict.get("title"),
                role=emp_dict.get("role"),
                email=emp_dict.get("email"),
                profile_url=emp_dict.get("profile_url"),
                source_url=chair_website_url,
            )
            researchers.append(researcher)

        logger.info("Discovered %d researchers from %s", len(researchers), chair_website_url)
        return researchers

    async def close(self) -> None:
        """Clean up resources."""
        if self._session is not None:
            await self._session.aclose()
