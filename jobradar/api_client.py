import requests
import time


class JobRadarError(Exception):
    pass


class ApiUnavailableError(JobRadarError):
    pass


class RateLimitError(JobRadarError):
    pass


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
                raise ApiUnavailableError("Api Failed after 5 attempts")
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
every_job_id = []
every_job__url = []
every_job_title = []
every_job_category = []
every_job_date = []
every_job_type = []
every_job_salary = []
for each_job in jobs:
    every_job_id.append(each_job["id"])
    every_job__url.append(each_job["url"])
    every_job_category.append(each_job["category"])
    every_job_date.append(each_job["publication_date"])
    every_job_title.append(each_job["title"])
    every_job_salary.append(each_job["salary"])
    every_job_type.append(each_job["job_type"])
