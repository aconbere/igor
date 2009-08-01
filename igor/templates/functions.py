from jinja2 import environmentfunction
from os import path

functions = []

@environmentfunction
def link_to(env, slug):
    posts = env.globals.get("posts")
    if posts:
        f_posts = [p for p in posts if p.slug == slug]

        if f_posts:
            return path.join(env.globals['config'].config.get("blog_uri"),
                             f_posts[0].publish_directory())
    return ""
functions.append(link_to)
