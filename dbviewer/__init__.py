
def classFactory(iface):

    from .DBPlugin import DBPlugin
    return DBPlugin(iface) 
