"""A failed or overlapping rebuild must not delete the last published trade table."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import runpy
import threading

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from dmaga import db, paths


EXPORT = Path(__file__).resolve().parents[1] / "scripts" / "ana_19_export.py"


def trade(signature, source="pool", slot=2):
    return {"signature": signature, "slot": slot, "tx_index": 0,
            "source": source, "kind": "swap", "owner": "wallet",
            "venue": "pool", "token_delta": 100}


@pytest.fixture
def layout(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "BIG", tmp_path)
    monkeypatch.setattr(db, "TMP", tmp_path / "duckdb")
    monkeypatch.setattr(paths, "BIG", tmp_path)
    monkeypatch.setattr(paths, "exige_v2", lambda: None)
    for sub in ("trades_shards", "vault_shards"):
        (tmp_path / sub).mkdir()
    pq.write_table(pa.Table.from_pylist([trade("new"), trade("new"), trade("new", "mint")]),
                   tmp_path / "trades_shards" / "input.parquet")
    pq.write_table(pa.Table.from_pylist([{"vault": "v", "post": 100}]),
                   tmp_path / "vault_shards" / "input.parquet")
    output = tmp_path / "trades.parquet"
    pq.write_table(pa.Table.from_pylist([trade("previous", slot=1)]), output)
    return output, output.read_bytes()


def run_export():
    runpy.run_path(str(EXPORT), run_name="__main__")


@pytest.mark.parametrize("problem", ["missing", "corrupt"])
def test_input_failure_keeps_previous_materialization(layout, problem):
    output, original = layout
    shard = output.parent / "trades_shards" / "input.parquet"
    if problem == "missing":
        shard.unlink()
    else:
        shard.write_bytes(b"invalid parquet")
    with pytest.raises(duckdb.Error):
        run_export()
    assert output.read_bytes() == original


def test_rebuild_uses_shards_without_losing_deduplication(layout):
    output, _ = layout
    run_export()
    assert pq.read_table(output).to_pylist() == [trade("new")]
    assert not list(output.parent.glob(".trades-*.parquet"))


def test_default_readers_still_use_materialized_table(layout):
    con = db.connect(mem="100MB", threads=1)
    try:
        assert con.execute("SELECT signature FROM trades").fetchall() == [("previous",)]
    finally:
        con.close()


@pytest.mark.parametrize("stage", ["write", "validation", "replace"])
def test_publication_failure_keeps_previous_output_and_removes_staging(layout, monkeypatch, stage):
    output, original = layout
    connect = db.connect
    replace = Path.replace

    class FailingConnection:
        def __init__(self, con):
            self.con = con

        def execute(self, sql, *args, **kwargs):
            result = self.con.execute(sql, *args, **kwargs)
            if stage == "write" and sql.startswith("COPY"):
                raise OSError("injected write failure")
            if stage == "validation" and sql.startswith("SELECT count(*)"):
                raise OSError("injected validation failure")
            return result

        def close(self):
            self.con.close()

    def fail_replace(path, target):
        if stage == "replace" and target == output:
            raise OSError("injected replacement failure")
        return replace(path, target)

    monkeypatch.setattr(db, "connect", lambda **kwargs: FailingConnection(connect(**kwargs)))
    monkeypatch.setattr(Path, "replace", fail_replace)
    with pytest.raises(OSError, match="injected"):
        run_export()
    assert output.read_bytes() == original
    assert not list(output.parent.glob(".trades-*.parquet"))


def test_overlapping_exports_have_independent_staging_files(layout, monkeypatch):
    output, _ = layout
    connect = db.connect
    replace = Path.replace
    ready_to_publish = threading.Barrier(2, timeout=10)
    first_write_finished = threading.Event()
    worker = threading.local()
    sources = []
    sources_lock = threading.Lock()

    class OrderedConnection:
        def __init__(self, con):
            self.con = con

        def execute(self, sql, *args, **kwargs):
            if sql.startswith("COPY") and worker.number == 1:
                assert first_write_finished.wait(10)
            result = self.con.execute(sql, *args, **kwargs)
            if sql.startswith("COPY") and worker.number == 0:
                first_write_finished.set()
            return result

        def close(self):
            self.con.close()

    def simultaneous_publish(path, target):
        if target == output:
            with sources_lock:
                sources.append(path)
            ready_to_publish.wait()
        return replace(path, target)

    def run_worker(number):
        worker.number = number
        run_export()

    monkeypatch.setattr(db, "connect", lambda **kwargs: OrderedConnection(connect(**kwargs)))
    monkeypatch.setattr(Path, "replace", simultaneous_publish)
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = [pool.submit(run_worker, number) for number in range(2)]
        for result in results:
            result.result(timeout=20)
    assert len(set(sources)) == 2
    assert pq.read_table(output).to_pylist() == [trade("new")]
    assert not list(output.parent.glob(".trades-*.parquet"))
