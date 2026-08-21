import hashlib
import json
from storage import ai_response
from groq import Groq
from config import load_dotenv
from storage import get_jobs
from storage import ai_response
from storage import get_response


def analyze_job():
    CV = open("C:\\Users\\PC\\Desktop\\hsenPYTH\\jobradar\\jobradar\\cv.txt",
              "r", encoding="utf-8")
    CV = CV.read()
    if not CV.strip():
        print("Your CV is empty")
        exit()
    CVh = hashlib.sha256(CV.encode())
    CVh = CVh.hexdigest()
    DB = get_jobs()
    ai_call = 0
    for job in DB:
        job_id = job[0]
        cached = get_response(job_id, CVh)
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
            {job}

            Tasks:
            1. Identify the top job matches.
            2. For each match, provide: Job Title, Match Score (0-100), and a 1-sentence justification.
            3. Write a tailored, professional cover letter for the #1 best match.
            4. return  the response as a valid JSON
        """}]
            )
            output = response.choices[0].message.content
            try:
                answer = json.loads(output)
            except json.JSONDecodeError:
                print("AI returned invalid JSON.")
            else:
                ai_response(job_id, CVh, output)
                print(output)
    print(f"New Ai Calls : {ai_call}")
