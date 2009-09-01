from __future__ import with_statement

from os import path
import yaml

class Config(object):
    """
    The config class captures the config state of Igor, this is primarily used
    for reading in the config yaml and creating the various paths used by igor
    to extract posts, templates, etc.
    """

    config_file = "_config.yaml"

    defaults = {
                "author": "John Doe",
                "email": "jdoe@example.com",
                "blog_title": "Welcome to Igor",
                "destination": "/tmp/igor",
                "publish_prefix": "",
                "blog_url": "http://example.com/",
                "media_url": "http://media.example.com/",
                "summary_length": 10,
                "templates_prefix": "_templates",
                "posts_prefix": "_posts",
               }

    def __init__(self, source, destination=""):
        self._data = self.defaults

        self.source = self.abspath(source)

        self._data.update(self.read(path.join(self.source,
                                              self.config_file)))

        if destination:
            self._data['destination'] = self.abspath(destination)
        elif self._data['destination']:
            self._data['destination'] = self.abspath(self._data['destination'])
        else:
            self._data['destination'] = self.abspath("")

        self.publish_dir = path.join(self._data['destination'],
                                     self._data['publish_prefix'])

        self.posts_dir = path.join(self.source,
                                   self._data['posts_prefix']),

        self.templates_dir = path.join(self.source,
                                       self._data['templates_prefix']),

    def data(self):
        return dict(source = self.source,
                    publish_dir = self.publish_dir,
                    posts_dir = self.posts_dir,
                    templates_dir = self.templates_dir,
                    **self._data)

    def abspath(self, p):
        return path.abspath(path.expanduser(p))

    def read(self, filename):
        try:
            with open(filename, 'r') as f:
                return yaml.load(f.read())
        except IOError:
            raise Exception("No config file found: %s" % filename)

    def write(self, filename):
        """
        Writes out the current data as a config file. Mostly used to write out
        the default config file if none is found.
        """
        with open(self.config_path, 'w') as f:
            f.write(yaml.dump(self._data, default_flow_style=False))
