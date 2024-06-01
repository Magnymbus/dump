import os
import re
from glob import iglob

SCRIPT_PATH_RE = re.compile(r'ScriptPath\("res://(.*?\.cs)')

def get_script_path(file_path):
    with open(file_path, "r") as f:
        for line in f:
            if match := SCRIPT_PATH_RE.search(line):
                return match.group(1)
    return None

def pluralize(string):
    return f'{string[:-1]}ies' if string.endswith('y') else f'{string}s'

def validate_path(file_path):
    parts = file_path.split('\\')
    file_name = parts[-1]
    valid_path = ''
    for part in parts[:-1]:
        if part == 'Game':
            valid_path = os.path.join(valid_path, 'scripts')
        elif part != '.':
            potential_path = os.path.join(valid_path, part)
            if not os.path.exists(potential_path):
                potential_path = os.path.join(valid_path, pluralize(part))
                if not os.path.exists(potential_path):
                    raise ValueError("bad path: ", potential_path)
            valid_path = potential_path
    return os.path.join(valid_path.lower(), file_name)

files = list(iglob(os.path.join(".\\Game", '**', '*.cs'), recursive=True))
for file in files:
    new_path = get_script_path(file) or validate_path(file)
    print(f"{new_path} {'replaces existing!' if os.path.exists(new_path) else 'DOES NOT EXIST!'}")
