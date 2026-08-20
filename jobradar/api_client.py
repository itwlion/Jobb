import requests
r = requests.get("https://remotive.com/api/remote-jobs", timeout=7)
r = r.json()
jobs = r["jobs"]
every_job_id = []
every_job__url = []
every_job_title = []
every_job_category = []
every_job_type = []
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
