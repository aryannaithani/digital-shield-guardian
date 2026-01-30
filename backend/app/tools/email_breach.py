import requests

def check_email_breach_leakcheck(email: str) -> dict:
    """
    Check email exposure using LeakCheck public API.

    Uses publicly available breach data.
    No API key required.
    Fails gracefully.
    """

    url = f"https://leakcheck.net/api/public?check={email}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return {
                "found_in_breaches": None,
                "breach_sources": [],
                "error": f"LeakCheck returned {response.status_code}"
            }

        data = response.json()

        # LeakCheck response format can vary slightly, so be defensive
        found = bool(data.get("found", False))
        sources = []

        if found:
            # Try to extract source names if present
            sources = data.get("sources", [])
            if not isinstance(sources, list):
                sources = []

        return {
            "found_in_breaches": found,
            "breach_sources": sources
        }

    except Exception as e:
        return {
            "found_in_breaches": None,
            "breach_sources": [],
            "error": str(e)
        }
