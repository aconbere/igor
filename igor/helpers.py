from jinja.datastructure import contextcallable


def do_link_to(slug = u''):
    def link_to(env, context, slug):
        posts = env.globals.get("posts")
        if posts:
            f_posts = [p for p in posts if p.slug == slug]

            if f_posts:
                return f_posts[0].out_file_dir()
        return ""
    return link_to
