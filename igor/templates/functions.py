from jinja2 import environmentfunction
from os import path

functions = []

@environmentfunction
def link_to(env, slug):
    docs = env.globals.get("documents")
    if docs:
        f_docs = [d for d in docs if d.slug == slug]

        if f_docs:
            return path.join(env.globals['config'].config.get("blog_uri"),
                             f_docs[0].publish_directory())
    return ""
functions.append(link_to)
