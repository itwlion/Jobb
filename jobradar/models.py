from dataclasses import dataclass


@dataclass
class Job:
    id: int
    url: str
    title: str
    category: str
    job_type: str
    date_posted: str
    salary: str
    is_old: bool


@dataclass
class Match:
    score: int
    matched_skills: list
    missing_skills: list
    reason: str
    seniority: str
    letter: str = ""
