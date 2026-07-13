from __future__ import annotations

from typing import Dict, List, Optional

from github_tools import list_open_issues


class GitHubService:
    def listar_issues(self, repo: str) -> Optional[List[Dict]]:
        if not repo:
            return None
        return list_open_issues(repo)