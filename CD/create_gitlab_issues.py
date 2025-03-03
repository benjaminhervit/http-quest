import requests
import os

GITLAB_API_URL = 'https://gitlab.com/api/v4'
GITLAB_PROJECT_ID = '19560'
GITLAB_ACCESS_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN')

def create_issue(title, description):
    url = f"{GITLAB_API_URL}/projects/{GITLAB_PROJECT_ID}/issues"
    headers = {
        'Private-Token': GITLAB_ACCESS_TOKEN
    }
    data = {
        'title': title,
        'description': description
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 201:
        print(f"Issue created: {title}")
    else:
        print(f"Failed to create issue: {response.content}")

if __name__ == '__main__':
    from CD.scan_todos import find_todos

    todos = find_todos('.')
    for todo in todos:
        title = f"TODO in {todo['file']} at line {todo['line']}"
        description = todo['comment']
        create_issue(title, description)