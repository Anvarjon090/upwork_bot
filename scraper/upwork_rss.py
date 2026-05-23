import feedparser
import hashlib
import re
from dataclasses import dataclass


@dataclass
class Job:
    id: str
    title: str
    description: str
    link: str
    published: str
    budget: str


def parse_budget(description: str) -> str:
    budget_match = re.search(r'\$[\d,]+(?:\s*[-–]\s*\$[\d,]+)?(?:/hr)?', description)
    if budget_match:
        return budget_match.group(0)
    return "Ko'rsatilmagan"


def fetch_jobs(rss_url: str) -> list[Job]:
    feed = feedparser.parse(rss_url)
    jobs = []

    for entry in feed.entries:
        job_id = hashlib.md5(entry.link.encode()).hexdigest()
        description = entry.get("summary", "")
        budget = parse_budget(description)

        jobs.append(Job(
            id=job_id,
            title=entry.title,
            description=description[:500],
            link=entry.link,
            published=entry.get("published", ""),
            budget=budget,
        ))

    return jobs
