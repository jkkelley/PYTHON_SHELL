#!/usr/bin/env python3
"""Decode a coordinate-grid secret message from a published Google Doc.

Structure: pure core (parse -> render), impure shell (fetch, print, exit).
Only `fetch_html` and `main` touch the outside world; everything else is a
deterministic function of its arguments and is trivially unit-testable.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Sequence

import requests
from bs4 import BeautifulSoup

CONNECT_TIMEOUT = 5.0
READ_TIMEOUT = 30.0
FILL = " "


class DecodeError(Exception):
    """Raised when the document cannot be interpreted as a coordinate grid."""


@dataclass(frozen=True, slots=True)
class Point:
    x: int
    y: int
    char: str


# --------------------------------------------------------------------------
# Pure core
# --------------------------------------------------------------------------

def _cell_text(cell) -> str:
    """Normalize a cell's text, mapping non-breaking spaces to real spaces."""
    return cell.get_text().replace("\xa0", " ")


def _parse_row(cells: Sequence) -> Point | None:
    """Return a Point, or None if the row is a header / malformed."""
    if len(cells) < 3:
        return None
    try:
        x = int(_cell_text(cells[0]).strip())
        y = int(_cell_text(cells[2]).strip())
    except ValueError:
        return None

    raw = _cell_text(cells[1])
    # Preserve a literal space as a glyph; strip() would collapse the column.
    return Point(x, y, raw[0] if raw else FILL)


def parse_points(html: str) -> tuple[tuple[Point, ...], int]:
    """Parse the first table into points. Returns (points, skipped_row_count)."""
    table = BeautifulSoup(html, "html.parser").find("table")
    if table is None:
        raise DecodeError("no <table> element found in the document")

    points: list[Point] = []
    skipped = 0
    for row in table.find_all("tr"):
        point = _parse_row(row.find_all(["td", "th"]))
        if point is None:
            skipped += 1
        else:
            points.append(point)

    if not points:
        raise DecodeError("table contained no parsable coordinate rows")
    return tuple(points), skipped


def render_grid(points: Sequence[Point]) -> str:
    """Render points as a newline-joined grid, y descending (origin bottom-left)."""
    if not points:
        return ""

    grid = {(p.x, p.y): p.char for p in points}
    xs = [p.x for p in points]
    ys = [p.y for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    lines = [
        "".join(grid.get((x, y), FILL) for x in range(min_x, max_x + 1)).rstrip()
        for y in range(max_y, min_y - 1, -1)
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Impure shell
# --------------------------------------------------------------------------

def fetch_html(url: str, timeout: tuple[float, float]) -> str:
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.text


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="secret-decoder",
        description="Print the grid encoded in a published Google Doc table.",
    )
    parser.add_argument("url", help="URL of the published Google Doc")
    parser.add_argument(
        "--timeout",
        type=float,
        default=READ_TIMEOUT,
        help=f"read timeout in seconds (default: {READ_TIMEOUT})",
    )
    args = parser.parse_args(argv)

    try:
        html = fetch_html(args.url, (CONNECT_TIMEOUT, args.timeout))
    except requests.RequestException as exc:
        print(f"error: fetch failed: {exc}", file=sys.stderr)
        return 2

    try:
        points, skipped = parse_points(html)
    except DecodeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3

    if skipped > 1:  # one skip is the expected header row
        print(f"warning: skipped {skipped} unparsable rows", file=sys.stderr)

    print(render_grid(points))
    return 0


if __name__ == "__main__":
    sys.exit(main())


"""
podman run --rm --entrypoint "python" secret-decoder \
codex_decode.py "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
"""