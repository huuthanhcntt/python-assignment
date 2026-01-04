import argparse
import asyncio
import csv
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Dict


# ============================
# CPU-bound work (TOP-LEVEL)
# ============================

def analyze_overview(overview: str) -> int:
    """
    Simulate CPU-heavy text analysis.
    """
    score = 0
    for char in overview:
        score += ord(char) % 7
    return score


# ============================
# Async mock API logger
# ============================

async def log_movie_result(tmdb_id: str, score: int) -> None:
    await asyncio.sleep(0.1)  # simulate network delay
    print(f"[API] TMDB={tmdb_id} → score={score}")


# ============================
# Row processing
# ============================

async def process_movie_row(
    row: Dict[str, str],
    pool: ProcessPoolExecutor,
) -> None:
    loop = asyncio.get_running_loop()

    overview = row["Overview"]
    tmdb_id = row["TMDB ID"]

    # CPU-bound work → process pool
    score = await loop.run_in_executor(
        pool,
        analyze_overview,
        overview,
    )

    # Async I/O
    await log_movie_result(tmdb_id, score)


# ============================
# CSV orchestration
# ============================

async def process_csv(path: Path, workers: int) -> None:
    pool = ProcessPoolExecutor(max_workers=workers)

    try:
        tasks = []

        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                tasks.append(
                    process_movie_row(row, pool)
                )

        await asyncio.gather(*tasks)

    finally:
        pool.shutdown()


# ============================
# CLI entry point
# ============================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Process movie CSV using ProcessPoolExecutor + AsyncIO"
    )
    parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to movie CSV file",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of CPU workers (default: 4)",
    )

    args = parser.parse_args()
    asyncio.run(process_csv(args.csv_file, args.workers))


if __name__ == "__main__":
    main()
