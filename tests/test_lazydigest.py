import importlib

import pytest


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("LAZYDIGEST_INPUT_DIR", str(tmp_path / "in"))
    monkeypatch.setenv("LAZYDIGEST_PROCESSED_DIR", str(tmp_path / "done"))
    monkeypatch.setenv("LAZYDIGEST_OUTPUT_FILE", str(tmp_path / "out" / "digest.md"))
    import src.config, src.model_runner, src.digest_engine
    for m in (src.config, src.model_runner, src.digest_engine):
        importlib.reload(m)
    (tmp_path / "in").mkdir()
    (tmp_path / "in" / "a.md").write_text("Idea A\nmore", encoding="utf-8")
    (tmp_path / "in" / "b.md").write_text("Idea B\nmore", encoding="utf-8")
    return tmp_path, src.model_runner, src.digest_engine


def test_fenced_and_partial_json(env, monkeypatch):
    tmp, mr, de = env
    replies = iter([
        {"response": '```json\n{"category": "Tech", "key_takeaway": "A works", "action_item": "Try it"}\n```'},
        {"response": '{"category": "Life"}'},  # partial: missing keys
    ])
    monkeypatch.setattr(mr.ollama, "generate", lambda **kw: next(replies))
    assert de.process_notes(analyze=mr.analyze_note_with_gemma) == 2
    out = (tmp / "out" / "digest.md").read_text(encoding="utf-8")
    assert "**[Tech]** A works" in out and "*Action:* Try it" in out
    assert "**[Life]** Idea B" in out
    assert not list((tmp / "in").glob("*.md"))
    assert sorted(p.name for p in (tmp / "done").glob("*.md")) == ["a.md", "b.md"]


def test_garbage_and_error_fallback(env, monkeypatch):
    tmp, mr, de = env
    calls = {"n": 0}
    def fake(**kw):
        calls["n"] += 1
        if calls["n"] == 1:
            return {"response": "not json at all"}
        raise ConnectionError("ollama down")
    monkeypatch.setattr(mr.ollama, "generate", fake)
    assert de.process_notes(analyze=mr.analyze_note_with_gemma) == 2
    out = (tmp / "out" / "digest.md").read_text(encoding="utf-8")
    assert "**[General]** Idea A" in out and "**[General]** Idea B" in out


def test_empty_folder(env):
    tmp, mr, de = env
    for p in (tmp / "in").glob("*.md"):
        p.unlink()
    assert de.process_notes() == 0
