import yaml

class Config(object):
    defaults = {"summary_length": 0,
                "output_directory": "~blog"}
                "config_path": "_config.yaml"}

    def __init__(self, project_path):
        config_path = path.join(project_path, defaults['config_path'])
        self.project_path = project_path

        if path.exists(default_config_path):
            self.config = defauls.update(self.read(config_path))
        else:
            self.config = defaults

    def read(self, filename):
        with open(filename, 'r') as f:
            return yaml.load(f.read())
