from models import Job
import requests
import time
from datetime import datetime, timezone, timedelta


def old_status(date_string):
    try:
        date = datetime.fromisoformat(
            date_string.replace("Z", "+00:00")
        )
        if date.tzinfo is None:
            date = date.replace(tzinfo=timezone.utc)
        date = date.astimezone(timezone.utc)
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        return date < seven_days_ago
    except (ValueError, TypeError):
        return True


class JobRadarError(Exception):
    pass


class ApiUnavailableError(JobRadarError):
    pass


class RateLimitError(JobRadarError):
    pass


def fetch_jobs():
    url = "https://remotive.com/api/remote-jobs"
    for attempt in range(5):
        try:
            r = requests.get(url, timeout=7)
            if r.status_code == 429:
                if attempt == 4:
                    raise RateLimitError("Rate limited after 5 attempts")
                wait = 2 ** attempt
                print(f'Requeset Failed. Retrying in {wait} seconds.')
                time.sleep(wait)
                continue
            if 500 <= r.status_code < 600:
                if attempt == 4:
                    raise ApiUnavailableError(
                        "Api Failed after 5 attempts")
                wait = 2 ** attempt
                print(f'Request Failed. Retryin in {wait} seconds.')
                time.sleep(wait)
                continue
            r.raise_for_status()
            break
        except requests.RequestException:
            if attempt == 4:
                raise ApiUnavailableError("API Failed After 5 Attempts")
            wait = 2 ** attempt
            print(f'Request Failed. Retrying in {wait} seconds')
            time.sleep(wait)

    r = r.json()
    jobs = r["jobs"]
    Full_Jobs = []
    for each_job in jobs:
        date = each_job.get("publication_date", "Undefined")
        each_job = Job(
            id=each_job.get("id"),
            url=each_job.get("url", "Undeifned"),
            title=each_job.get("title", "Undefinde"),
            category=each_job.get("category", "Undefined"),
            job_type=each_job.get("job_type", "Undefined"),
            date_posted=date,
            salary=each_job.get("salary", "Undefined"),
            is_old=old_status(date)
        )
        Full_Jobs.append(each_job)
    return Full_Jobs
