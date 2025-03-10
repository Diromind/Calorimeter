import os
import yaml

def __read_config__(cache={'content':None}) -> dict:
    if not cache['content']:
        config_path = os.path.join(os.environ["HOME"], "calorimeter/config.yaml")
        with open(config_path, "r") as f:
            cache['content'] = yaml.safe_load(f)
    return cache['content']

def get_config_value(key: str):
    config = __read_config__()
    if key not in config:
        return None
    return config[key]



