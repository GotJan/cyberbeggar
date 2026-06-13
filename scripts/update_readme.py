#!/usr/bin/env python3
"""Update README.md with hot and latest beggars via Issue reactions."""
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


def api_get_all(url):
    """Paginate through all results."""
    results = []
    page = 1
    while True:
        sep = "&" if "?" in url else "?"
        page_url = f"{url}{sep}page={page}&per_page=100"
        data = api_get(page_url)
        if not data:
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results


def get_beggar_issues():
    """Get all open issues labeled 'beggar'."""
    issues = api_get_all(f"{API}/issues?labels=beggar&state=open")
    return issues


def get_issue_reactions(issue_number):
    """Count +1 reactions on an issue."""
    try:
        # Reactions API requires authentication; GITHUB_TOKEN is available in Actions
        reactions_url = f"{API}/issues/{issue_number}/reactions"
        req = urllib.request.Request(reactions_url, headers={
            **HEADERS, "Accept": "application/vnd.github.squirrel-girl-preview+json"
        })
        with urllib.request.urlopen(req) as resp:
            reactions = json.loads(resp.read())
        return sum(1 for r in reactions if r.get("content") == "+1")
    except Exception as e:
        print(f"Warning: could not fetch reactions for issue #{issue_number}: {e}")
        return 0


def render_hot_beggars(issues_with_votes, lang="en"):
    """Render hot beggars table including header — markers wrap the whole table."""
    if lang == "zh":
        lines = ["| 👍 | 乞丐 | 口号 |", "|----|------|------|"]
    else:
        lines = ["| 👍 | Beggar | Slogan |", "|----|--------|--------|"]
    for issue, votes in issues_with_votes[:10]:
        badge_url = issue["html_url"]
        title = issue.get("title", "").split("\n")[0][:60]
        author = issue["user"]["login"]
        lines.append(
            f"| [![👍 {votes}]({badge_url})]({badge_url}) "
            f"| [{author}]({issue['user']['html_url']}) "
            f"| {title} |"
        )
    return "\n".join(lines)


def render_latest_beggars(issues, lang="en"):
    """Render latest beggars table including header — markers wrap the whole table."""
    if lang == "zh":
        lines = ["| 乞丐 | 口号 |", "|------|------|"]
    else:
        lines = ["| Beggar | Slogan |", "|--------|--------|"]
    for issue in issues[:10]:
        author = issue["user"]["login"]
        title = issue.get("title", "").split("\n")[0][:60]
        lines.append(
            f"| [{author}]({issue['user']['html_url']}) "
            f"| [{title}]({issue['html_url']}) |"
        )
    return "\n".join(lines)


def replace_section(content, start_marker, end_marker, new_content):
    """Replace content between markers, works even if old content exists."""
    pattern = f"({re.escape(start_marker)})(.*?)({re.escape(end_marker)})"
    replacement = f"\\1\n{new_content}\n\\3"
    return re.sub(pattern, replacement, content, flags=re.DOTALL)


def main():
    readme_path = "README.md"
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    issues = get_beggar_issues()
    if not issues:
        print("No beggar issues found, skipping update.")
        return

    # Sort by creation date descending for latest
    issues.sort(key=lambda i: i.get("created_at", ""), reverse=True)

    # Get votes for hot ranking
    issues_with_votes = []
    for issue in issues:
        votes = get_issue_reactions(issue["number"])
        issues_with_votes.append((issue, votes))
    issues_with_votes.sort(key=lambda x: x[1], reverse=True)

    # Render sections (each includes table header)
    hot_en = render_hot_beggars(issues_with_votes, "en")
    hot_zh = render_hot_beggars(issues_with_votes, "zh")
    latest_en = render_latest_beggars(issues, "en")
    latest_zh = render_latest_beggars(issues, "zh")

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
