from utils import slugify
from os import path, makedirs

summary_length = 30

class HomePage(object):
    default_template = "main.html"
    default_out_filename = "index.html"

    def __init__(self, posts, context = {}):
        self.context = {}
        self.posts = posts
        self.cached_output = None

    def render(self, env, template = None):
        template = template or self.context.get(template) or self.default_template
        t = env.get_template(template)
        self.cached_output = t.render(posts=self.posts, **self.context)
        return self.cached_output

    def out_file_path(self, out_dir):
        return path.join(out_dir, self.default_out_filename)

    def write(self, env, out_dir, template=None):
        out = self.cached_output or self.render(env, template)

        if not path.exists(out_dir):
            makedirs(out_dir)

        out_file_path = self.out_file_path(out_dir)
        with open(self.out_file_path(out_dir), 'w') as f:
            print("publishing %s" % path.relpath(out_file_path, out_dir))
            f.write(out)
        return self
        
            
        

class Post(object):
    default_template = "post.html"
    default_out_filename = "index.html"

    def __init__(self, title="", content="", published_on = None,
                 last_modified = None, slug = "", context = {}, filename=""):
        self.title = title
        self.content = content
        self.published_on = published_on
        self.last_modified = last_modified
        self.filename = filename
        self.slug = slug or slugify(title) or slugify(filename)
        self.context = context
        self.cached_output = None

    def render(self, env, template = None):
        template = template or self.context.get(template) or self.default_template
        t = env.get_template(template)
        self.cached_output =  t.render(post=self, **self.context)
        return self.cached_output

    def out_file_dir(self, out_dir=None):
        date_path = self.published_on.strftime("%Y/%m/%d/")

        if out_dir:
            return path.join(out_dir, date_path, self.slug)

        return path.join(date_path, self.slug)

    def out_file_path(self, out_dir=None):
        return path.join(self.out_file_dir(out_dir), self.default_out_filename)

    def write(self, env, out_dir, template = None):
        out = self.cached_output or self.render(env, template)
        out_file_dir = self.out_file_dir(out_dir)

        if not path.exists(out_file_dir):
            makedirs(out_file_dir)

        out_file_path = self.out_file_path(out_dir)
        with open(out_file_path, 'w') as f:
            print("publishing %s" % path.relpath(out_file_path, out_dir))
            f.write(out)
        return self
