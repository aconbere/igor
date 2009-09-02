class Git(object):
    def __init__(self, project_path, file_path)
        self.project_path = project_path
        self.git_log = Log(self.project_path, relpath(self.ref, self.project_path)).call()

    def published_date():
        pass

    def author():
        return self.git_log.headers['author'].name

    def author_email():
        return self.git_log.headers['author'].email
