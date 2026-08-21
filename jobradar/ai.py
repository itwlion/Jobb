import hashlib
import json
from .storage import ai_response
from groq import Groq
from .config import load_dotenv
from .storage import get_jobs
from .storage import ai_response
from .storage import get_response


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
            #1 best match.
            3. Write a tailored, professional cover letter for the best job
            4. return  the response as a valid JSON
        """}]
            )
            output = response.choices[0].message.content
            try:
                for attempts in range(2):
                    answer = json.loads(output)
                    if type(answer) == dict:
                        if type(answer["matchscore"]) == int and 0 <= answer["matchscore"] <= 100:
                            ai_response(job_id, CVh, output)
                            break
                        else:
                            response = client.chat.completions.create(
                                model="openai/gpt-oss-120b",
                                messages=[{"role": "user",
                                           "content": f"""
                Your previous response was invalid.

Return ONLY valid JSON.

Rules:
- Use exactly these fields: matchscore, job_title, justification, cover_letter
- matchscore MUST be an integer between 0 and 100.
- 0 and 100 are valid.
- Do not use markdown.
- Do not add any text before or after the JSON.
- Do not put the JSON inside ```.

Example:
{
                                               "matchscore": 75,
  "job_title": "Python Developer",
  "justification": "The candidate has strong Python skills but lacks some required experience.",
  "cover_letter": "Dear Hiring Manager..."
}
            """}]
                            )
                            ai_call += 1
                            output = (response.choices[0].message.content)
                            answer = json.loads(output)
                            if attempts == 1:
                                if type(answer) == dict:
                                    if type(answer["matchscore"]) == int:
                                        if 0 > answer["matchscore"] or answer["matchscore"] > 100:
                                            ai_response(
                                                job_id, CVh, "unscored")
                                            break
                                        else:
                                            ai_response(job_id, CVh, output)
                                        break
            except json.JSONDecodeError:
                ai_response(job_id, CVh, "unscored")
    print(f"New Ai Calls : {ai_call}")
