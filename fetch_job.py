import sys
from langchain_openai import ChatOpenAI
import requests
import sqlite3
from dotenv import load_dotenv
load_dotenv()
con = None
try:
    con = sqlite3.connect("jobs.db")
    cur = con.cursor()
    try:
        with open("cv.txt", "r") as f:
            cv = f.read().strip()
    except FileNotFoundError:
        print("<<!>> CV.TXT is not found or it is empty")
        if con:
            con.close()
        sys.exit(1)
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
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS ai_cache(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        report TEXT
                    )
                    """)
    cur.execute("SELECT report FROM ai_cache ORDER BY id DESC LIMIT 1")
    cached = cur.fetchone()
    if cached:
        print("---LOADED FROM CACHE---")
        print(cached[0])
        con.close()
        sys.exit(0)
    jet = requests.get("https://remotive.com/api/remote-jobs", timeout=10)
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
    cur.executemany(
        "INSERT OR IGNORE INTO jobs (Id,url,title,companyname,category,salary) VALUES (?,?,?,?,?,?)",
        job_list
    )
    con.commit()
    cur.execute("SELECT * FROM jobs")
    db = cur.fetchall()
    llm = ChatOpenAI(
        model="gpt-5-nano",
        max_completion_tokens=2000,
        max_retries=5
    )
    formatted_jobs = "\n".join(
        [
            f'{row[0]}|{row[2]}|{row[3]}|{row[4]}|{row[5]}'
            for row in db
        ]
    )
    messages = [
        (
            "system",
            "You are Ai job matcher.Try each job on the cv list them from the best and evaluate each one on a scale to one hundred write a draft letter for the best job"
        ),
        ("human", f"Here is my CV \n {cv} \n find me jobs from the Databse \n {formatted_jobs} \n and give me a score on a hunder on each job and tell me why and draft a cover letter for my best match.")
    ]
    ai_msg = llm.invoke(messages)
    print(ai_msg.content)
    cur.execute("INSERT INTO ai_cache (report) VALUES (?)", (ai_msg.content,))
    con.commit()
    con.close()
except KeyboardInterrupt:
    print("\n\n <<!>> Process interrupted by user for pressing (CTRL+C)")
    if con:
        con.rollback()
        con.close()
    print("<< :) Safe Shutdown Complete >>")
    sys.exit(0)
except Exception as e:
    print(f"<<!>>An ERROR OCCURED : {e}")
    if con:
        con.rollback()
        con.close()
    sys.exit(1)
