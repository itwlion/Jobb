import requests
import sqlite3
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
con = sqlite3.connect("jobs.db")
cur = con.cursor()
cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs(
                Id INTEGER PRIMARY KEY,
                Url TEXT,
                Title TEXT,
                CompanyName TEXT,
                Category TEXT,
                Salary TEXT
            )
            """
            )
cur.executemany(
    "INSERT OR IGNORE INTO jobs (Id,url,title,companyname,category,salary) VALUES (?,?,?,?,?,?)",
    job_list
)
con.close()
