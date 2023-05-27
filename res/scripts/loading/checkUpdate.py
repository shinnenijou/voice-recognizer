import os
import shutil
import configparser
import zipfile
from urllib.parse import urlparse
import requests
import json

import myPath

NOT_COPY_LIST = [
    ".gitignore",
    ".gitattributes",
]

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


def get_remote_version():
    version = [0, 0, 0]
    url = urlparse("https://raw.githubusercontent.com/shinnenijou/voice-recognizer-res/main/version.txt")
    try:
        response = requests.get(url.geturl(), proxies=PROXIES)
    except Exception as e:
        print(str(e))
        return version

    try:
        version_info = json.loads(response.text)
        version = parse_version(version_info.get('version', '0.0.0'))
    except json.JSONDecodeError:
        pass

    return version


def download_release(version):
    version = encode_version(version)
    url = urlparse(f"https://github.com/shinnenijou/voice-recognizer-res/archive/refs/tags/v{version}.zip")

    file = os.path.join(myPath.TEMP_PATH, os.path.basename(url.path))
    try:
        response = requests.get(url.geturl(), proxies=PROXIES)
        with open(file, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(str(e))

    return file


def check_update():
    if not os.path.exists(myPath.CONFIG_FILE):
        file = open(myPath.CONFIG_FILE, 'w')
        file.write('[global]\n')
        file.close()

    config = configparser.RawConfigParser()
    config.read(myPath.CONFIG_FILE)

    local_version = parse_version(config['global'].get('version', '0.0.0'))
    remote_version = get_remote_version()

    if local_version < remote_version:
        archive = download_release(remote_version)
        if os.path.exists(archive):
            z = zipfile.ZipFile(archive, "r")
            if not os.path.exists(myPath.RES_PATH):
                os.mkdir(myPath.RES_PATH)

            dir_name = os.path.dirname(z.namelist()[0])
            z.extractall(os.path.dirname(archive))
            files = os.listdir(myPath.join(os.path.dirname(archive), dir_name))
            for file in files:
                if os.path.basename(file) in NOT_COPY_LIST:
                    continue

                src_path = myPath.join(os.path.dirname(archive), dir_name, file)
                dst_path = myPath.join(myPath.RES_PATH, file)
                if os.path.isdir(src_path):
                    shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
                else:
                    shutil.copy(src_path, dst_path)

            z.close()

            config.set('global', 'version', encode_version(remote_version))
            with open(myPath.CONFIG_FILE, 'w') as f:
                config.write(f)

            os.remove(archive)
            shutil.rmtree(myPath.join(os.path.dirname(archive), dir_name))
