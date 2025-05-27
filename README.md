# MrAgentX.github.io

This repository contains the source files for my personal website. The
`posts/` directory holds all Markdown articles. Some posts need manual
cleanup before migrating to Jekyll.

Two helper scripts are provided:

- `rename_duplicate_posts.py` &mdash; GUI tool that lists Markdown files
  whose filenames share the same slug or have an empty slug. Select a
  file and choose a new slug to rename it.
- `fix_missing_titles.py` &mdash; GUI tool that shows posts with an empty
  `title` field in their YAML front matter. You can edit the title and
  file content directly in the interface.

Run either script with Python 3 on your local machine:

```bash
python3 rename_duplicate_posts.py
python3 fix_missing_titles.py
```

Both scripts require Tkinter, which is included with most Python
installations.
