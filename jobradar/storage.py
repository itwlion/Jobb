from api_client import every_job__url
from api_client import every_job_type
from api_client import every_job_id
from api_client import every_job_salary
from api_client import every_job_title
from api_client import every_job_category
from api_client import every_job_date
import sqlite3
con = sqlite3.connect("JOBS.db")
cur = con.cursor()
cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs(
                id PRIMARY KEY,
                url,
                title,
                category,
                job_type,
                date_posted,
                salary
                )
            """)
zipped_lists = zip(every_job_id, every_job__url, every_job_title,
                   every_job_category, every_job_type, every_job_date, every_job_salary)
cur.executemany(
    'INSERT OR REPLACE INTO jobs VALUES (?,?,?,?,?,?,?)', zipped_lists)
con.commit()
DB = []
for row in cur.execute("SELECT * FROM jobs"):
    DB.append(row)
con.close()
conn = sqlite3.connect("Responses.db")
curs = conn.cursor()
curs.execute("""
             CREATE TABLE IF NOT EXISTS responses(
                 job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 response TEXT
             )
             """)


def ai_response(output):
    curs.execute(
        "INSERT INTO responses(job_id,response) VALUES (?,?)", (job_id, output,))
    conn.commit()
