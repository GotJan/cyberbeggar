#!/usr/bin/env python3
"""Update README.md with hot and latest beggars from merged PRs."""
import os
import re
import json
import urllib.request

REPO = os.environ.get("GITHUB_REPOSITORY", "GotJan/cyberbeggar")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = f"https://api.github.com/repos/{REPO}"
HEADERS = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    HEADERS["Authorization"] = f"token {TOKEN}"

def api_get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())

def get_merged_prs():
    prs = api_get(f"{API}/pulls?state=closed&per_page=100")
    return [pr for pr in prs if pr.get("merged_at")]

def get_pr_reactions(pr_number):
    try:
        reactions = api_get(f"{API}/pulls/{pr_number}/reactions")
        return sum(1 for r in reactions if r.get("content") == "+1")
    except Exception:
        return 0

def get_contributor_info(pr):
    """Extract contributor name and slogan from PR files."""
    try:
        files = api_get(f"{API}/pulls/{pr['number']}/files")
        for f in files:
            if f["filename"].startswith("contributors/") and f["filename"].endswith(".md"):
                name = os.path.splitext(os.path.basename(f["filename"]))[0]
                return name
    except Exception:
        pass
    return pr["user"]["login"]

def render_hot_beggars(prs_with_votes, lang="en"):
    lines = []
    for pr, votes, name in prs_with_votes[:10]:
        badge = f"[![👍 {votes}]({pr['html_url']}#issuecomment-{pr['number']})]({pr['html_url']})"
        title = pr.get("title", "").split("\n")[0][:60]
        if lang == "zh":
            lines.append(f"| {badge} | {name} | {title} |")
        else:
            lines.append(f"| {badge} | {name} | {title} |")
    return "\n".join(lines)

def render_latest_beggars(prs, lang="en"):
    lines = []
    for pr in prs[:10]:
        name = get_contributor_info(pr)
        title = pr.get("title", "").split("\n")[0][:60]
        link = f"[{title}]({pr['html_url']})"
        lines.append(f"| [{name}]({pr['html_url']}) | {link} |")
    return "\n".join(lines)

def replace_section(content, start_marker, end_marker, new_content):
    pattern = f"({re.escape(start_marker)}\\n)({re.escape(end_marker)})"
    return re.sub(pattern, f"\\1{new_content}\n\\2", content)

def main():
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    prs = get_merged_prs()
    if not prs:
        print("No merged PRs found, skipping update.")
        return

    # Sort by merged_at descending for latest
    prs.sort(key=lambda p: p.get("merged_at", ""), reverse=True)

    # Get votes for hot ranking
    prs_with_votes = []
    for pr in prs:
        votes = get_pr_reactions(pr["number"])
        name = get_contributor_info(pr)
        prs_with_votes.append((pr, votes, name))
    prs_with_votes.sort(key=lambda x: x[1], reverse=True)

    # Render sections
    hot_en = render_hot_beggars(prs_with_votes, "en")
    hot_zh = render_hot_beggars(prs_with_votes, "zh")
    latest_en = render_latest_beggars(prs, "en")
    latest_zh = render_latest_beggars(prs, "zh")

    # Replace in README
    content = replace_section(content, "<!-- HOT_BEGGARS_START -->", "<!-- HOT_BEGGARS_END -->", hot_en)
    content = replace_section(content, "<!-- HOT_BEGGARS_ZH_START -->", "<!-- HOT_BEGGARS_ZH_END -->", hot_zh)
    content = replace_section(content, "<!-- LATEST_BEGGARS_START -->", "<!-- LATEST_BEGGARS_END -->", latest_en)
    content = replace_section(content, "<!-- LATEST_BEGGARS_ZH_START -->", "<!-- LATEST_BEGGARS_ZH_END -->", latest_zh)

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("README.md updated successfully!")

if __name__ == "__main__":
    main()
