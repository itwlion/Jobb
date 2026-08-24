import argparse
from .api_client import fetch_jobs, ApiUnavailableError
from .storage import save_jobs, get_jobs
from .ai import analyze_job


def main():

    try:
        jobs = fetch_jobs()
        save_jobs(jobs)
    except ApiUnavailableError:
        print("Could not connect to the job Api. Using Cache")
    analyze_job()
    jobs = get_jobs()
    print(jobs)


if __name__ == "__main__":
    main()
