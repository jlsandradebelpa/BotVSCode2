from __future__ import annotations

import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from typing import Dict, List, Optional

GITHUB_API = "https://api.github.com"


def list_open_issues(repo: str) -> Optional[List[Dict]]:
    issues = _list_open_issues_with_gh(repo)
    if issues is not None:
        return issues
    return _list_open_issues_with_api(repo)


def _list_open_issues_with_gh(repo: str) -> Optional[List[Dict]]:
    if shutil.which("gh") is None:
        return None
    cmd = [
        "gh",
        "issue",
        "list",
        "--repo",
        repo,
        "--state",
        "open",
        "--limit",
        "30",
        "--json",
        "number,title,labels,state,url",
    ]
    try:
        kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20, **kwargs)
        if result.returncode != 0:
            return None
        data = json.loads(result.stdout)
        return [_normalize_gh_issue(issue) for issue in data]
    except (json.JSONDecodeError, OSError, subprocess.SubprocessError):
        return None


def _normalize_gh_issue(issue: Dict) -> Dict:
    labels = issue.get("labels") or []
    return {
        "number": issue.get("number"),
        "title": issue.get("title"),
        "state": issue.get("state"),
        "url": issue.get("url"),
        "labels": labels,
    }


def _list_open_issues_with_api(repo: str) -> Optional[List[Dict]]:
    url = f"{GITHUB_API}/repos/{repo}/issues?state=open&per_page=30&sort=created&direction=desc"
    headers = {
        "User-Agent": "BotVSCode/0.1.0",
        "Accept": "application/vnd.github.v3+json",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status != 200:
                return None
            data = json.loads(resp.read().decode("utf-8"))
            return [issue for issue in data if "pull_request" not in issue]
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, OSError):
        return None
