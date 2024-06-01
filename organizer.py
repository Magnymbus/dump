import os
import re
import shutil

def list_files_recursive(path='.'):
    files = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if os.path.isdir(full_path):
            files.extend(list_files_recursive(full_path))
        else:
            if entry.endswith('.cs'):
                files.append(full_path)
    return files

def getScriptPath(file):
    with open(file, "r") as f:
        contents = f.read()
        repl = re.compile(r'ScriptPath\("res://(.*?\.cs)')
        match = re.search(repl, contents)
        if match:
            return match.group(1)

def validatePath(file):
    dirs = file.split('\\')
    newPath = ''
    for dir in dirs:
        if dir == ".":
            continue
        elif dir == "Game":
            newPath = newPath + 'cripts/'
        elif dir.endswith('.cs'):
            newPath = newPath + dir
        else:
            newPath = newPath + dir.lower()
            if not os.path.exists(newPath):
                trypath = newPath.lower()
                if trypath.endswith('y'):
                    trypath = trypath[:-1]+"ies/"
                else:
                    trypath = trypath + "s/"
                if not os.path.exists(trypath):
                    trypath = newPath.lower() + '/'
                    if not os.path.exists(trypath):
                        raise ValueError("bad path: ", trypath)
                    else:
                        newPath = trypath
                else:
                    newPath = trypath
            else:
                newPath = newPath + '/'
    return newPath

directory_path = ".\\Game"
files = list_files_recursive(directory_path)
for file in files:
    newPath = getScriptPath(file)
    if not newPath:
        newPath = validatePath(file)
    if not os.path.exists(newPath):
        print(newPath, " DOES NOT EXIST!")