"""Exercise 7: review the repository before you push it to GitHub.

Checks what git would publish: no outputs, data, environments or secrets in any commit, no large files,
and every script you wrote is committed. It prints file names only, never file contents.

Run:  uv run python exercises/07_review_before_push.py
"""
import re
import subprocess
import sys

BLOCKED = re.compile(r"(^|/)(out|\.venv|__pycache__)/|(^|/)\.env|\.(nc|grib2?|h5|tif|csv)$|\.zarr(/|$)|(^|/)keys")
# Shapes of common secrets (OpenRouter, Anthropic, GitHub, AWS). Matched, never printed.
SECRET = re.compile(r"sk-or-v1-[0-9a-f]{20,}|sk-ant-[\w-]{20,}|gh[pousr]_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}")
MAX_KB = 1000


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


problems = []
tracked = git("ls-files").splitlines()

# 1. Nothing that should stay local is tracked.
for f in tracked:
    if BLOCKED.search(f):
        problems.append(f"tracked but should not be: {f}")

# 2. No large files, no secrets in tracked files (the lock file is large on purpose).
for f in tracked:
    try:
        data = open(f, "rb").read()
    except OSError:
        continue
    if len(data) > MAX_KB * 1024 and f != "uv.lock":
        problems.append(f"large file ({len(data) // 1024} KB): {f}")
    if SECRET.search(data.decode(errors="ignore")):
        problems.append(f"looks like a key or token, remove it and tell the instructor: {f}")

# 3. Secrets in any earlier commit count too: a later deletion does not remove them from history.
if SECRET.search(git("log", "-p", "--all")):
    problems.append("a key or token appears in an earlier commit: stop and ask the instructor, do not push")

# 4. Work that is not committed yet.
status = git("status", "--porcelain").splitlines()
unsaved = [s[3:] for s in status if s[3:].endswith(".py") or s[3:].endswith(".md")]

print("Commits on this branch:")
print("  " + git("log", "--oneline", "-15").replace("\n", "\n  ").rstrip())
print("Remotes:")
print("  " + git("remote", "-v").replace("\n", "\n  ").rstrip())
if unsaved:
    print("Not committed yet (commit them if they are your work):")
    for f in unsaved:
        print("  ", f)
if problems:
    print("\nFix before pushing:")
    for p in problems:
        print("  -", p)
    sys.exit(1)
print("\nOK to push: no outputs, data, large files or secrets are tracked.")
print("Still check by eye: are the numbers finite, the units right, and the sizes plausible?")
