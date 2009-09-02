from distutils.core import setup

setup(name="igor",
      version="1.0",
      author="Anders Conbere",
      author_email = "aconbere@conbere.org",
      license = "bsd",
      packages=["igor_extras", "igor", "igor.vcs", "igor.vcs.git"],
      package_data={"igor_extras": ["initial_project/*", "config/*.vhost"]},
      scripts=["scripts/igor", "scripts/igor-post-update"]
     )
