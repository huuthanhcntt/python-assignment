📅 Week 1.1: Python Mastery & The Infrastructure Shift
Goal: Transition from PHP’s "Isolated Request" model to Python’s "Shared State" and modern tooling.
Modern Tooling:
PHP: Composer, composer.json, PSR-12.
Python: Poetry (currently used in AskBob) or uv (the 2025 standard for speed), PEP 8, and Type Hinting.
Architectural Concepts:
The Global Interpreter Lock (GIL): Understanding why Python is single-threaded but handles concurrency via AsyncIO.
Python Memory Model: Mutable vs. Immutable objects (critical for avoiding bugs in long-running processes).
Assessment 1:
Task: Build a CLI tool that processes a CSV file concurrently using ProcessPoolExecutor (for CPU work) and AsyncIO (for mock API logging).
Reference: [Python Typing Docs](https://docs.python.org/3/library/typing.html)