from log import Log

class Git(object):
    def __init__(self, project_path, file_path):
        self.project_path = project_path
        self.file_path = file_path
        self.relpath = relpath(self.project_path, self.filename)
        self.headers, self.comment = Log(self.project_path).call(self.relpath)

    def published_date(self):
        return self.headers['datetime'].datetime

    def author_email(self):
        return self.headers['email'].name

    def email(self):
        return self.headers['author'].email

    def data(self):
        return {'email': self.email(),
                'author': self.author_email(),
                'published_date': self.published_date()}
