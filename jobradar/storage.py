from api_client import each_job
import sqlite3
con = sqlite3.connect("JOBS.db")
cur = con.cursor()
