"""
Doorsale exceptions classes
"""


class DoorsaleError(Exception):
    """
    Creating user which already exist.
    """

    def __init__(self, *args, **kwargs):
        super(DoorsaleError, self).__init__(*args, **kwargs)
