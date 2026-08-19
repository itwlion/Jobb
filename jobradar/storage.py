from api_client import every_job__url
from api_client import every_job_type
from api_client import every_job_id
from api_client import every_job_salary
from api_client import every_job_title
from api_client import every_job_category
from api_client import every_job_date
import sqlite3
formatted_id = [(job_id,) for job_id in every_job_id]
formatted_url = [(job_url,) for job_url in every_job__url]
formatted_type = [(job_type,) for job_type in every_job_type]
formatted_salary = [(job_salary,)for job_salary in every_job_salary]
formatted_title = [(job_title,)for job_title in every_job_title]
formatted_category = [(job_category,)for job_category in every_job_category]
formatted_date = [(job_date,)for job_date in every_job_date]
con = sqlite3.connect("JOBS.db")
cur = con.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS jobs(id,url,title,category,job_type,date_posted)")
cur.executemany("INSERT INTO jobs(id) VALUES(?)", formatted_id)
cur.executemany("INSERT INTO jobs(url) VALUES(?)", formatted_url)
cur.executemany("INSERT INTO jobs(title) VALUES(?)", formatted_title)
cur.executemany("INSERT INTO jobs(category) VALUES(?)", formatted_category)
cur.executemany("INSERT INTO jobs(job_type) VALUES(?)", formatted_type)
cur.executemany("INSERT INTO jobs(date_posted) VALUES(?)", formatted_date)
