import requests
jet = requests.get("https://remotive.com/api/remote-jobs")
jet = jet.json()
jobs = jet["jobs"]
# jobs is a list containing 16 dicts.
job_list = []
for i in jobs:
    id = i["id"]
    url = i["url"]
    title = i["title"]
    company_name = i['company_name']
    category = i["category"]
    salary = i["salary"]
    job_list.append([id, url, title, company_name, category, salary])
print(job_list)
