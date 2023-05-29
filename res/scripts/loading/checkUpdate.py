import os
import shutil
import configparser
from urllib.parse import urlparse
import requests
import json

import myPath
from res.scripts.config import config

REPO_URL = "https://raw.githubusercontent.com/shinnenijou/voice-recognizer/main/"

PROXIES = None
if os.getenv('DEBUG', '0') == '1':
    PROXIES = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890',
    }


def parse_version(string: str):
    temp = []

    for segment in string.split('.'):
        temp.append(int(segment))

    return temp


def encode_version(version: list[int]):
    temp = []

    for i in range(len(version)):
        temp.append(str(version[i]))

    return '.'.join(temp)


def get_remote_file(remote_path:str, local_dir: str):
    file = ''
    url = urlparse(REPO_URL + remote_path)
    try:
        response = requests.get(url.geturl(), proxies=PROXIES)
    except Exception as e:
        print(str(e))
        return file

    if response.status_code == 200:
        file = os.path.join(local_dir, url.path.split('/')[-1])
        os.makedirs(local_dir, exist_ok=True)
        with open(file, 'wb') as f:
            f.write(response.content)

    return file


def get_remote_version():
    version = [0, 0, 0]
    update_files = {}
    file = os.path.join(myPath.TEMP_PATH, 'version.txt')
    if not os.path.exists(file):
        file = get_remote_file("version.txt", myPath.TEMP_PATH)

    if file == '':
        return version, update_files

    try:
        with open(file, 'r', encoding='utf-8') as f:
            version_info = json.loads(f.read())
            version = parse_version(version_info.get('version', '0.0.0'))
            update_files = version_info.get('update_files', {})
        os.remove(file)
    except json.JSONDecodeError:
        pass

    return version, update_files


def check_update():
    local_version = parse_version(config['global'].get('version', '0.0.0'))
    remote_version, update_files = get_remote_version()

    if local_version < remote_version:
        complete_flag = True
        dst_map = {}

        for remote_file, local_dir in update_files.items():
            temp_file = get_remote_file(remote_file, myPath.TEMP_PATH)
            if temp_file != '':
                abs_dst = os.path.join(myPath.ROOT_PATH, local_dir)
                dst_map[temp_file] = abs_dst
            else:
                complete_flag = False
                break

        if complete_flag:
            for src, dst in dst_map.items():
                if not os.path.exists(dst):
                    os.makedirs(dst, exist_ok=True)

                shutil.copy(src, dst)
                os.remove(src)

            local_version = remote_version

    config.set('global', 'version', encode_version(local_version))
    config.save()
