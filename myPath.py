from os.path import join, dirname

ROOT_PATH = dirname(__file__)
RES_PATH = join(ROOT_PATH, 'res')
ENV_PATH = join(ROOT_PATH, 'env')
TEMP_PATH = join(ROOT_PATH, '.temp')
PYTHON_PATH = join(ENV_PATH, 'python.exe')
MODEL_PATH = join(RES_PATH, 'model')
SCRIPTS_PATH = join(RES_PATH, 'scripts')
CONFIG_FILE = join(ROOT_PATH, 'config.ini')
