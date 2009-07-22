from utils import slugify
from os import path, makedirs
from content_processor import BasicProccessor

class Page(object):
    default_template = "post.html"
    default_out_filename = "index.html"

    def __init__(self, context = {}):
        self.context = context
        self.cached_output = None

    def render(self, env, template=None):
        template = template or self.context.get(template) or self.default_template
        t = env.get_template(template)
        self.cached_output = t.render(**self.context)
        return self.cached_output

    def out_file_path(self):
        return self.default_out_filename

    def out_file_dir(self):
        return ""

    def write(self, env, out_dir, template = None):
        out = self.cached_output or self.render(env, template)
        out_file_dir = path.join(out_dir, self.out_file_dir())

        if not path.exists(out_file_dir):
            makedirs(out_file_dir)

        self.file_path = path.join(out_dir, self.out_file_path())
        with open(self.file_path, 'w') as f:
            print("publishing %s" % self.file_path)
            f.write(out)
        return self

class HomePage(Page):
    default_template = "main.html"

    def __init__(self, posts, context = {}):
        super(HomePage, self).__init__()
        self.posts = posts
        self.context['posts'] = self.posts

class Post(Page):
    content_processor = BasicProccessor

    def __init__(self, title="", content="", slug="", published_on=None,
                 last_modified=None, filename="", context={}):
        super(Post, self).__init__(context)

        self.title = title

        self.content = self.apply_content_processor(content)
        self.published_on = published_on
        self.last_modified = last_modified
        self.filename = filename
        self.slug = slug or slugify(title) or slugify(filename)

        self.context["post"] = self

    def apply_content_processor(self, content):
        if self.content_processor:
            content = self.content_processor(content).render()
        return content

    def out_file_dir(self):
        date_path = self.published_on.strftime("%Y/%m/%d/")
        return path.join(date_path, self.slug)

    def out_file_path(self):
        return path.join(self.out_file_dir(), self.default_out_filename)
