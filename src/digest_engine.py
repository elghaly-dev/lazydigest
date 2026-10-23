import glob
import os
import shutil
from datetime import date

from src import config
from src.model_runner import analyze_note_with_gemma


def process_notes(analyze=analyze_note_with_gemma) -> int:
    """Digest every .md note in the input folder, then archive it. Returns count."""
    os.makedirs(config.PROCESSED_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(config.OUTPUT_FILE), exist_ok=True)

    note_files = sorted(glob.glob(os.path.join(config.INPUT_DIR, "*.md")))
    if not note_files:
        print("No notes to digest. Relax!")
        return 0

    print(f"Processing {len(note_files)} notes with local Gemma...")
    summaries = []
    for file_path in note_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        summaries.append((os.path.basename(file_path), analyze(content)))
        shutil.move(file_path, os.path.join(config.PROCESSED_DIR, os.path.basename(file_path)))

    with open(config.OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n## Daily Lazy Digest ({date.today().isoformat()})\n")
        for filename, data in summaries:
            f.write(f"- **[{data.get('category', 'General')}]** {data.get('key_takeaway', '')} _(from {filename})_\n")
            action = data.get("action_item", "None")
            if action and action != "None":
                f.write(f"  - *Action:* {action}\n")

    print(f"Digest written to {config.OUTPUT_FILE}; notes archived to {config.PROCESSED_DIR}.")
    return len(summaries)
