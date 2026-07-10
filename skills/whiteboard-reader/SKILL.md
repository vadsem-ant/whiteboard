---
name: whiteboard-reader
description: Read a GitHub-synced whiteboard (drawn on an iPad via the companion web app). Use when the user says "check the whiteboard", "look at my sketch/drawing", or references something they drew. Fetches the board PNG (view it) and stroke JSON from the user's data repo.
---

# Whiteboard reader

The user draws on the companion web app and taps **Sync**, which commits
`boards/<name>.png` (rendered image) and `boards/<name>.json` (strokes) to a
GitHub data repo of their choosing (usually private). Default board name:
`board`.

## Configuration

Two values, from environment or by asking the user once:

- `WHITEBOARD_REPO` — data repo as `owner/repo`
- `GITHUB_TOKEN` — any token with Contents:read on that repo

## Reading the board

Use `whiteboard.py` next to this file (stdlib only, Python 3.8+):

```bash
python whiteboard.py fetch                 # -> whiteboard_board.png + .json in cwd
python whiteboard.py fetch --board=notes   # named board
python whiteboard.py list                  # boards + last-modified
python whiteboard.py sha                   # latest commit sha touching the board (cheap poll)
```

Or import: `from whiteboard import fetch, list_boards, latest_sha`.

Then **view the PNG** — that is the primary interface; read handwriting and
diagrams visually. The stroke JSON (`strokes: [{color, width, eraser,
pts: [[x,y,pressure],...]}]`, world coordinates) is for programmatic needs
only (replay, diffing, cropping).

## Live session ("watch the board")

Poll `sha` every ~10 s; on change, `fetch` and view the new PNG. Remind the
user to tap **Sync** after each change — nothing arrives without it.

## Notes

- Each Sync is a commit: history = board versions (`fetch --ref=<sha>`).
- 404 on fetch: board name may differ — run `list`.
- The PNG is a crop to the ink's bounding box; coordinates in the JSON are
  the authoritative geometry.
