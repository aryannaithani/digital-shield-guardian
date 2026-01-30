from app.tools.email_breach import check_email_breach_leakcheck
from app.tools.github import fetch_github_public_data
from app.tools.username_reuse import check_username_reuse


def information_gathering_agent(planner_output: dict) -> dict:
    tasks = planner_output.get("tasks", [])
    inputs = planner_output.get("normalized_input", {})

    evidence = {}

    # ---- Email breach intelligence (LeakCheck – REAL DATA) ----
    if "check_breach_exposure" in tasks and "email" in inputs:
        breach_data = check_email_breach_leakcheck(inputs["email"])

        evidence["email"] = {
            "value": inputs["email"],
            "found_in_breaches": breach_data.get("found_in_breaches"),
            "breach_sources": breach_data.get("breach_sources", [])
        }

    # ---- GitHub public data (already integrated) ----
    if "analyze_github_public_data" in tasks and "username" in inputs:
        username = inputs["username"].rstrip("/").split("/")[-1]
        github_data = fetch_github_public_data(username)

        evidence["github"] = {
            "username": username,
            "public_repos": github_data.get("public_repos"),
            "commit_email_exposed": github_data.get("commit_email_exposed")
        }

        # ---- Username reuse detection (REAL TOOL) ----
    if "check_username_reuse" in tasks and "username" in inputs:
        username_data = check_username_reuse(inputs["username"])

        evidence["username"] = {
            "value": username_data["value"],
            "reuse_count": username_data["reuse_count"],
            "platforms": username_data["platforms"]
        }


    return evidence
