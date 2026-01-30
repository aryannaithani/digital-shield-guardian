import requests

PLATFORMS = {
    "GitHub": "https://github.com/{username}",
    "Reddit": "https://www.reddit.com/user/{username}",
    "Dev.to": "https://dev.to/{username}",
    "Medium": "https://medium.com/@{username}",
    "Twitter": "https://twitter.com/{username}"
}


def check_username_reuse(username: str) -> dict:
    """
    Check username reuse across major platforms using existence checks.

    - No auth
    - No scraping
    - Best-effort, fail-safe
    """

    found_platforms = []

    headers = {
        "User-Agent": "DigitalFootprintRiskAgent"
    }

    for platform, url_template in PLATFORMS.items():
        url = url_template.format(username=username)

        try:
            resp = requests.get(url, headers=headers, timeout=8, allow_redirects=True)

            # Heuristic:
            # 200 -> exists
            # 404 -> does not exist
            # 429/403 -> skip quietly
            if resp.status_code == 200:
                found_platforms.append(platform)

        except Exception:
            # Ignore platform failures completely
            continue

    return {
        "value": username,
        "reuse_count": len(found_platforms),
        "platforms": found_platforms
    }


