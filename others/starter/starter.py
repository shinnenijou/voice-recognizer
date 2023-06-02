import os
import subprocess

cur_path = os.path.dirname(__file__)
python_file = os.path.abspath(os.path.join(cur_path, 'env', 'python.exe'))
main_file = os.path.abspath(os.path.join(cur_path, 'main.py'))


while True:
    subp = subprocess.run(f'{python_file} -s {main_file}', shell=True)
    if subp.returncode != 100:
        break
