"""Temporary provider errors must remain retryable, not become deleted-post evidence."""
import json
import urllib.error

import pytest

from dmaga import xposts


@pytest.mark.parametrize("code", [401, 403, 429, 500, 503])
def test_transient_http_failure_does_not_create_a_post(tmp_path, monkeypatch, code):
    monkeypatch.setattr(xposts, "POSTS", tmp_path / "posts.jsonl")
    monkeypatch.setattr(xposts, "X_RAW", tmp_path / "raw")

    def fail(url, timeout=30):
        raise urllib.error.HTTPError(url, code, "provider error", {}, None)

    monkeypatch.setattr(xposts, "_get", fail)
    with pytest.raises(urllib.error.HTTPError):
        xposts.fetch("1815054374982324401")
    assert not xposts.POSTS.exists()


def test_legacy_error_rows_remain_retryable(tmp_path, monkeypatch):
    posts = tmp_path / "posts.jsonl"
    rows = [
        {"id": "ok", "status": "ok"},
        {"id": "temporary", "status": "unavailable", "fx_http": 429, "synd_http": 503},
        {"id": "legacy", "status": "unavailable", "fx_http": 404},
        {"id": "missing", "status": "unavailable", "fx_http": 404, "synd_http": 410},
    ]
    posts.write_text("\n".join(json.dumps(row) for row in rows))
    monkeypatch.setattr(xposts, "POSTS", posts)
    assert xposts.existing_ids() == {"ok", "missing"}


def test_terminal_source_statuses_are_archived(tmp_path, monkeypatch):
    monkeypatch.setattr(xposts, "POSTS", tmp_path / "posts.jsonl")
    monkeypatch.setattr(xposts, "X_RAW", tmp_path / "raw")

    def missing(url, timeout=30):
        raise urllib.error.HTTPError(url, 404, "not found", {}, None)

    monkeypatch.setattr(xposts, "_get", missing)
    row = xposts.fetch("1815054374982324401")
    assert row["status"] == "unavailable"
    assert row["fx_http"] == row["synd_http"] == 404
    assert xposts.existing_ids() == {row["id"]}
