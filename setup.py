from distutils.core import setup

setup(name="igor",
      version="1.0",
      author="Anders Conbere",
      author_email = "aconbere@conbere.org",
      license = "bsd",
      packages=["igor", "igor.vcs", "igor.vcs.git", "igor.vcs.hg"],
      package_data=["examples/init/*", "config/*.vhost"],
      scripts=["scripts/igor", "scripts/igor-post-update"]
     )
