from __future__ import with_statement
from os import path, makedirs

def render_template(doc, env, template_path):
    template = env.get_template(template_path)
    return template.render(doc=doc, **doc.headers)

def post_directory(post, date_format="%Y/%m/%d"):
    return post.publish_directory();

def publish(doc, env, publish_dir):
    out = render_template(doc, env, doc.template)
    publish_path = path.join(publish_dir, _map[doc.type](doc))

    if not path.exists(publish_path):
        makedirs(publish_path) 

    with open(path.join(publish_path, doc.index), 'w') as f:
        f.write(out)

_map = {"post": post_directory,
        'homepage': lambda h: ""}
