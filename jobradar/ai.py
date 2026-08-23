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
            Analyze the candidate's CV against the job description.

CV:
{CV}

Job:
{job}

Return ONLY valid JSON.

The JSON must contain exactly these five fields:

{
                               "score": 0,
  "matched_skills": [],
  "missing_skills": [],
  "reason": "",
  "seniority": ""
}

Rules:
- "score" must be an integer from 0 to 100.
- "matched_skills" must be a list of skills the candidate has that match the job.
- "missing_skills" must be a list of important skills required by the job that are missing from the CV.
- "reason" must be a short explanation of why the score was given.
- "seniority" must describe the appropriate level for the candidate/job, such as "junior", "mid", or "senior".
- Only use information actually present in the CV and job description.
- Do not invent skills, experience, education, or qualifications.
- Do not use Markdown.
- Do not put the JSON inside ```.

Return nothing except the JSON.
        """}]
            )
            output = response.choices[0].message.content
            try:
                for attempts in range(2):
                    answer = json.loads(output)
                    if type(answer) == dict:
                        if type(answer["score"]) == int and 0 <= answer["score"] <= 100:
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
- Use exactly these fields: score, matched_skills, missing_skills, reason,seniority
- score MUST be an integer between 0 and 100.
- 0 and 100 are valid.
- Do not use markdown.
- Do not add any text before or after the JSON.
- Do not put the JSON inside ```.

Example:
{
                                               "score": 75,
    "matched_skills": ["Python", "SQL"],
    "missing_skills": ["Docker"],
    "reason": "The candidate has strong Python and SQL skills but lacks Docker experience.",
    "seniority": "junior"
}
            """}]
                            )
                            ai_call += 1
                            output = (response.choices[0].message.content)
                            answer = json.loads(output)
                            if attempts == 1:
                                if type(answer) == dict:
                                    if type(answer["score"]) == int:
                                        if 0 > answer["score"] or answer["score"] > 100:
                                            ai_response(
                                                job_id, CVh, "unscored")
                                            break
                                        else:
                                            ai_response(job_id, CVh, output)
                                        break
            except json.JSONDecodeError:
                ai_response(job_id, CVh, "unscored")
    print(f"New Ai Calls : {ai_call}")
