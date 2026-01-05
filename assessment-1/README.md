## 📅 Week 1.1: Python Mastery & The Infrastructure Shift

- **Goal**: Transition from PHP’s "Isolated Request" model to Python’s "Shared State" and modern tooling.
- **Modern Tooling**:
    - PHP: Composer, `composer.json`, PSR-12.
    - Python: [Poetry](https://python-poetry.org/) (currently used) or [uv](https://github.com/astral-sh/uv) (the 2025 standard for speed), PEP 8, and Type Hinting.
- **Architectural Concepts**:
    - The Global Interpreter Lock (GIL): Understanding why Python is single-threaded but handles concurrency via AsyncIO.
    - Python Memory Model: Mutable vs. Immutable objects (critical for avoiding bugs in long-running processes).
- **Assessment 1**:
    - Task: Build a CLI tool that processes a CSV file concurrently using `ProcessPoolExecutor` (for CPU work) and `AsyncIO` (for mock API logging).
    - Reference: [Python Typing Docs](https://docs.python.org/3/library/typing.html)

## 📄 Assessment 1 — Current Implementation

**Overview**
- **Goal**: Process a CSV of movies using a mix of CPU-bound worker processes and AsyncIO for I/O (mock API logging).
- **Approach**: CPU-heavy text analysis runs in a `ProcessPoolExecutor`; per-row async logging runs with `asyncio`.

**Files of interest**
- `analize_content.py`: simulates CPU-bound analysis — chunks a paragraph by a fixed number of sentences, counts words per chunk, and computes an aggregated 'rare' word score (intensive CPU work).
- `main.py`: CSV orchestration and CLI

**CLI usage**
Run the processor with a CSV file:

```bash
python3 main.py path/to/movies.csv            # uses all available CPUs by default
python3 main.py movies.csv --worker 4         # request 4 workers
python3 main.py movies.csv --worker 999       # will fall back to available CPU count and print a message
```

**Notes & behaviour**
- Results from the CPU analysis are dictionaries and printed by the async logger for each movie.
- `ProcessPoolExecutor` is created with `max_workers` capped at `os.cpu_count()` to avoid over-provisioning.
- The project uses type hints and dataclasses for clearer parsing and data handling.
