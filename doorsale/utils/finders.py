import os


def get_app_paths(app_names):
    """
    Returns list of app directory paths
    """
    from importlib import import_module

    app_paths = []

    for app_name in app_names:
        mod = import_module(app_name)
        app_path = os.path.dirname(mod.__file__)
        app_paths.append(app_path)

    return app_paths


def get_static_paths(app_names):
    """
    Returns list of static folders path of specified apps
    """
    static_paths = []

    for app_dir in get_app_paths(app_names):
        app_static_dir = os.path.join(app_dir, 'static')

        if os.path.exists(app_static_dir):
            static_paths.append(app_static_dir)

    return static_paths
