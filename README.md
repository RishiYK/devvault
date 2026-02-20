# 🔐 DevVault

> Your personal command-line code snippet manager.

Stop Googling the same snippets over and over. DevVault lets you **save, search, and retrieve** your favorite code snippets directly from the terminal — no internet, no account, no dependencies.

---

## ✨ Features

- 📝 **Add** snippets with a title, language, tags, and description
- 📋 **List** all your saved snippets at a glance
- 🔍 **Search** by keyword, language, tag, or even code content
- 👁️ **View** any snippet with syntax-colored output
- 🗑️ **Delete** snippets you no longer need
- 📊 **Stats** — see your most-used languages and tags
- 💾 Zero dependencies — uses only Python's standard library
- 🗂️ Data stored locally in `~/.devvault.json`

---

## 🚀 Getting Started

**Requirements:** Python 3.6+

```bash
# Clone or download the project
git clone https://github.com/yourusername/devvault.git
cd devvault

# Run it
python devvault.py --help
```

---

## 📖 Usage

### Add a snippet
```bash
python devvault.py add
```
You'll be prompted to enter a title, language, tags, and paste your code.

### List all snippets
```bash
python devvault.py list
```

### View a snippet (with code)
```bash
python devvault.py view 1
```

### Search snippets
```bash
python devvault.py search "list comprehension"
python devvault.py search python
python devvault.py search "#loop"
```

### Delete a snippet
```bash
python devvault.py delete 3
```

### View stats
```bash
python devvault.py stats
```

---

## 🗂️ Data Storage

All snippets are saved in a single JSON file at `~/.devvault.json`.  
You can back it up, sync it with Dropbox, or version-control it.

---

## 🛠️ Project Structure

```
devvault/
├── devvault.py   # All source code (single file, ~200 lines)
└── README.md     # You're reading it
```

---

## 💡 Ideas for Future Features

- [ ] Export snippets to Markdown
- [ ] Import from a JSON backup
- [ ] Edit existing snippets
- [ ] `--copy` flag to copy code to clipboard
- [ ] Color themes

---

## 📄 License

MIT — free to use, modify, and share.
