import sys
import ast
import argparse

"""<instructions>
How to use the LeetCode Tracker script from the command line:

1. Mark a single problem as done:
   $ python3 tracker.py 1

2. Mark multiple individual problems or ranges as done (wrap in quotes):
   $ python3 tracker.py "15-19, 22, 25-29, 41"

3. Specify a custom Python file using the -f or --file flag:
   $ python3 tracker.py "15-19, 22" -f stoney_codes_leetcode_list.py

4. Undo a range or list of problems (sets 'done' back to 'no'):
   $ python3 tracker.py "15-19, 22" --undo
   
5. Combine custom file and undo flags:
   $ python3 tracker.py "25-29" -f custom_list.py --undo
</instructions>
"""

import sys
import ast
import argparse

def parse_ranges(range_str):
    """Parses strings like '15-19, 22, 25-29, 41' into a sorted list of unique integers."""
    numbers = set()
    # Remove all whitespace to safely handle spaces around dashes or commas
    clean_str = range_str.replace(" ", "")
    parts = clean_str.split(',')
    
    for part in parts:
        if not part:
            continue
        if '-' in part:
            try:
                start_str, end_str = part.split('-')
                start, end = int(start_str), int(end_str)
                # Ensure correct range even if someone types backwards like 19-15
                if start > end:
                    start, end = end, start
                numbers.update(range(start, end + 1))
            except ValueError:
                print(f"Warning: Could not parse range segment '{part}'")
        else:
            try:
                numbers.add(int(part))
            except ValueError:
                print(f"Warning: Could not parse number '{part}'")
                
    return sorted(list(numbers))

def update_status(filename, targets_str, undo=False):
    target_orders = parse_ranges(targets_str)
    if not target_orders:
        print("Error: No valid problem numbers or ranges provided.")
        return

    try:
        # Read the python file content
        with open(filename, "r") as f:
            content = f.read()

        if "=" in content:
            _, rhs = content.split("=", 1)
        else:
            rhs = content

        # Safely parse the python list text into actual python dictionaries
        problems = ast.literal_eval(rhs.strip())
        
        updated_count = 0
        new_status = "no" if undo else "yes"
        action = "marked as NOT done (undone)" if undo else "marked as DONE"

        # Loop through problems and update if their order is in our target list
        for p in problems:
            if p.get("order") in target_orders:
                p["done"] = new_status
                updated_count += 1
                print(f"-> Problem {p['order']} ({p['name']}) has been {action}.")

        if updated_count == 0:
            print(f"Error: None of the specified order numbers {target_orders} were found in '{filename}'.")
            return

        # Write it back cleanly line-by-line using your exact format
        with open(filename, "w") as f:
            f.write("leetcode_problems = [\n")
            for p in problems:
                f.write(f"    {p},\n")
            f.write("]\n")
            
        print(f"\nSuccessfully updated {updated_count} problem(s) in '{filename}'.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Update LeetCode problem progress using single numbers or ranges.")
    parser.add_argument("targets", type=str, help="Problem numbers or ranges (e.g., '15-19, 22, 25-29, 41').")
    parser.add_argument("-f", "--file", type=str, default="stoney_codes_leetcode_list.py", help="Target Python list file.")
    parser.add_argument("--undo", action="store_true", help="Undo the done status (sets done to 'no').")
    
    args = parser.parse_args()  # <-- This was missing!
    update_status(args.file, args.targets, undo=args.undo)