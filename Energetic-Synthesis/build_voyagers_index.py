#!/usr/bin/env python3
"""
Build Voyagers jsonl index from chunk JSON files.

- Input:  Energetic-Synthesis/voyagers-chunks/*.json
- Output: Energetic-Synthesis/voyagers-index/voyagers.jsonl
"""

from pathlib import Path
import json

CHUNKS_DIR = Path("Energetic-Synthesis/voyagers-chunks")
INDEX_DIR = Path("Energetic-Synthesis/voyagers-index")
INDEX_FILE = INDEX_DIR / "voyagers.jsonl"


def normalize_chunk(raw, file_path: Path, idx_in_file: int):
    """
    Normalize whatever structure each chunk has into a common shape.

    Adjust this if your JSON structure is slightly different.
    """
    # Try to discover the main text field
    text = (
        raw.get("text")
        or raw.get("content")
        or raw.get("body")
        or raw.get("chunk_text")
        or raw.get("page_text")
        or ""
    )

    # ID: prefer an explicit id, otherwise derive from filename + idx
    cid = raw.get("id") or f"{file_path.stem}-{idx_in_file}"

    # Title: try some likely keys, fallback to filename
    title = (
        raw.get("title")
        or raw.get("heading")
        or raw.get("chapter_title")
        or raw.get("section_title")
        or f"Voyagers · {file_path.stem}"
    )

    # Optional structured metadata
    volume = raw.get("volume") or raw.get("vol") or None
    chapter = raw.get("chapter") or raw.get("chap") or None
    part = raw.get("part") or None

    return {
        "id": str(cid),
        "title": str(title),
        "text": str(text),
        "meta": {
            "source_file": str(file_path.relative_to(CHUNKS_DIR)),
            "index_in_file": idx_in_file,
            "volume": volume,
            "chapter": chapter,
            "part": part,
        },
    }


def main():
    if not CHUNKS_DIR.exists():
        raise SystemExit(f"[ERROR] Chunk directory not found: {CHUNKS_DIR}")

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    total_files = 0
    total_chunks = 0
    skipped_files = 0

    print(f"[INFO] Building Voyagers index from {CHUNKS_DIR}...")
    with INDEX_FILE.open("w", encoding="utf-8") as out_f:
        for fp in sorted(CHUNKS_DIR.rglob("*.json")):
            total_files += 1
            try:
                raw_text = fp.read_text(encoding="utf-8")
                if not raw_text.strip():
                    print(f"[WARN] Empty file, skipping: {fp}")
                    skipped_files += 1
                    continue

                data = json.loads(raw_text)
            except Exception as e:
                print(f"[WARN] Could not parse {fp}: {e}")
                skipped_files += 1
                continue

            # Handle "list of chunks in one file" vs "single chunk per file"
            if isinstance(data, list):
                for idx, item in enumerate(data):
                    chunk = normalize_chunk(item, fp, idx)
                    if not chunk["text"].strip():
                        continue
                    out_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                    total_chunks += 1
            else:
                chunk = normalize_chunk(data, fp, 0)
                if chunk["text"].strip():
                    out_f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                    total_chunks += 1

    print(f"[DONE] Processed files:   {total_files}")
    print(f"[DONE] Skipped files:    {skipped_files}")
    print(f"[DONE] Total chunks out: {total_chunks}")
    print(f"[DONE] Index written to: {INDEX_FILE}")


if __name__ == "__main__":
    main()
