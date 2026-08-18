🎟️ Ticket: Homelab OS Utility Library

Description:
Create a reusable Python package that handles common system-level tasks across the homelab, starting with OS detection and generic dependency error messaging.

Acceptance Criteria:
    Project follows the standard Python `src` layout.
    Package is configured using a modern `pyproject.toml` file.
    Contains an importable function for OS detection and error handling.
    Can be installed locally in a virtual environment for reuse in other scripts.

Tasks & Checklist:  
    [ ] 1. Initialize Layout: Create the root directory (`homelab-os-tools`) and the nested `src/homelab_os_tools` directories.
    [ ] 2. Core Logic: Create an `__init__.py` file and the main Python file for the OS detection logic.
    [ ] 3. Packaging Config: Create a `pyproject.toml` file at the root to define the package metadata.
    [ ] 4. Local Install: Use `pip install -e .` to install the library locally so other scripts can import it.