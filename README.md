# dejima-importer-example


Want to write your own importer for Dejima?  This gives you a solid foundation.

* Free software: MIT license

# Instructions

1. Edit the file in `src/my_importer/__init__.py` to handle importing the source you want to import from.
2. Install the package into the same virtual environment as Dejima by running:

```
python setup.py install
```

That's it!

# How does Dejima know about this importer?

Dejima uses setuptools entrypoints for plugin detection.  If you look at the `entry_points` field in `setup.py`, you'll see that this package adds a new entrypoint named named `my-importer` to the `dejima.sources` entrypoint list.  As long as the class named `SomeSource` in the `my_importer` module looks like a plugin to Dejima, it'll import it and make it available.

# Are there any more examples out there?

Definitely -- have a look at https://github.com/coddingtonbear/dejima/tree/master/src/dejima/sources for the built-in examples.

# How to see this in action

Just try running this importer for a particular deck -- you'll want to replace "Test" with the name of a deck to import cards into:

```
dejima import "Test" my-importer
```
