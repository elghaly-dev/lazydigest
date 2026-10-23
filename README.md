# LazyDigest: Local Markdown Snippet Synthesizer

**LazyDigest** is an open-source, local-first background utility that reads the scattered Markdown notes you drop into a folder and turns them into one short daily digest — a category, a one-line takeaway, and an optional action item per note — using Google's Gemma model running locally through Ollama.

Built for the **Hacktoberfest Open-Source AI Challenge 2026 (Week 3: Slow and Steady)**.

## What It Does
1. **Reads** every `.md` file in `data/input_notes/`.
2. **Analyzes** each note with `gemma3:1b` via Ollama, without sending data to external APIs.
3. **Writes** the results into `data/output_digests/digest_output.md`, then moves processed notes into `data/processed/` so they are never read twice.

## Lazy Payoff
- **Time saved:** roughly 75 minutes a week of re-reading raw notes, tagging them, and copying out action items (our own estimate).
- **Set and forget:** run `--daemon` and it digests your notes every night at 03:00 while you sleep.

## Setup & Running

### Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.com/) installed locally

### Installation
```bash
git clone https://github.com/elghaly-dev/lazydigest.git
cd lazydigest
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
ollama pull gemma3:1b
```

### Usage
```bash
# Run a single pass now
python main.py --once

# Run in the background, daily at 03:00
python main.py --daemon
```

Optional settings live in `.env.example` (model tag, run time, folders). No API keys are needed.

### Tests
```bash
pip install pytest
python -m pytest -q
```
The tests mock the model, so they run without Ollama.

## Model Choice
Gemma 3 1B is small enough to run on an ordinary CPU-only laptop, needs no paid API key and no GPU, and handles short structured-JSON summaries well at low temperature (0.1).

## Privacy & Security
Inference runs on your own machine through the local Ollama server. Your notes are not uploaded anywhere by LazyDigest.

## Limitations
- Built for short to medium plain Markdown notes (`.md`).
- Speed depends on your CPU; expect a few seconds per note on a typical laptop.
- If the model returns invalid JSON, LazyDigest falls back to the note's first line instead of stopping.

## License
MIT License — see [LICENSE](LICENSE).

## Credits & Attribution
- Local model runtime: [Ollama](https://ollama.com/); model: Google Gemma 3.
- Built during Hacktoberfest 2026 DEV Challenge Week 3 by Wyndham Heaven (elghaly, LLC).

## Post-Deadline Changes
None yet.
