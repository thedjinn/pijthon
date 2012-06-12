class Node(object):
    def __init__(self, name, args={}, text=None):
        self.name = name
        self.args = args
        self.text = text
        self.children = []

    def __repr__(self):
        args = "".join(" %s=\"%s\"" % (key, self.args[key]) for key in self.args.keys())

        if self.text:
            text = " " + repr(self.text)
        else:
            text = ""

        return "<mnml.Node:%s%s%s children=[%s]>" % (self.name, args, text, ", ".join(repr(child) for child in self.children))

