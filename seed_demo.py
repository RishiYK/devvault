#!/usr/bin/env python3
"""
Run this once to populate DevVault with 5 demo snippets.
Usage: python seed_demo.py
"""

import json, os

snippets = [
    {
        "id": 1,
        "title": "Reverse a list",
        "language": "python",
        "description": "Turns a list backwards using slice notation",
        "tags": ["list", "trick", "slicing"],
        "code": "my_list = [1, 2, 3, 4, 5]\nreversed_list = my_list[::-1]\nprint(reversed_list)  # [5, 4, 3, 2, 1]",
        "created_at": "2026-02-18 09:12"
    },
    {
        "id": 2,
        "title": "Read a file line by line",
        "language": "python",
        "description": "Safe way to read a file without loading it all into memory",
        "tags": ["file", "io"],
        "code": "with open(\"myfile.txt\", \"r\") as f:\n    for line in f:\n        print(line.strip())",
        "created_at": "2026-02-19 14:30"
    },
    {
        "id": 3,
        "title": "Debounce function",
        "language": "javascript",
        "description": "Delays a function call until after a wait period",
        "tags": ["js", "performance", "events"],
        "code": "function debounce(fn, wait) {\n  let timer;\n  return function(...args) {\n    clearTimeout(timer);\n    timer = setTimeout(() => fn.apply(this, args), wait);\n  };\n}",
        "created_at": "2026-02-20 10:05"
    },
    {
        "id": 4,
        "title": "Flatten a nested list",
        "language": "python",
        "description": "Turns [[1,2],[3,4]] into [1,2,3,4]",
        "tags": ["list", "flatten", "comprehension"],
        "code": "nested = [[1, 2], [3, 4], [5, 6]]\nflat = [x for xs in nested for x in xs]\nprint(flat)  # [1, 2, 3, 4, 5, 6]",
        "created_at": "2026-02-20 11:42"
    },
    {
        "id": 5,
        "title": "Bash: find large files",
        "language": "bash",
        "description": "Lists files over 100MB sorted by size",
        "tags": ["bash", "files", "disk"],
        "code": "find . -type f -size +100M | xargs ls -lh | sort -k5 -rh",
        "created_at": "2026-02-20 12:00"
    }
]

path = os.path.join(os.path.expanduser("~"), ".devvault.json")
with open(path, "w") as f:
    json.dump({"snippets": snippets}, f, indent=2)

print(f"✔ Seeded 5 demo snippets to {path}")
print("\nTry these commands:")
print("  python devvault.py list")
print("  python devvault.py view 1")
print("  python devvault.py search list")
print("  python devvault.py stats")
print("  python devvault.py add")
