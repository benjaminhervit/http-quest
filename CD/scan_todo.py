import os
import re

def find_todos(directory):
    todos = []
    todo_pattern = re.compile(r'#\s*TODO:(.*)')

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.html', '.js', '.css')):  # Add other file extensions as needed
                with open(os.path.join(root, file), 'r') as f:
                    for line_number, line in enumerate(f, start=1):
                        match = todo_pattern.search(line)
                        if match:
                            todos.append({
                                'file': os.path.join(root, file),
                                'line': line_number,
                                'comment': match.group(1).strip()
                            })
    return todos

if __name__ == '__main__':
    todos = find_todos('.')
    for todo in todos:
        print(f"{todo['file']}:{todo['line']} - {todo['comment']}")