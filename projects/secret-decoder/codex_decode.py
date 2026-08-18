import sys
from collections.abc import Mapping
from typing import Final

import requests
from bs4 import BeautifulSoup


REQUEST_TIMEOUT_SECONDS: Final[int] = 10


class SecretDecoderError(Exception):
    """Base exception for secret decoder failures."""


class DocumentFetchError(SecretDecoderError):
    """Raised when the remote document cannot be retrieved."""


class CoordinateTableError(SecretDecoderError):
    """Raised when a valid coordinate table cannot be found or parsed."""


def fetch_document(url: str, timeout: int = REQUEST_TIMEOUT_SECONDS) -> str:
    """
    Retrieve HTML content from a published document URL.

    Args:
        url: URL of the published document.
        timeout: Maximum number of seconds to wait for the HTTP request.

    Returns:
        The raw HTML document as a string.

    Raises:
        DocumentFetchError: If the request fails or returns an HTTP error.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise DocumentFetchError(
            f"Unable to retrieve document from {url!r}: {exc}"
        ) from exc

    return response.text


def parse_coordinates(html: str) -> dict[tuple[int, int], str]:
    """
    Parse coordinate data from an HTML table.

    The expected table format is:

        Column 0: x-coordinate
        Column 1: character
        Column 2: y-coordinate

    The first row is treated as the header.

    Args:
        html: Raw HTML containing the coordinate table.

    Returns:
        A mapping of (x, y) coordinates to characters.

    Raises:
        CoordinateTableError: If no table exists, no valid coordinate rows
            are found, or a coordinate value is invalid.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if table is None:
        raise CoordinateTableError("Document does not contain a table.")

    rows = table.find_all("tr")
    if len(rows) < 2:
        raise CoordinateTableError(
            "Coordinate table does not contain any data rows."
        )

    coordinates: dict[tuple[int, int], str] = {}

    for row_number, row in enumerate(rows[1:], start=2):
        columns = row.find_all("td")

        if len(columns) < 3:
            raise CoordinateTableError(
                f"Row {row_number} does not contain the expected 3 columns."
            )

        x_text = columns[0].get_text(strip=True)
        character = columns[1].get_text(strip=True)
        y_text = columns[2].get_text(strip=True)

        try:
            x_coordinate = int(x_text)
            y_coordinate = int(y_text)
        except ValueError as exc:
            raise CoordinateTableError(
                f"Row {row_number} contains an invalid coordinate: "
                f"x={x_text!r}, y={y_text!r}."
            ) from exc

        if x_coordinate < 0 or y_coordinate < 0:
            raise CoordinateTableError(
                f"Row {row_number} contains a negative coordinate: "
                f"x={x_coordinate}, y={y_coordinate}."
            )

        if not character:
            raise CoordinateTableError(
                f"Row {row_number} does not contain a character."
            )

        coordinates[(x_coordinate, y_coordinate)] = character

    if not coordinates:
        raise CoordinateTableError("No valid coordinate data was found.")

    return coordinates


def render_grid(
    coordinates: Mapping[tuple[int, int], str],
    empty_character: str = " ",
) -> str:
    """
    Render coordinate data as a top-to-bottom text grid.

    This function is pure: it performs no I/O and has no external side effects.

    Args:
        coordinates: Mapping of (x, y) coordinates to displayed characters.
        empty_character: Character used for unoccupied grid positions.

    Returns:
        The rendered grid as a newline-delimited string.

    Raises:
        ValueError: If coordinates is empty or contains negative positions.
    """
    if not coordinates:
        raise ValueError("coordinates must not be empty")

    if len(empty_character) != 1:
        raise ValueError("empty_character must contain exactly one character")

    for x_coordinate, y_coordinate in coordinates:
        if x_coordinate < 0 or y_coordinate < 0:
            raise ValueError("coordinates cannot contain negative positions")

    max_x_coordinate = max(x for x, _ in coordinates)
    max_y_coordinate = max(y for _, y in coordinates)

    rendered_rows: list[str] = []

    for current_y in range(max_y_coordinate, -1, -1):
        row = "".join(
            coordinates.get((current_x, current_y), empty_character)
            for current_x in range(max_x_coordinate + 1)
        )
        rendered_rows.append(row)

    return "\n".join(rendered_rows)


def decode_secret_message(url: str) -> str:
    """
    Retrieve, parse, and render the secret message from a published document.

    Args:
        url: URL of the published document.

    Returns:
        The rendered secret message.

    Raises:
        DocumentFetchError: If the document cannot be retrieved.
        CoordinateTableError: If the coordinate table is missing or invalid.
    """
    html = fetch_document(url)
    coordinates = parse_coordinates(html)
    return render_grid(coordinates)


def main(argv: list[str] | None = None) -> int:
    """
    Run the command-line interface.

    Args:
        argv: Optional command-line argument list excluding the program name.

    Returns:
        Process exit code.
    """
    arguments = sys.argv[1:] if argv is None else argv

    if len(arguments) != 1:
        print(
            "Usage: python secret_decoder.py <URL>",
            file=sys.stderr,
        )
        return 2

    url = arguments[0].strip()

    if not url:
        print("URL must not be empty.", file=sys.stderr)
        return 2

    try:
        message = decode_secret_message(url)
    except SecretDecoderError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


"""
podman run --rm --entrypoint "python" secret-decoder \
codex_decode.py "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
"""