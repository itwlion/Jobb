import hashlib
from storage import ai_response
from groq import Groq
from config import load_dotenv
from storage import DB
from storage import ai_response
from storage import get_response
CV = open("C:\\Users\\PC\\Desktop\\hsenPYTH\\jobradar\\jobradar\\cv.txt", "r")
CV = CV.read()
CVh = hashlib.sha256(CV.encode())
CVh = CVh.hexdigest()
job = DB[0]
job_id = job[0]
cached = get_response(job_id, CVh)
ai_call = 0
if cached:
    print("Using Cache:")
    print(cached)
else:
    client = Groq()
    ai_call += 1
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user",
                   "content": f"""
        Analyze the candidate CV against the job listings below.

        CV:
        {CV}

        Jobs:
        {DB}

        Tasks:
        1. Identify the top job matches.
        2. For each match, provide: Job Title, Match Score (0-100), and a 1-sentence justification.
        3. Write a tailored, professional cover letter for the #1 best match.
    """}]
    )
    print(f"New Ai Calls : {ai_call}")
    output = response.choices[0].message.content
    ai_response(job_id, CVh, output)
    print(output)
