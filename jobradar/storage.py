import sqlite3


def save_jobs(
    every_job_id,
    every_job__url,
    every_job_title,
    every_job_category,
    every_job_type,
    every_job_date,
    every_job_salary,
    every_job_old
):
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
        zipped_lists = zip(every_job_id, every_job__url, every_job_title,
                           every_job_category, every_job_type, every_job_date, every_job_salary, every_job_old)
        cur.executemany(
            'INSERT OR IGNORE INTO jobs VALUES (?,?,?,?,?,?,?,?)', zipped_lists)


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

        DB = []

        for row in cur.execute("SELECT * FROM jobs"):
            DB.append(row)

        return DB


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
