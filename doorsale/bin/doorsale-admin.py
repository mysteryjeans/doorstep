#!/usr/bin/env python
import os
import sys

from django.core import management


def configure_doorsale(project_name):
    """
    Configures Doorsale settings in project
    """
    import doorsale

    doorsale_app_urls_path = os.path.join(
        os.path.dirname(doorsale.__file__),
        'conf', 'project_settings', 'app_urls.py')

    project_urls_path = os.path.join(
        os.getcwd(),
        project_name,
        project_name,
        'urls.py'
    )

    doorsale_app_settings_path = os.path.join(
        os.path.dirname(doorsale.__file__),
        'conf', 'project_settings', 'app_settings.py')

    project_settings_path = os.path.join(
        os.getcwd(),
        project_name,
        project_name,
        'settings.py'
    )

    # Dumps all preconfigured settings of Doorsale apps
    # into projects settings file
    with open(doorsale_app_settings_path, "r+") as f:
        app_settings = f.read()

    with open(project_settings_path, 'a+') as f:
        f.write(app_settings)

    # Replaceing project urls.py from Doorsale urls
    with open(doorsale_app_urls_path, "r+") as f:
        app_urls = f.read()

    with open(project_urls_path, "a+") as f:
        f.write(app_urls)


if __name__ == "__main__":
    management.execute_from_command_line()

    if 'startproject' in sys.argv:
        configure_doorsale(sys.argv[-1])
