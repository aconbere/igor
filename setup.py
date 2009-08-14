from distutils.core import setup

setup(name="igor",
      version="1.0",
      author="Anders Conbere",
      author_email = "aconbere@conbere.org",
      license = "bsd",
      packages=["igor", "igor.git"],
      scripts=["scripts/igor", "scripts/igor-post-update"]
     )
