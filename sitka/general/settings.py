"""General model environment and simulation settings.
"""
class Settings:
    """
    Store general simulation settings.

    Parameters
    ----------
    working_directory : str
        A valid directory used for working files.

    Attributes
    ----------
    working_directory

    """
    def __init__(self, working_directory):
        self.working_directory = working_directory
