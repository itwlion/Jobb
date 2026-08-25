import argparse
from .api_client import fetch_jobs, ApiUnavailableError
from .storage import save_jobs, get_jobs
from .ai import analyze_job


def cmd_fetch():
    jobs = fetch_jobs()
    save_jobs(jobs)
    print(f"Fetched {len(jobs)} jobs")


def cmd_stats():
    analyze_job()


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    stats_parser = subparsers.add_parser("stats")
    fetch_parser = subparsers.add_parser("fetch")
    args = parser.parse_args()
    if args.command == "fetch":
        cmd_fetch()
    elif args.command == "stats":
        cmd_stats()


if __name__ == "__main__":
    main()
