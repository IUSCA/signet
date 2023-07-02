import importlib
import os

from dotenv import load_dotenv

from signet import utils
from signet.config import common

load_dotenv()  # take environment variables from .env.

env = os.environ.get('APP_ENV', None)
print(f'loading {env} conf')
if env:
    env_module = importlib.import_module(f'signet.config.{env}')
    config = utils.merge(common.config, env_module.config)
else:
    config = common.config
