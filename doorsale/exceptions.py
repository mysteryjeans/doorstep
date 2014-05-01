"""
Doorsale exceptions classes
"""

class DoorsaleError(Exception):
    """
    Creating user which already exist. 
    """
    def __init__(self, error_code, *args, **kwargs):
        super(DoorsaleError, self).__init__(*args, **kwargs)
        self.error_code = error_code