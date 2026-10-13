import filecmp
import os
import sys

SKILL_DIR = os.path.join("skills", "prove-it-done")
REQUIRED_FILES = ("SKILL.md", "LICENSE", "SECURITY.md")
REQUIRED_DIRS = ("scripts", "references", "examples")


def get_files(directory):
    files = set()

    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs if d != "__pycache__"]

        for filename in filenames:
            if filename.endswith(".pyc"):
                continue

            path = os.path.join(root, filename)
            relative = os.path.relpath(path, directory)
            files.add(relative.replace(os.sep, "/"))

    return files


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print("Usage: python3 scripts/check_skill_sync.py UPSTREAM_DIR")
        return 2

    upstream_dir = sys.argv[1]
    here_dir = SKILL_DIR

    if not os.path.isdir(here_dir):
        print(f"MISSING-HERE {SKILL_DIR}")
        return 1

    here_files = get_files(here_dir)
    upstream_files = set()

    for path in REQUIRED_FILES:
        if os.path.isfile(os.path.join(upstream_dir, path)):
            upstream_files.add(path)

    for directory in REQUIRED_DIRS:
        path = os.path.join(upstream_dir, directory)

        if os.path.isdir(path):
            upstream_files.update(
                f"{directory}/{item}" for item in get_files(path)
            )

    problems = 0

    for path in sorted(here_files - upstream_files):
        print(f"MISSING-UPSTREAM {path}")
        problems += 1

    for path in sorted(upstream_files - here_files):
        print(f"MISSING-HERE {path}")
        problems += 1

    for path in sorted(here_files & upstream_files):
        if not filecmp.cmp(
            os.path.join(here_dir, path),
            os.path.join(upstream_dir, path),
            shallow=False,
        ):
            print(f"DIFFERS {path}")
            problems += 1

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())