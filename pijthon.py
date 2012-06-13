#!/usr/bin/env python

"""
Pijthon - Python without the line noise. 
(i.e. more like Ruby, but don't tell anyone!)

Written by Emil Loer for the PyGrunn Monthly Meetup of June 2012.
"""

import sys
import os
import imp
import re

# Set DEBUG to True to print the preprocessed source code when importing
# modules.
DEBUG = False

class Loader(object):
    """
    The Loader class is responsible for loading a specific module from disk and
    initializing the module in the interpreter environment.
    """

    first_keyword = re.compile(r"^[a-zA-Z][a-zA-Z0-9_]*")
    parens_split = re.compile(r"^(\s*\S+\s+\S+)(.*)$")

    parens_keyword_list = ["def", "class"]
    colon_keyword_list = ["if", "else", "elif", "for", "while", "try",
            "except", "finally", "with"]

    def __init__(self, path):
        """ Initialize the loader for a given module filename """
        self.path = path

    def parse(self):
        """ Read the Pijthon module code from disk and compile it to Python """

        def transform(line):
            """ Transform a single line of Pijthon into Python """
            line = line.rstrip()

            # Find the first keyword on the line, if any
            match = self.first_keyword.match(line.lstrip())
            keyword = match and match.group()

            # Insert parentheses on function and class definitions
            if keyword in self.parens_keyword_list:
                match = self.parens_split.match(line)
                if not match:
                    raise SyntaxError("error on line '%s'" % line)

                outside, inside = match.groups()
                return "%s(%s):" % (outside, inside.strip())

            # Insert trailing colon on statements that require them
            if keyword in self.colon_keyword_list:
                return line + ":"

            return line

        # Read file and transform
        lines = file(self.path).readlines()
        transformed = map(transform, lines)

        return "\n".join(transformed)

    def load_module(self, fullname):
        # Create and prepare a new blank module
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__file__ = self.path
        mod.__loader__ = self
        mod.__package__ = fullname.rpartition(".")[0]

        # Read source code
        source = self.parse()

        # Show the preprocessed source code if desired
        if DEBUG:
            print "--- begin %s preprocessed source ---" % fullname
            print source
            print "--- end %s preprocessed source ---" % fullname

        # Execute the module
        exec source in mod.__dict__

        return mod

class Importer(object):
    """
    The Importer class is responsible for resolving module locations. In our
    case we only search for files with the .pij extension. If these aren't
    found we return None to delegate to any other hooks or the internal
    resolver.
    """

    def find_module(self, fullname, path=None):
        """
        Find a module in a given path (or the system module search path) and
        create a Loader instance for it.
        """
        lastname = fullname.rsplit('.', 1)[-1]

        # Find the first matching filename in the list of paths
        for d in (path or sys.path):
            pyd = os.path.join(d, lastname + '.pij')
            if os.path.exists(pyd):
                return Loader(pyd)

        # No Pijthon file found
        return None

# Set the meta import hook to the Pijthon importer
sys.meta_path = [Importer()]

if __name__ == "__main__":
    print "Welcome to Pijthon!\n"

    # Start IPython interactive shell
    try:
        import IPython
        from IPython.config.loader import Config
        from IPython.frontend.terminal.embed import InteractiveShellEmbed
        shell = InteractiveShellEmbed()
        shell()
    except ImportError:
        print "In order to run the interactive shell you need IPython"
