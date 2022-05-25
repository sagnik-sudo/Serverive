import os
import tempfile


class Tools:
    def __init__(self):
        pass

    def get_temp_dir(self):
        """
        Returns the temporary directory
        """
        return tempfile.gettempdir()

    def delete_tempfile(self, file):
        """
        Deletes the temporary file
        """
        os.remove(file)
