"""
Doorstep exceptions classes
"""


class DoorstepError(Exception):
    """
    Creating user which already exist.
    """

    def __init__(self, *args, **kwargs):
        super(DoorstepError, self).__init__(*args, **kwargs)
