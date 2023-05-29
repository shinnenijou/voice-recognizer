import os
import myPath
from urllib.parse import urlparse
import json
import subprocess

import requests


PROXIES = None
if os.getenv('DEBUG', '0') == '1':
    PROXIES = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }


REPO_URL = "https://raw.githubusercontent.com/shinnenijou/voice-recognizer/main/"


def get_remote_dependencies():
    remote_dependencies = {}
    url = urlparse(REPO_URL + 'version.txt')

    try:
        response = requests.get(url.geturl(), proxies=PROXIES)
    except Exception as e:
        print(str(e))
        return remote_dependencies

    try:
        version_info = json.loads(response.text)
        remote_dependencies = version_info.get('dependencies', 'v0.0.0')
    except json.JSONDecodeError:
        pass

    return remote_dependencies


def make_temp_py(module_name: str):
    data = f"""
try:
    import {module_name}
    exit(0)
except ModuleNotFoundError:
    exit(-1)
"""
    file = os.path.join(myPath.TEMP_PATH, f'import_{module_name}.py')
    with open(file, 'w') as f:
        f.write(data)

    return file


def is_module_available(module_name: str):
    file = make_temp_py(module_name)
    subp = subprocess.run(f'{myPath.PYTHON_PATH} -s {file}', shell=True)
    os.remove(file)

    return subp.returncode == 0


def check_dependency(module, version=''):
    if not is_module_available(module):
        if version == '':
            subprocess.run(f"{myPath.PYTHON_PATH} -s -m pip install {module}", shell=True)
        else:
            subprocess.run(f"{myPath.PYTHON_PATH} -s -m pip install {module}=={version}", shell=True)


def check_dependencies():
    for module, version in get_remote_dependencies():
        check_dependency(module, version)
