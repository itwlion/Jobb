from api_client import every_job__url
from api_client import every_job_type
from api_client import every_job_id
from api_client import every_job_salary
from api_client import every_job_title
from api_client import every_job_category
from api_client import every_job_date
import sqlite3
with sqlite3.connect("JOBS.db") as con:
    cur = con.cursor()
    cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs(
                id INTEGER PRIMARY KEY,
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
        'INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?,?)', zipped_lists)
    DB = []
    for row in cur.execute("SELECT * FROM jobs"):
        DB.append(row)
conn = sqlite3.connect("Responses.db")
curs = conn.cursor()
curs.execute("""
             CREATE TABLE IF NOT EXISTS responses(
                 job_id INTEGER,
                 cv_hash TEXT,
                 response TEXT,
                 PRIMARY KEY(job_id,cv_hash)
             )
             """)


def ai_response(job_id, cv_hash, output):
    curs.execute(
        "INSERT INTO responses(job_id,cv_hash,response) VALUES (?,?,?)", (job_id, cv_hash, output,))
    conn.commit()


def get_response(job_id, cv_hash):
    curs.execute(
        "SELECT response FROM responses WHERE job_id =? AND cv_hash =?",
        (job_id, cv_hash,)
    )
    result = curs.fetchone()
    if result:
        return result[0]
    return None
