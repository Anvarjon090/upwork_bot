import hashlib
import re
import aiohttp
import feedparser
from dataclasses import dataclass


@dataclass
class Job:
    id: str
    title: str
    description: str
    link: str
    published: str
    budget: str
    source: str


def parse_budget(description: str) -> str:
    budget_match = re.search(r'\$[\d,]+(?:\s*[-–]\s*\$[\d,]+)?(?:/hr)?', description)
    if budget_match:
        return budget_match.group(0)
    return "Ko'rsatilmagan"


def fetch_rss_jobs(rss_url: str, source: str) -> list[Job]:
    feed = feedparser.parse(rss_url)
    jobs = []
    for entry in feed.entries:
        job_id = hashlib.md5(entry.link.encode()).hexdigest()
        description = entry.get("summary", "")
        jobs.append(Job(
            id=job_id,
            title=entry.title,
            description=description[:500],
            link=entry.link,
            published=entry.get("published", ""),
            budget=parse_budget(description),
            source=source,
        ))
    return jobs


async def fetch_remoteok_jobs() -> list[Job]:
    url = "https://remoteok.com/api?tag=python"
    headers = {"User-Agent": "Mozilla/5.0"}
    jobs = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json(content_type=None)
                for item in data[1:]:
                    if not isinstance(item, dict):
                        continue
                    job_id = hashlib.md5(str(item.get("id", "")).encode()).hexdigest()
                    description = re.sub(r"<[^>]+>", "", item.get("description", ""))
                    jobs.append(Job(
                        id=job_id,
                        title=item.get("position", ""),
                        description=description[:500],
                        link=item.get("url", ""),
                        published=item.get("date", ""),
                        budget=parse_budget(description),
                        source="RemoteOK",
                    ))
    except Exception:
        pass
    return jobs


async def fetch_all_jobs(rss_urls: list[tuple[str, str]]) -> list[Job]:
    jobs = []
    for url, source in rss_urls:
        jobs.extend(fetch_rss_jobs(url, source))
    jobs.extend(await fetch_remoteok_jobs())
    return jobs
