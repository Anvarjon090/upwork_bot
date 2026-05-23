from scraper.upwork_rss import Job
from config.settings import SKILLS


def is_matching(job: Job) -> tuple[bool, list[str]]:
    text = (job.title + " " + job.description).lower()
    matched = [skill for skill in SKILLS if skill in text]
    return len(matched) > 0, matched
