import re
import os

SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+')
WORD_PATTERN = re.compile(r"\b\w+\b")

def split_sentences(text: str) -> list[str]:
    return SENTENCE_SPLIT.split(text.strip())

def sentence_chunker(text: str, max_sentences: int = 5):
    """
    Divide the text into chunks, each chunk containing max_sentences of a sentence.
    """
    sentences = split_sentences(text)
    for i in range(0, len(sentences), max_sentences):
        yield " ".join(sentences[i:i + max_sentences])

def heavy_sentence_analysis(text_chunk: str) -> dict:
    words = WORD_PATTERN.findall(text_chunk)

    # CPU-bound simulation
    rare_score = 0
    for _ in range(2000):
        rare_score += sum(len(w) > 7 for w in words)

    return {
        "word_count": len(words),
        "rare_score": rare_score
    }

def analize_content(paragraph: str) -> dict:
    chunks = sentence_chunker(paragraph, max_sentences=2)

    total_words = 0
    total_rare = 0
    chunk_count = 0

    for chunk in chunks:
        result = heavy_sentence_analysis(chunk)
        total_words += result["word_count"]
        total_rare += result["rare_score"]
        chunk_count += 1

    # detect current process and (if possible) the CPU/core executing this code
    pid = os.getpid()

    return {
        "chunk_count": chunk_count,
        "total_words": total_words,
        "total_rare_score": total_rare,
        "pid": pid
    }
