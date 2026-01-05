import argparse
import os
import asyncio
import csv
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from analize_content import analize_content

@dataclass(frozen=True)
class Movie:
    movie_name: str
    movie_link: str
    fshare_link: str
    original_title: str
    genre: str
    year: int
    runtime: str
    rating: float
    overview: str
    poster_url: str
    backdrop_url: str
    tmdb_id: str

def parse_movie_row(row: dict[str, str]) -> Movie:
    return Movie(
        movie_name=row["Movie Name"].strip(),
        movie_link=row["Movie Link"].strip(),
        fshare_link=row["Fshare Link"].strip(),
        original_title=row["Original Title"].strip(),
        genre=row["Genre"].strip(),
        year=int(row["Year"]),
        runtime=row["Runtime"].strip(),
        rating=float(row["Rating"].strip()) if row["Rating"].strip() else 0.0,
        overview=row["Overview"].strip(),
        poster_url=row["Poster URL"].strip(),
        backdrop_url=row["Backdrop URL"].strip(),
        tmdb_id=row["TMDB ID"].strip(),
    )

# ============================
# Async mock API logger
# ============================

async def log_movie_result(movie: Movie, result: dict) -> None:
    await asyncio.sleep(0.1)  # simulate network delay
    print(f"Movie={movie.original_title} → {result}")


# ============================
# Row processing
# ============================

async def process_movie_row(
    movie: Movie,
    pool: ProcessPoolExecutor,
) -> None:
    loop = asyncio.get_running_loop()

    # CPU-bound work → process pool (process_paragraph now accepts Movie)
    result = await loop.run_in_executor(
        pool,
        analize_content,
        movie.overview,
    )

    # Async I/O
    await log_movie_result(movie, result)


# ============================
# CSV orchestration
# ============================

async def process_csv(path: Path, workers: int) -> None:
    # clamp requested workers to available CPU count
    cpu = os.cpu_count() or 1
    if workers > cpu:
        workers = cpu

    pool = ProcessPoolExecutor(max_workers=workers)

    try:
        tasks = []

        with path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:
                movie = parse_movie_row(row)
                tasks.append(
                    process_movie_row(movie, pool)
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
    # use os.cpu_count() as the default worker count
    cpu = os.cpu_count() or 1
    parser.add_argument(
        "--workers",
        "--worker",
        dest="workers",
        type=int,
        default=cpu,
        help=f"Number of CPU workers (default: {cpu})",
    )

    args = parser.parse_args()
    # fallback with message when requested workers exceed available CPUs
    if args.workers > cpu:
        print(
            f"Requested workers {args.workers} > available CPUs {cpu}; falling back to {cpu}."
        )
        args.workers = cpu
    asyncio.run(process_csv(args.csv_file, args.workers))


if __name__ == "__main__":
    main()
