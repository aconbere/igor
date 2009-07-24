Igor is a static blog generator akin to Jekyll [1], at it's essence is a script that runs against a given git repository and outpus a nice directory of html files.

Install
=======

To install igor simply run

> git clone git://github.com/aconbere/igor.git
> cd igor
> sudo python setup.py install

Run
===

Igor installs a simple command line script to run it

> igor path/to/git/repo path/to/output/dir
... beginning parsing path/to/git/repo/_posts
... publishing index.html
... publishing 2009/01/11/post1/index.html
... publishing 2009/07/21/post2/index.html

* NOTE this is a pretty dumb script right now and will delete anything you point the outdir to, so be careful

TODO
====

* write the actual git hook

* atom publishing
* archive links
