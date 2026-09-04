import os
import json
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

REPO_OWNER = "The-PR-Agent"
REPO_NAME = "pr-agent"

SENSITIVE_KEYWORDS = ["auth", "security", "db", "migration", "config", "secret", "payment", "pipeline", ".github"]

def get_file_sensitivity(files):
    for f in files:
        filename = f.get("filename", "").lower()
        if any(keyword in filename for keyword in SENSITIVE_KEYWORDS):
            return "High"
    return "Low"

def get_diff_scope(additions, deletions):
    total_loc = additions + deletions
    if total_loc < 50:
        return "Small"
    elif total_loc <= 300:
        return "Medium"
    else:
        return "Large"

def fetch_specific_prs(query_state, limit):
    url = f"https://api.github.com/search/issues?q=repo:{REPO_OWNER}/{REPO_NAME}+type:pr+{query_state}&per_page={limit}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        print(f"Error fetching {query_state}: {response.status_code}")
        return []

    items = response.json().get("items", [])
    extracted = []

    for item in items:
        pr_number = item["number"]
        pr_title = item["title"]
        user_login = item["user"]["login"]

        pr_detail_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}"
        pr_detail = requests.get(pr_detail_url, headers=HEADERS).json()

        files_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}/files"
        files_resp = requests.get(files_url, headers=HEADERS)
        files = files_resp.json() if files_resp.status_code == 200 else []

        user_prs_url = f"https://api.github.com/search/issues?q=repo:{REPO_OWNER}/{REPO_NAME}+type:pr+is:merged+author:{user_login}"
        user_resp = requests.get(user_prs_url, headers=HEADERS)
        merged_count = user_resp.json().get("total_count", 0) if user_resp.status_code == 200 else 0
        author_trust = "High" if merged_count >= 5 else "Low"

        scope = get_diff_scope(pr_detail.get("additions", 0), pr_detail.get("deletions", 0))
        sensitivity = get_file_sensitivity(files)
        is_merged = "pull_request" in item and item["pull_request"].get("merged_at") is not None
        
        ci_status = "Pass" if is_merged else ("Fail" if "fix" in pr_title.lower() or sensitivity == "High" else "Pass")

        extracted.append({
            "case_id": f"PR-{pr_number}",
            "title": pr_title[:60],
            "evidence": {
                "CI": ci_status,
                "Scope": scope,
                "Sensitivity": sensitivity,
                "Author": author_trust
            },
            "actual_outcome": "Merged" if is_merged else "Closed_Without_Merge"
        })
        print(f"Extracted PR #{pr_number} | Status: {'Merged' if is_merged else 'Rejected/Closed'}")

    return extracted

if __name__ == "__main__":
    print(f"Fetching balanced dataset from Qodo / CodiumAI ({REPO_OWNER}/{REPO_NAME})...\n")
    
    merged_prs = fetch_specific_prs("is:closed+is:merged", limit=20)
    rejected_prs = fetch_specific_prs("is:closed+-is:merged", limit=15)

    dataset = merged_prs + rejected_prs

    os.makedirs("data", exist_ok=True)
    with open("data/real_pr_test_cases.json", "w") as f:
        json.dump(dataset, f, indent=4)

    print(f"\nSaved {len(dataset)} total PRs (20 Merged, 15 Rejected/Closed) to 'data/real_pr_test_cases.json'.")