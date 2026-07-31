# PYTHON_SHELL

This is a personal practice repository for working through LeetCode problems in Python.
It is a learning scratchpad, not a library or an application.
Solutions here are written to build intuition for data structures, algorithms, and complexity analysis - not to be imported or reused elsewhere.

## No PII, ever

Nothing in this repository may contain personally identifiable information.
That includes real names, email addresses, phone numbers, physical addresses, account numbers, employer or client names, credentials, tokens, and internal hostnames or URLs.

The rule applies to every part of the repo: source files, comments, docstrings, sample input data, commit messages, branch names, and filenames.
Sample data must be synthetic.
If a problem statement calls for something that looks like personal data, invent an obviously fake placeholder instead.

## Layout

Problems are organized by difficulty, then one directory per problem:

```
leetcode/<difficulty>/<problem_name>/<problem_name>.py
```

Directory and file names use `snake_case` and match the problem title.
Each problem gets its own directory so notes or alternate files can live alongside the solution.

## Running a solution

Each file is standalone and self-executing - it defines its own input at module level and prints the result.

```bash
python3 leetcode/easy/missing_number/missing_number.py
```

There is no build step, no dependency manifest, and no test suite.
Only the Python standard library is used.

## Conventions

Each file opens with the problem statement, as either a module docstring or a comment block, followed by any constraints that matter.

Superseded attempts are kept in the file, commented out, rather than deleted.
Seeing the brute-force version next to the optimized one is the point of the exercise, so the progression stays visible.

Every implementation carries its time and space complexity as a comment, with a short explanation of where the cost comes from.
The final, active implementation is the uncommented one at the bottom.
