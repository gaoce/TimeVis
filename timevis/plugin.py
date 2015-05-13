plugins = {}


class PluginMeta(type):

    def __init__(cls, name, bases, clsdict):
        type.__init__(cls, name, bases, clsdict)
        if name in plugins:
            raise ValueError("Class {} already registered!".format(name))
        elif name == 'Plugin':
            pass
        else:
            plugins[name] = cls


class Plugin(object):
    __metaclass__ = PluginMeta
