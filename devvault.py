#!/usr/bin/env python3
"""
DevVault - Your personal code snippet manager
Save, search, and retrieve code snippets from the terminal.
"""

import json
import os
import sys
import argparse
import datetime
import textwrap

# ── Where snippets are stored ─────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.expanduser("~"), ".devvault.json")

# ── ANSI color helpers ────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"

def c(color, text):
    """Wrap text in a color code."""
    return f"{color}{text}{RESET}"

# ── Storage helpers ───────────────────────────────────────────────────────────
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"snippets": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def next_id(snippets):
    return max((s["id"] for s in snippets), default=0) + 1

# ── Display helpers ───────────────────────────────────────────────────────────
def divider(char="─", width=60):
    print(c(DIM, char * width))

def print_banner():
    banner = f"""
{c(CYAN, BOLD + "  ██████╗ ███████╗██╗   ██╗██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗")}
{c(CYAN,       "  ██╔══██╗██╔════╝██║   ██║██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝")}
{c(CYAN,       "  ██║  ██║█████╗  ██║   ██║██║   ██║███████║██║   ██║██║     ██║   ")}
{c(CYAN,       "  ██║  ██║██╔══╝  ╚██╗ ██╔╝╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   ")}
{c(CYAN,       "  ██████╔╝███████╗ ╚████╔╝  ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   ")}
{c(CYAN,       "  ╚═════╝ ╚══════╝  ╚═══╝    ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   ")}
    {c(DIM, "Your personal code snippet vault  •  v1.0.0")}
"""
    print(banner)

def print_snippet(s, show_code=True):
    """Pretty-print a single snippet."""
    divider()
    tag_str = "  ".join(c(YELLOW, f"#{t}") for t in s.get("tags", []))
    sid = s['id']
    print(f"  {c(BOLD, '[' + str(sid) + ']')}  {c(WHITE, BOLD + s['title'])}   {c(GREEN, s['language'])}")
    if tag_str:
        print(f"  {tag_str}")
    print(f"  {c(DIM, 'Added: ' + s['created_at'])}")
    if s.get("description"):
        print(f"  {c(DIM, s['description'])}")
    if show_code:
        divider("·")
        for line in s["code"].splitlines():
            print(f"  {c(CYAN, line)}")
    divider()

# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_add(args):
    """Interactively add a new snippet."""
    print(c(BOLD, "\n  ✦ Add a new snippet\n"))

    title = input(c(GREEN, "  Title: ")).strip()
    if not title:
        print(c(RED, "  Title cannot be empty.")); return

    language = input(c(GREEN, "  Language (e.g. python, bash, js): ")).strip() or "text"

    description = input(c(GREEN, "  Short description (optional): ")).strip()

    tags_raw = input(c(GREEN, "  Tags (comma-separated, e.g. loop,string): ")).strip()
    tags = [t.strip().lower() for t in tags_raw.split(",") if t.strip()]

    print(c(GREEN, "  Paste your code below."))
    print(c(DIM,   "  Type 'END' on a new line when finished:\n"))

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    code = "\n".join(lines).strip()
    if not code:
        print(c(RED, "  Code cannot be empty.")); return

    data = load_data()
    snippet = {
        "id":          next_id(data["snippets"]),
        "title":       title,
        "language":    language.lower(),
        "description": description,
        "tags":        tags,
        "code":        code,
        "created_at":  datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    data["snippets"].append(snippet)
    save_data(data)
    print(c(GREEN, f"\n  ✔ Snippet #{snippet['id']} '{title}' saved!\n"))


def cmd_list(args):
    """List all snippets (no code shown)."""
    data = load_data()
    snippets = data["snippets"]

    if not snippets:
        print(c(YELLOW, "\n  No snippets yet. Run: python devvault.py add\n"))
        return

    print(c(BOLD, f"\n  ✦ {len(snippets)} snippet(s) in your vault\n"))
    for s in snippets:
        print_snippet(s, show_code=False)
    print()


def cmd_view(args):
    """View a snippet by ID."""
    data = load_data()
    matches = [s for s in data["snippets"] if s["id"] == args.id]
    if not matches:
        print(c(RED, f"\n  Snippet #{args.id} not found.\n"))
        return
    print()
    print_snippet(matches[0], show_code=True)
    print()


def cmd_search(args):
    """Search snippets by keyword or tag."""
    query = args.query.lower()
    data  = load_data()

    results = [
        s for s in data["snippets"]
        if  query in s["title"].lower()
        or  query in s["language"].lower()
        or  query in s.get("description", "").lower()
        or  any(query in t for t in s.get("tags", []))
        or  query in s["code"].lower()
    ]

    if not results:
        print(c(YELLOW, f"\n  No snippets found for '{query}'.\n"))
        return

    print(c(BOLD, f"\n  ✦ {len(results)} result(s) for '{c(CYAN, query)}'\n"))
    for s in results:
        print_snippet(s, show_code=False)
    print()


def cmd_delete(args):
    """Delete a snippet by ID."""
    data = load_data()
    before = len(data["snippets"])
    data["snippets"] = [s for s in data["snippets"] if s["id"] != args.id]

    if len(data["snippets"]) == before:
        print(c(RED, f"\n  Snippet #{args.id} not found.\n"))
        return

    confirm = input(c(YELLOW, f"  Delete snippet #{args.id}? (y/n): ")).strip().lower()
    if confirm == "y":
        save_data(data)
        print(c(GREEN, f"\n  ✔ Snippet #{args.id} deleted.\n"))
    else:
        print(c(DIM, "\n  Cancelled.\n"))


def cmd_stats(args):
    """Show vault statistics."""
    data     = load_data()
    snippets = data["snippets"]

    if not snippets:
        print(c(YELLOW, "\n  Your vault is empty.\n")); return

    # Count by language
    langs = {}
    for s in snippets:
        langs[s["language"]] = langs.get(s["language"], 0) + 1

    all_tags = [t for s in snippets for t in s.get("tags", [])]
    tag_counts = {}
    for t in all_tags:
        tag_counts[t] = tag_counts.get(t, 0) + 1

    top_tags = sorted(tag_counts.items(), key=lambda x: -x[1])[:5]

    print(c(BOLD, "\n  ✦ DevVault Stats\n"))
    divider()
    print(f"  Total snippets : {c(CYAN, str(len(snippets)))}")
    print(f"  Languages used : {c(CYAN, str(len(langs)))}")
    print()
    print(c(BOLD, "  Languages:"))
    for lang, count in sorted(langs.items(), key=lambda x: -x[1]):
        bar = "█" * count
        print(f"    {lang:<12} {c(GREEN, bar)}  {count}")
    if top_tags:
        print()
        print(c(BOLD, "  Top tags:"))
        for tag, count in top_tags:
            print(f"    {c(YELLOW, '#' + tag):<20} {count} snippet(s)")
    divider()
    print()

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print_banner()

    parser = argparse.ArgumentParser(
        prog="devvault",
        description="DevVault – your personal code snippet manager",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # add
    subparsers.add_parser("add",    help="Add a new snippet interactively")
    # list
    subparsers.add_parser("list",   help="List all snippets")
    # stats
    subparsers.add_parser("stats",  help="Show vault statistics")

    # view <id>
    p_view = subparsers.add_parser("view",   help="View a snippet by ID")
    p_view.add_argument("id", type=int, metavar="ID", help="Snippet ID")

    # search <query>
    p_search = subparsers.add_parser("search", help="Search snippets by keyword or tag")
    p_search.add_argument("query", metavar="QUERY", help="Search keyword")

    # delete <id>
    p_del = subparsers.add_parser("delete",  help="Delete a snippet by ID")
    p_del.add_argument("id", type=int, metavar="ID", help="Snippet ID")

    args = parser.parse_args()

    commands = {
        "add":    cmd_add,
        "list":   cmd_list,
        "view":   cmd_view,
        "search": cmd_search,
        "delete": cmd_delete,
        "stats":  cmd_stats,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
