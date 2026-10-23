import os

GEMMA_MODEL = os.getenv("LAZYDIGEST_MODEL", "gemma3:1b")
INPUT_DIR = os.getenv("LAZYDIGEST_INPUT_DIR", "data/input_notes")
PROCESSED_DIR = os.getenv("LAZYDIGEST_PROCESSED_DIR", "data/processed")
OUTPUT_FILE = os.getenv("LAZYDIGEST_OUTPUT_FILE", "data/output_digests/digest_output.md")
RUN_AT = os.getenv("LAZYDIGEST_RUN_AT", "03:00")
