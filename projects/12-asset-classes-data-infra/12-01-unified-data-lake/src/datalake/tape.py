"""Tape recorder + deterministic replay (subproject 12-02).

Capture the live depth/LTP feed to disk so any strategy can be **replayed deterministically**
offline — the same events, in the same order, every run. The record/replay format (NDJSON,
optionally gzipped) and ordering are the testable core here; live capture attaches Upstox's
`MarketDataStreamerV3` (SDK + token) and calls `write()` on each message — that wiring is
private (needs the token) and documented in the subproject.
"""
from __future__ import annotations

import gzip
import json
from pathlib import Path


def _open(path: Path, mode: str):
    return gzip.open(path, mode, encoding="utf-8") if str(path).endswith(".gz") else open(path, mode, encoding="utf-8")


class TapeRecorder:
    """Append market events (plain dicts, each with a numeric/ISO `ts`) to an NDJSON tape."""

    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._f = None
        self.n = 0

    def __enter__(self):
        self._f = _open(self.path, "wt")
        return self

    def write(self, event: dict) -> None:
        self._f.write(json.dumps(event, separators=(",", ":")) + "\n")
        self.n += 1

    def record(self, events) -> int:
        """Batch helper (also how tests drive it): write an iterable of events."""
        for e in events:
            self.write(e)
        return self.n

    def __exit__(self, *exc):
        if self._f:
            self._f.close()
            self._f = None


class TapeReplay:
    """Iterate a recorded tape. `events(sort=True)` returns them in `ts` order (deterministic)."""

    def __init__(self, path):
        self.path = Path(path)

    def __iter__(self):
        with _open(self.path, "rt") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)

    def events(self, sort: bool = True) -> list[dict]:
        evs = list(self)
        if sort:
            evs.sort(key=lambda e: e.get("ts", 0))
        return evs
