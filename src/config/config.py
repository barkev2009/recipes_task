import yaml
import pathlib
import os

path = pathlib.Path(__file__).parent
with open(os.path.join(path, 'config.yaml')) as file:
    config = yaml.safe_load(file)
