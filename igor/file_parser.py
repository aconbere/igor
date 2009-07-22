from os import path
from datetime import datetime

import yaml

from git_wrapper.log import Log
from post import Post

class FileParser(object):
    default_template = "post.html"
    index = "index.html"

    def __init__(self, project_path, relative_file_path):
        """
            file_path is relative to project_path
        """
        self.project_path = project_path
        self.relative_file_path = relative_file_path

        _, self.filename = path.split(relative_file_path)

        self.file_path = path.join(self.project_path, self.relative_file_path)

    def _pop_section(self, fd):
        section = ""
        l = fd.readline()

        while l != "\n":
            section += l
            l = fd.readline()

        return section.strip() 

    def parse_header(self, header):
        return yaml.load(header)

    def get_published_date(self, data):
        datestr = data.get("published_on")

        if datestr:
            return datetime.strptime(datestr, "%Y-%m-%d")

        else:
            l = Log(self.project_path, self.relative_file_path)
            headers = l.call().headers
            return l.call().headers["author"].datetime
            

    def parse(self):
        file_dir, filename = path.split(self.file_path)
        data = {}

        with open(self.file_path, 'r') as f:
            data = {}
            top = self._pop_section(f)
            title = top

            if ":" in top:
                data = self.parse_header(top)
                title = data.get("title") or self._pop_section(f)

            return Post(title = title,
                        published_on = self.get_published_date(data),
                        last_modified = datetime.now(),
                        filename = filename,
                        content = f.read().strip(),
                        context = data)
