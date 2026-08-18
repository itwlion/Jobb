import requests
r = requests.get("https://remotive.com/api/remote-jobs")
r = r.json()
jobs = r["jobs"]
every_job = []
for each_job in jobs:
    every_job.append([f"Id : {each_job["id"]}",
                      f"URL : {each_job["url"]}",
                      f"Title : {each_job["title"]}",
                     f"Category : {each_job["category"]}",
                     f"Job Type : {each_job["job_type"]}",
                     f"Date Posted : {each_job["publication_date"]}"
                      ])
print(every_job)
