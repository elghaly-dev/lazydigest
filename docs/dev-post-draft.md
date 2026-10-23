---
title: "LazyDigest: Zero-Effort Note Digests Powered by Local Gemma"
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 3: Slow and Steady](https://dev.to/challenges/hacktoberfest-week3-2026-10-19)*

## What I Built
I built **LazyDigest**, a small background utility that takes the raw, unorganized Markdown notes I drop into a folder and turns them into a short daily digest: a category, a one-line takeaway and an optional action item for each note.

Instead of organizing folders, adding tags or re-reading messy scratchpads, LazyDigest runs quietly every night at 03:00 using Google's **Gemma 3 1B** open-weight model through Ollama. I dump files into a folder, go to sleep, and wake up to a summary.

## Demo
{% youtube DEMO_VIDEO_LINK_PLACEHOLDER %}

*(The video shows LazyDigest reading a folder of raw Markdown notes, writing a digest file offline, and moving the processed notes into the archive folder.)*

## Code
{% github https://github.com/elghaly-dev/lazydigest %}

## How I Built It
* **Local inference:** `ollama-python` with `gemma3:1b`.
* **No API keys:** no cloud services or credentials.
* **CPU friendly:** temperature 0.1 for short, structured JSON on CPU-only laptops.
* **Robust parsing:** strips code fences, fills missing fields, and falls back to the note's first line if the model output is not valid JSON.
* **Archiving and scheduling:** the `schedule` library runs it daily at 03:00 and moves processed files into `data/processed/` so nothing is read twice.
* **Tests:** the model is mocked, so the tests run without Ollama.

## Why Does Open Innovation Matter?
1. **Privacy:** personal scratchpads stay on my own machine.
2. **Offline:** it works without an internet connection.
3. **Ownership:** an open-weight model keeps a local tool working without API deprecations or surprise bills.

## The Lazy Payoff
* **Time saved:** about 75 minutes a week (my estimate) that I used to spend re-reading notes and picking out action items.
* **Effort saved:** no more manual sorting or tagging; I just drop files in the folder.

## Prize Categories
* **Best Use of Gemma**
