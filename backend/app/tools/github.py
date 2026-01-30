import requests

def fetch_github_public_data(username: str) -> dict:
    """
    Fetch basic public GitHub profile data.

    Public, unauthenticated, best-effort.
    Falls back gracefully on failure.
    """

    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github+json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return {
                "public_repos": None,
                "commit_email_exposed": None,
                "error": f"GitHub API returned {response.status_code}"
            }

        data = response.json()

        return {
            "public_repos": data.get("public_repos"),
            # heuristic placeholder; real check would require repo scan
            "commit_email_exposed": True
        }

    except Exception as e:
        return {
            "public_repos": None,
            "commit_email_exposed": None,
            "error": str(e)
        }
