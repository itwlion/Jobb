import argparse
from .api_client import fetch_jobs, ApiUnavailableError
from .storage import save_jobs, get_jobs
from .ai import analyze_job


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
    analyze_job()


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
