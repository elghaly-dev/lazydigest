import argparse
import time

import schedule

from src import config
from src.digest_engine import process_notes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LazyDigest CLI")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--daemon", action="store_true", help=f"Run daily at {config.RUN_AT}")
    args = parser.parse_args()

    if args.daemon:
        print(f"Daemon active. Scheduled to run daily at {config.RUN_AT}...")
        schedule.every().day.at(config.RUN_AT).do(process_notes)
        while True:
            schedule.run_pending()
            time.sleep(60)
    else:
        process_notes()
