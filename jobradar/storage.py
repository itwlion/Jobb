from .models import Job
import sqlite3


def save_jobs(jobs):
    jobs = [
        (j.id, j.url, j.title, j.category, j.job_type,
         j.date_posted, j.salary, j.is_old)
        for j in jobs
    ]
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
                    salary,
                    is_old
                    )
                """)
        cur.executemany(
            'INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?,?,?)', jobs)


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


def get_jobs():
    with sqlite3.connect("JOBS.db") as con:
        cur = con.cursor()
        jobs = []
        for row in cur.execute("SELECT * FROM jobs"):
            job = Job(
                id=row[0],
                url=row[1],
                title=row[2],
                category=row[3],
                job_type=row[4],
                date_posted=row[5],
                salary=row[6],
                is_old=row[7]
            )
            jobs.append(job)
        return jobs


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
