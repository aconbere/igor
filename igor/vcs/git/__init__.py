from log import Log

from igor.utils import relpath

class Git(object):
    def __init__(self, project_path, file_path):
        self.project_path = project_path
        self.file_path = file_path
        self.relpath = relpath(self.file_path, self.project_path)
        self.headers, self.comment = Log(self.project_path).call(self.relpath)
        print(self.headers)

    def published_date(self):
        return self.headers['author'].datetime

    def author(self):
        return self.headers['author'].name

    def author_email(self):
        return self.headers['author'].email

    def data(self):
        return {'email': self.author_email(),
                'author': self.author(),
                'published_date': self.published_date()}
