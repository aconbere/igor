from __future__ import with_statement

from os import path
import yaml

class Config(dict):
    """
    The config class captures the config state of Igor, this is primarily used
    for reading in the config yaml and creating the various paths used by igor
    to extract posts, templates, etc.
    """

    config_file = "_config.yaml"

    defaults = {
                "author": "author",
                "email": "author@example.com",
                "blog_title": "Welcome to Igor",
                "publish_directory": "~/blog",
                "posts_prefix": "",
                "blog_url": "http://example.com/",
                "media_url": "http://media.blog.com",
                "summary_length": 0,
                "templates_prefix" = "_templates",
                "posts_prefix" = "_posts",
               }

    def __init__(self, source, destination):
        self.data = self.defaults

        self.source = self.abspath(source)
        self.data.update(self.read(path.join(self.source, self.config_file)))
        self.destination = self.data['publish_directory'] or self.abspath(destination)
        self.data['publish_directory'] = self.destination
        self.posts_dir = path.join(self.source, self.posts_prefix),
        self.templates_dir = path.join(self.source, self.templates_prefix),

        super(Config, self).__init__(self.data)

    def abspath(self, path):
        return path.abspath(path.expanduser(path))

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
            f.write(yaml.dump(self.data, default_flow_style=False))
