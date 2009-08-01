from __future__ import with_statement
from os import path, makedirs

def render_template(doc, env, template_path):
    template = env.get_template(template_path)
    return template.render(doc=doc, **doc.headers)

def publish(doc, env, publish_dir):
    out = render_template(doc, env, doc.template)
    publish_dir = path.join(publish_dir, doc.publish_directory())

    if not path.exists(publish_dir):
        makedirs(publish_dir) 

    publish_path = path.join(publish_dir, doc.index)

    print("... publishing: %s to %s" % (doc.slug, publish_path))

    with open(publish_path, 'w') as f:
        f.write(out)
