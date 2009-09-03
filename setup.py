from distutils.core import setup

setup(name="igor",
      version="1.0",
      author="Anders Conbere",
      author_email = "aconbere@conbere.org",
      license = "bsd",
      packages=["igor_extras", "igor", "igor.vcs", "igor.vcs.git"],
      package_data={"igor_extras": ["initial_project/*.yaml",
                                    "initial_project/_posts/*",
                                    "initial_project/media/css/*",
                                    "initial_project/media/js/*",
                                    "initial_project/_templates/*",
                                    "server_config/*"]},
      scripts=["scripts/igor", "scripts/igor-post-update"]
     )
