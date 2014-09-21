VERSION = (0, 1, 0, 'alpha', 0)


def get_version():
    from doorsale.utils.version import get_version
    return get_version(VERSION)
