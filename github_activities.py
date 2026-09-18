import requests

BASE_URL = "https://api.github.com"

def get_user_events(username):
    url = f"{BASE_URL}/users/{username}/events"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"Failed to retrieve data. Error {response.status_code}")
    return None

def display_event(event):
    repo_name = event.get("repo", {}).get("name", "N/A")
    created_at = event.get("created_at", "").replace("T", " ").replace("Z", " UTC") or "N/A"
    event_type = event.get("type") or "UnknownEvent"
    payload = event.get("payload", {})

    print(f"Repo: {repo_name}")
    print(f"Time: {created_at}")

    if event_type == "PushEvent":
        commits = payload.get("commits", [])
        print(f"Commits ({len(commits)}):")
        for commit in commits:
            sha = commit.get("sha", "")[:7]
            msg = commit.get("message", "").split("\n")[0]
            print(f"  • [{sha}] {msg}")

    elif event_type == "IssuesEvent":
        action = payload.get("action", "performed action on")
        title = payload.get("issue", {}).get("title", "")
        print(f"Activity: {action.capitalize()} issue: '{title}'")

    elif event_type == "PullRequestEvent":
        action = payload.get("action", "performed action on")
        title = payload.get("pull_request", {}).get("title", "")
        print(f"Activity: {action.capitalize()} PR: '{title}'")

    elif event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "item")
        ref = payload.get("ref", "")
        print(f"Activity: Created {ref_type} {ref}".strip())

    elif event_type == "WatchEvent":
        print("Activity: Starred this repo")

    else:
        clean_name = event_type.replace("Event", "")
        print(f"Activity: {clean_name}")


username = input("Enter the username: ")
events = get_user_events(username)

if events:
    print(f"---Recent Activity for {username}---")
    for event in events[:10]:
        display_event(event)
        print(" ")