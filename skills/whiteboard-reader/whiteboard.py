#!/usr/bin/env python3
"""Read a GitHub-synced whiteboard. Stdlib only.

Config: WHITEBOARD_REPO (owner/repo) and GITHUB_TOKEN env vars,
or pass repo=/token= explicitly.
"""
import argparse
import json
import os
import sys
import urllib.request

def _cfg(repo, token):
    repo = repo or os.environ.get("WHITEBOARD_REPO", "")
    token = token or os.environ.get("GITHUB_TOKEN", "")
    if not repo:
        sys.exit("set WHITEBOARD_REPO=owner/repo (or pass --repo)")
    if not token:
        sys.exit("set GITHUB_TOKEN (Contents:read on the data repo)")
    return repo, token

def _gh(path, repo=None, token=None, raw=False):
    repo, token = _cfg(repo, token)
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.raw+json" if raw else "application/vnd.github+json",
            "User-Agent": "whiteboard-reader",
        },
    )
    with urllib.request.urlopen(req) as r:
        data = r.read()
    return data if raw else json.loads(data)

def fetch(board="board", ref="main", repo=None, token=None, out_prefix=None):
    """Download board PNG + stroke JSON; returns metadata dict."""
    out_prefix = out_prefix or f"whiteboard_{board}"
    png = _gh(f"contents/boards/{board}.png?ref={ref}", repo, token, raw=True)
    with open(f"{out_prefix}.png", "wb") as f:
        f.write(png)
    meta = json.loads(_gh(f"contents/boards/{board}.json?ref={ref}", repo, token, raw=True))
    with open(f"{out_prefix}.json", "w") as f:
        json.dump(meta, f)
    commits = _gh(f"commits?path=boards/{board}.png&per_page=1&sha={ref}", repo, token)
    c = commits[0] if commits else {}
    return {
        "board": board,
        "png_path": f"{out_prefix}.png",
        "json_path": f"{out_prefix}.json",
        "updated": meta.get("updated"),
        "n_strokes": len(meta.get("strokes", [])),
        "commit_sha": c.get("sha"),
        "commit_time": c.get("commit", {}).get("committer", {}).get("date"),
    }

def list_boards(repo=None, token=None):
    out = []
    for e in _gh("contents/boards?ref=main", repo, token):
        if e["name"].endswith(".png"):
            b = e["name"][:-4]
            commits = _gh(f"commits?path={e['path']}&per_page=1", repo, token)
            c = commits[0] if commits else {}
            out.append({"board": b, "sha": c.get("sha"),
                        "commit_time": c.get("commit", {}).get("committer", {}).get("date")})
    return out

def latest_sha(board="board", repo=None, token=None):
    commits = _gh(f"commits?path=boards/{board}.png&per_page=1", repo, token)
    return commits[0]["sha"] if commits else None

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fetch", "list", "sha"])
    ap.add_argument("--board", default="board")
    ap.add_argument("--ref", default="main")
    ap.add_argument("--repo", default=None)
    args = ap.parse_args()
    if args.cmd == "fetch":
        print(json.dumps(fetch(args.board, args.ref, args.repo), indent=2))
    elif args.cmd == "list":
        print(json.dumps(list_boards(args.repo), indent=2))
    else:
        print(latest_sha(args.board, args.repo))
