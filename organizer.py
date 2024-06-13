import os
import re
from glob import iglob
import shutil

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


def replace_files(file_dict):
    for values in file_dict.values():
        shutil.copy(values['old'], values['new'])


def main():
    files = list(iglob(os.path.join(".\\Game", '**', '*.cs'), recursive=True))
    existing = {}
    new = {}
    for file in files:
        new_path = f'./{get_script_path(file) or validate_path(file)}'.replace('\\', '/')
        old_path = file.replace('\\', '/')
        script_name = new_path.split('/')[-1]
        if os.path.exists(new_path):
            existing[script_name] = {'old': old_path, 'new': new_path}
        else:
            new[script_name] = {'old': old_path, 'new': new_path}

    scripts = list(iglob(os.path.join(".\\scripts", '**', '*.cs'), recursive=True))
    repairs = {}
    unpaired = []
    for script in scripts:
        script = script.replace('\\', '/')
        script_name = script.split('/')[-1]
        if script_name in new:
            repairs[script_name] = {'old': new[script_name]['old'], 'new': script}
            del new[script_name]
        elif script_name not in existing:
            unpaired.append(script)

    if new:
        print('The following decomps were unable to be matched with scripts and may need to be manually recompiled:')
        for v in new.values():
            print(v['old'])

    if unpaired:
        print('\nThe following scripts were unable to be matched with decomps and may need to be manually recompiled:')
        for file in unpaired:
            print(file)

    replace_files(existing | repairs)


main()
