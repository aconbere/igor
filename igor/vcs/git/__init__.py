from log import Log

class Git(object):
    def __init__(self, project_path, file_path):
        self.project_path = project_path
        self.file_path = file_path
        self.git_log = Log(self.project_path, relpath(self.file_path, self.project_path)).call()

    def published_date(self):
        return self.git_log.headers['author'].datetime

    def author(self):
        return self.git_log.headers['author'].name

    def author_email(self):
        return self.git_log.headers['author'].email
