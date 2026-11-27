"""A corrected derivation must never overwrite the archived inputs or studies."""
from pathlib import Path

import pytest

from dmaga import paths


@pytest.fixture
def layout(tmp_path, monkeypatch):
    project = tmp_path / "project"
    external = tmp_path / "external"
    monkeypatch.setattr(paths, "ROOT", project, raising=False)
    monkeypatch.setattr(paths, "RAW", external / "raw", raising=False)
    monkeypatch.setattr(paths, "BIG_GELE", external / "data")
    monkeypatch.setattr(paths, "SOURCES", project / "data")
    return project, external


def select(monkeypatch, target):
    monkeypatch.setattr(paths, "_v2", str(target))
    monkeypatch.setattr(paths, "BIG", target)


@pytest.mark.parametrize("target", ["frozen", "raw", "source", "evidence", "study", "group", "ancestor"])
def test_rejects_existing_evidence_directories(layout, tmp_path, monkeypatch, target):
    project, external = layout
    destinations = {
        "frozen": external / "data",
        "raw": external / "raw" / "recomputed",
        "source": project / "data",
        "evidence": project / "evidence" / "derived",
        "study": project / "etude_final" / "derived",
        "group": project / "etude_groupe" / "derived",
        "ancestor": tmp_path,
    }
    select(monkeypatch, destinations[target])
    with pytest.raises(SystemExit, match="protég"):
        paths.exige_v2()


def test_rejects_alias_of_archived_data(layout, tmp_path, monkeypatch):
    _, external = layout
    frozen = external / "data"
    frozen.mkdir(parents=True)
    alias = tmp_path / "alias"
    alias.symlink_to(frozen, target_is_directory=True)
    select(monkeypatch, alias)
    with pytest.raises(SystemExit, match="protég"):
        paths.exige_v2()


def test_allows_a_separate_derived_directory(layout, monkeypatch):
    _, external = layout
    target = external / "data_v2"
    select(monkeypatch, target)
    paths.exige_v2()
    assert target.is_dir()


def test_missing_override_does_not_create_output(layout, monkeypatch):
    _, external = layout
    monkeypatch.setattr(paths, "_v2", None)
    monkeypatch.setattr(paths, "BIG", external / "data")
    with pytest.raises(SystemExit, match="DMAGA_BIG absent"):
        paths.exige_v2()
    assert not paths.BIG.exists()
