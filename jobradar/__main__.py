import argparse
from .api_client import fetch_jobs, ApiUnavailableError
from .storage import save_jobs, get_jobs
from .ai import analyze_job
import hashlib
import json
from .storage import get_response


def cmd_fetch():
    jobs = fetch_jobs()
    save_jobs(jobs)
    print(f"Fetched {len(jobs)} jobs")


def cmd_list(min_score, limit):
    all_matches = analyze_job(return_all=True)
    filtered = [m for m in all_matches if m["score"] >= min_score]
    limited = filtered[:limit]
    print(f"Jobs with Score >= {min_score}:")
    print("-" * 60)
    for item in limited:
        print(
            f"Score: {item['score']:3d} | ID: {item['id']:7d} | Title: {item['title']}")
    print("-" * 60)
    print(f"Showing {len(limited)} of {len(filtered)} jobs")


def cmd_stats():
    # Read and hash CV
    CV = open("C:\\Users\\PC\\Desktop\\hsenPYTH\\jobradar\\jobradar\\cv.txt",
              "r", encoding="utf-8")
    CV = CV.read()
    if not CV.strip():
        print("Your CV is empty")
        return
    CVh = hashlib.sha256(CV.encode())
    CVh = CVh.hexdigest()

    # Get all jobs
    jobs = get_jobs()

    # Initialize variables
    analyzed = 0
    scores = []
    seniority_count = {}
    category_count = {}

    # Loop through each job
    for job in jobs:
        cached = get_response(job.id, CVh)
        if cached:
            analyzed += 1
            scores.append(cached.score)

            # Count seniority
            seniority_count[cached.seniority] = seniority_count.get(
                cached.seniority, 0) + 1

            # Count category
            category_count[job.category] = category_count.get(
                job.category, 0) + 1

    # Calculate statistics
    total_jobs = len(jobs)
    analyzed_jobs = analyzed

    if scores:
        avg_score = sum(scores) / len(scores)
        highest_score = max(scores)
        lowest_score = min(scores)
    else:
        avg_score = 0
        highest_score = 0
        lowest_score = 0

    # Print statistics
    print("Database Statistics:")
    print("-" * 50)
    print(f"Total Jobs: {total_jobs}")
    print(f"Analyzed Jobs: {analyzed_jobs}")
    print(f"Average Score: {avg_score:.1f}")
    print(f"Highest Score: {highest_score}")
    print(f"Lowest Score: {lowest_score}")
    print()
    print("Seniority Breakdown:")
    for level, count in seniority_count.items():
        print(f"  {level}: {count}")
    print()
    print("Categories:")
    for category, count in sorted(category_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category}: {count}")
    print("-" * 50)


def main():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    stats_parser = subparsers.add_parser("stats")
    fetch_parser = subparsers.add_parser("fetch")
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--min-score", type=int, default=0)
    list_parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    if args.command == "fetch":
        cmd_fetch()
    elif args.command == "stats":
        cmd_stats()
    elif args.command == "list":
        cmd_list(args.min_score, args.limit)


if __name__ == "__main__":
    main()
