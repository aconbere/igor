from __future__ import with_statement

from os import path
import yaml

class Config(dict):
    config_path = "_config.yaml"

    defaults = {
                "author": "",
                "email": "author@example.com",
                "blog_title": "Welcome to Igor",
                "publish_directory": "~/blog",
                "blog_url": "http://example.com/",
                "media_url": "http://media.blog.com",
                "summary_length": 0,
               }

    def __init__(self, project_path):
        self.project_path = project_path
        config_path = path.join(self.project_path, self.config_path)
        self.data = self.defaults

        if path.exists(config_path):
            self.data.update(self.read(config_path))
        else:
            self.write(self.config_path)

        super(Config, self).__init__(self.defaults)

    def read(self, filename):
        try:
            with open(filename, 'r') as f:
                return yaml.load(f.read())
        except IOError:
            return {}

    def write(self, filename):
        with open(self.config_path, 'w') as f:
            f.write(yaml.dump(self.data, default_flow_style=False))
