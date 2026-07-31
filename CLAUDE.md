# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal LeetCode practice repository.
This is a learning space. The owner is here to work problems out for himself.
Solutions are learning exercises, not production code and not a reusable library.
See README.md for the full description.

## Hard rule: hands off the code

The solutions in this repository are the owner's learning work. Agents do not touch them and do not comment on them.

Never do any of the following unless the owner explicitly and unambiguously asks in that message:

- Create, edit, delete, rename, refactor, reformat, or "clean up" any `.py` file
- Suggest an improvement, optimization, alternative approach, better data structure, or idiomatic rewrite
- Point out a bug, a logic error, dead code, an unused variable, a misleading name, or a misleading comment
- Comment on the correctness, style, efficiency, or complexity of an existing solution
- Offer any of the above as an aside, a footnote, a "worth noting", or a "still outstanding" item at the end of an unrelated task

This holds even when something is plainly wrong.
Noticing a defect is not a reason to mention it.
Working the problem out unaided is the entire point of this repository, and an unsolicited answer takes that away.
If you spot something, say nothing.

"Explicitly asks" means a direct request about the code, in the current message - for example "review this", "why is this wrong", "make this faster".
A vague or adjacent instruction is not permission.
Prior permission does not carry forward: asking for help on one problem does not open the rest of the repo, and it expires at the end of that exchange.

When help is requested, answer only the question asked and stop.

## What agents are for here

Menial, mechanical, non-coding work:

- Git: branches, commits, pushes, PRs, post-merge cleanup
- Documentation: README, this file
- Configuration: `.gitignore`, `.claude/`, tooling config
- Filesystem chores: creating problem directories, moving or renaming files as instructed

Running a solution is fine when asked. Report its output verbatim and add no evaluation.

## Hard rule: no PII

Never write personally identifiable information anywhere in this repository - source, comments, sample data, filenames, or commit messages.
No real names, emails, phone numbers, addresses, account numbers, employer or client names, credentials, tokens, or internal hostnames.
All sample data must be synthetic and obviously fake.

If a request would introduce PII, substitute a placeholder and say so.

## Layout and running

Problems live at `leetcode/<difficulty>/<problem_name>/<problem_name>.py`, `snake_case` throughout.

Each file is standalone: it defines its input at module level and prints the result.
Run one with `python3 leetcode/easy/missing_number/missing_number.py`.

There is no build, no lint config, no dependency manifest, and no test suite - standard library only.
Do not add tooling, frameworks, or a `requirements.txt` unless explicitly asked.

## File conventions

Recorded so you can read these files correctly, not as a standard to enforce.
They are deliberate and differ from normal production practice.
Do not flag a file for departing from them:

- Open with the problem statement (module docstring or comment block), plus constraints when they affect the approach.
- Keep superseded attempts commented out in the file instead of deleting them.
  The brute-force version sitting above the optimized one is the point of the exercise.
- Annotate every implementation with its time and space complexity, and explain briefly where the cost comes from.
- The active implementation is the last, uncommented one in the file.

## Working style here

Do the menial task you were given, confirm it is done, and stop.
No code review, no suggestions, no closing list of things you noticed.
Silence about the code is the correct default, not a missed opportunity to help.

## Zenith agent instructions

These are common instructions for Zenith's agents across all scenarios.

General Guidelines

- Never use the em dash "—". Use plain dash "-" instead
- When writing commit messages, NEVER auto-add your agent name as co-author
- Never manually modify CHANGELOG.md files or any files that are marked as auto-generated
- When writing or substantially editing long Markdown files, put each full sentence on its own line.
  Preserve normal Markdown structure, but avoid wrapping multiple sentences onto one physical line.
- When making technical decisions, do not give much weight to development cost.
  Instead, prefer quality, simplicity, robustness, scalability, and long term maintainability.
- When doing bug fixes, always start with reproducing the bug in an E2E setting as closely aligned with how an end use
  This makes sure you find the real problem so your fix will actually solve it.
- When end-to-end testing a product, be picky about the UI you see and be obsessed with pixel perfection.
  If something clearly looks off, even if it is not directly related to what you are doing, try to get it fixed along
- Apply that same high standard to engineering excellence: lint, test failures, and test flakiness.
  If you see one, even if it is not caused by what you are working on right now, still get it fixed.

Zenith Opinions

When you are working on something that would benefit from being informed by Zenith's viewpoints, read ./OPINIONS.md to understand.
If I have a new opinion and the file doesn't exist, we need to create and ask the user if they want this added to OPINIONS.md

## Post-merge cleanup

When the user says a PR is merged, perform this cleanup automatically without being asked.
Do not wait for the user to spell out the steps each time.

1. `git fetch origin --prune`
2. `git checkout main`
3. `git merge --ff-only origin/main` to fast-forward local `main` to the merged state.
4. Delete the feature branch locally: `git branch -D <feature-branch>`.
   Use `-D`, not `-d`: squash and rebase merges rewrite the SHA, so `-d` refuses the delete even though the work landed.
5. Delete the feature branch on the remote: `git push origin --delete <feature-branch>`.
6. Verify the result: on `main`, in sync with `origin/main`, and the feature branch gone from both local and remote.
7. Remove any temporary or scratch directories and scaffolding created during the work.
