import sys
import requests
from bs4 import BeautifulSoup


def decode_secret_message(url: str) -> None:
    """
    Retrieves coordinate data from a published Google Doc URL, parses 
    the HTML table, and prints a 2D grid to reveal a secret message.

    The function expects an HTML table where each row (after the header) 
    contains:
        Column 0: x-coordinate (horizontal position)
        Column 1: Character to display
        Column 2: y-coordinate (vertical position)

    It dynamically calculates the dimensions of the grid based on the 
    maximum coordinates found and prints the grid top-to-bottom. Empty 
    spaces in the coordinate plane are filled with standard spaces.

    Args:
        url (str): The standard URL of the published Google Document.
        
    Returns:
        None: Output is printed directly to standard output (stdout).
    """
    # Attempt to fetch the raw HTML content from the provided URL.
    # We use raise_for_status() to immediately catch HTTP errors 
    # (like 404 or 403) rather than failing silently.
    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print("No table found at the provided URL.", file=sys.stderr)
        return

    # Initialize BeautifulSoup to parse the DOM tree of the Google Doc.
    soup: BeautifulSoup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    # Fail gracefully if the document doesn't contain a table.
    if not table:
        print("No table found at the provided URL.", file=sys.stderr)
        return

    # Use a dictionary to map (x, y) coordinates to their characters.
    # This provides O(1) lookup when we construct the final string grid.
    grid_coordinates: dict[tuple[int, int], str] = {}
    
    # Track the max boundaries of our grid to know exactly how large
    # the final nested loop needs to be.
    max_x_coordinate: int = 0
    max_y_coordinate: int = 0
    
    # Slice the rows array starting from index 1 to skip the header row.
    rows = table.find_all('tr')[1:]
    for row in rows:
        cols = row.find_all('td')
        
        # Ensure the row has the expected 3 columns to avoid IndexError.
        if len(cols) >= 3:
            x_coordinate_text: str = cols[0].get_text(strip=True)
            character: str = cols[1].get_text(strip=True)
            y_coordinate_text: str = cols[2].get_text(strip=True)
            
            # Validate that the coordinate strings contain numbers.
            if x_coordinate_text.isdigit() and y_coordinate_text.isdigit():
                x_coordinate: int = int(x_coordinate_text)
                y_coordinate: int = int(y_coordinate_text)
                
                # Dynamically expand our grid boundaries.
                if x_coordinate > max_x_coordinate: 
                    max_x_coordinate = x_coordinate
                if y_coordinate > max_y_coordinate: 
                    max_y_coordinate = y_coordinate
                
                # Plot the point on our virtual grid.
                grid_coordinates[(x_coordinate, y_coordinate)] = character

    # Construct and print the visual grid.
    # Terminals print top-to-bottom, so we iterate the Y-axis backwards 
    # (from max to 0) so the top of the image prints first.
    for current_y_coordinate in range(max_y_coordinate, -1, -1):
        row_characters: list[str] = []
        
        # Iterate the X-axis normally (left to right, 0 to max).
        for current_x_coordinate in range(max_x_coordinate + 1):
            # Attempt to grab the character at the current (x, y). 
            # If nothing exists there, default to a blank space ' '.
            char_to_print = grid_coordinates.get(
                (current_x_coordinate, current_y_coordinate), ' '
            )
            row_characters.append(char_to_print)
            
        # Join the list of characters into a single string and print.
        print("".join(row_characters))


if __name__ == '__main__':
    # Intercept the URL passed as a command-line argument.
    if len(sys.argv) > 1:
        input_url: str = sys.argv[1].strip()
        decode_secret_message(input_url)
    else:
        # Provide helpful usage instructions.
        print("Usage: podman run --rm secret-decoder <URL>", file=sys.stderr)


"""
podman run --rm --entrypoint "python" secret-decoder \
codex_decode.py "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
"""