import argparse
import ast
import os
import re
import sys

"""<instructions>
Scaffold a new LeetCode problem directory and file.

Creates leetcode/<difficulty>/<name>/<name>.py containing an empty docstring
at the top, ready for you to paste the problem prompt into.

Names are always converted to lowercase snake_case, and digits are spelled out
as words, so you can type the name however you like:

    3Sum                        -> three_sum
    Climbing Stairs             -> climbing_stairs
    Contains Duplicate II       -> contains_duplicate_ii
    Range Sum Query - Immutable -> range_sum_query_immutable
    24 Game                     -> twenty_four_game

The difficulty is looked up in stoney_codes_leetcode_list.py by comparing
snake_case forms, so "3Sum", "3 sum" and "three_sum" all find the same entry.

1. Create a problem whose name is in the list:
   $ python3 new_problem.py 3Sum
   -> leetcode/medium/three_sum/three_sum.py

2. Names with spaces need quotes:
   $ python3 new_problem.py "Climbing Stairs"
   -> leetcode/easy/climbing_stairs/climbing_stairs.py

3. Use a short directory name and point at the list entry by number:
   $ python3 new_problem.py contains_dupe_2 -n 219
   -> leetcode/easy/contains_dupe_two/contains_dupe_two.py

4. Skip the list entirely and state the difficulty yourself:
   $ python3 new_problem.py sliding_window_practice -d medium

Nothing is ever overwritten: if the file already exists the script reports it
and exits.
</instructions>
"""

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LEETCODE_DIR = os.path.dirname(SCRIPT_DIR)
DEFAULT_LIST = os.path.join(SCRIPT_DIR, "stoney_codes_leetcode_list.py")

TEMPLATE = '"""\n\n"""\n'

ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy",
        "eighty", "ninety"]
SCALES = [(10 ** 9, "billion"), (10 ** 6, "million"), (10 ** 3, "thousand")]


def _words_under_thousand(n):
    words = []
    if n >= 100:
        words.extend([ONES[n // 100], "hundred"])
        n %= 100
    if n >= 20:
        words.append(TENS[n // 10])
        n %= 10
        if n:
            words.append(ONES[n])
    elif n:
        words.append(ONES[n])
    return words


def number_to_words(digits):
    """Spell a run of digits out in words: '3' -> 'three', '24' -> 'twenty four'."""
    # Very long runs are not really numbers, so read them digit by digit.
    if len(digits) > 12 or digits.startswith("0"):
        return [ONES[int(d)] for d in digits]

    n = int(digits)
    if n == 0:
        return ["zero"]

    words = []
    for scale_value, scale_name in SCALES:
        if n >= scale_value:
            words.extend(_words_under_thousand(n // scale_value))
            words.append(scale_name)
            n %= scale_value
    if n:
        words.extend(_words_under_thousand(n))
    return words


def snake_case(name):
    """Convert any problem name to lowercase snake_case with digits spelled out."""
    # Spell out digit runs, padded so they never fuse with neighbouring words.
    spelled = re.sub(r"\d+", lambda m: "_" + "_".join(number_to_words(m.group())) + "_", name)
    # Break camelCase and acronym boundaries apart before lowercasing.
    spelled = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", spelled)
    spelled = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", "_", spelled)
    # Everything that is not alphanumeric becomes a separator.
    spelled = re.sub(r"[^0-9A-Za-z]+", "_", spelled)
    return spelled.strip("_").lower()


def load_problems(filename):
    with open(filename, "r") as f:
        content = f.read()

    if "=" in content:
        _, rhs = content.split("=", 1)
    else:
        rhs = content

    return ast.literal_eval(rhs.strip())


def find_problem(problems, name, leetcode_num=None):
    """Find the list entry for a name, or for an explicit leetcode number."""
    if leetcode_num is not None:
        for p in problems:
            if str(p.get("leetcode_num")) == str(leetcode_num):
                return p
        return None

    target = snake_case(name)
    for p in problems:
        if snake_case(p.get("name")) == target:
            return p
    return None


def create_problem(name, difficulty=None, leetcode_num=None, filename=DEFAULT_LIST):
    slug = snake_case(name)
    if not slug:
        print(f"Error: '{name}' does not contain anything usable as a name.")
        return 1

    problem = None
    if difficulty is None or leetcode_num is not None:
        try:
            problems = load_problems(filename)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return 1
        except Exception as e:
            print(f"Error processing file: {e}")
            return 1

        problem = find_problem(problems, name, leetcode_num)

    if difficulty is None:
        if problem is None:
            if leetcode_num is not None:
                print(f"Error: No problem with leetcode_num {leetcode_num} in '{filename}'.")
            else:
                print(f"Error: '{name}' was not found in '{filename}'.")
            print("Pass -d/--difficulty to create it anyway, or -n/--num to match by LeetCode number.")
            return 1
        difficulty = problem["difficulty"]

    difficulty = snake_case(difficulty)

    problem_dir = os.path.join(LEETCODE_DIR, difficulty, slug)
    problem_file = os.path.join(problem_dir, f"{slug}.py")

    if os.path.exists(problem_file):
        print(f"Error: '{problem_file}' already exists. Nothing was changed.")
        return 1

    os.makedirs(problem_dir, exist_ok=True)
    with open(problem_file, "w") as f:
        f.write(TEMPLATE)

    if problem is not None:
        print(f"-> Matched '{problem['name']}' (#{problem['leetcode_num']}, {problem['difficulty']}).")
    print(f"Created {problem_file}")
    print("Paste the problem prompt inside the docstring at the top.")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create a new LeetCode problem directory and starter file."
    )
    parser.add_argument("name", type=str, help="Problem name, converted to lowercase snake_case.")
    parser.add_argument("-d", "--difficulty", type=str, default=None,
                        help="Difficulty to use instead of looking it up (e.g. easy, medium, hard).")
    parser.add_argument("-n", "--num", type=int, default=None,
                        help="LeetCode number to look up when the name you want differs from the list.")
    parser.add_argument("-f", "--file", type=str, default=DEFAULT_LIST,
                        help="Problem list file to look the difficulty up in.")

    args = parser.parse_args()
    sys.exit(create_problem(args.name, difficulty=args.difficulty, leetcode_num=args.num, filename=args.file))
