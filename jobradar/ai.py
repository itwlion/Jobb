from storage import ai_response
from openai import OpenAI
from config import load_dotenv
from storage import DB
from storage import ai_response
from storage import get_response
CV = open("C:\\Users\\PC\\Desktop\\hsenPYTH\\jobradar\\jobradar\\cv.txt", "r")
CV = CV.read()
job = DB[0]
job_id = job[0]
cached = get_response(job_id)
if cached:
    print("Using Cache:")
    print(cached)
else:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.6",
        input=f"""
    Analyze the candidate CV against the job listings below.

    CV:
    {CV}

    Jobs:
    {DB}

    Tasks:
    1. Identify the top job matches.
    2. For each match, provide: Job Title, Match Score (0-100), and a 1-sentence justification.
    3. Write a tailored, professional cover letter for the #1 best match.
    """)
    output = response.output_text
    ai_response(job_id, output)
    print(output)
