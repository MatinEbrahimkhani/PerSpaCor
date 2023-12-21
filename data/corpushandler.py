import csv
import os


class CorpusHandler:
    def __init__(self, base_directory="./", filenames="./data/filenames.csv"):
        """
        Initializes the CorpusHandler class with a directory to search and a file that contains the filenames and their paths.

        Parameters:
        directory (str): The directory to search for files. Default is "./".
        filenames (str): The path to the file that contains the filenames and their paths. Default is "./data/filenames.csv".
        """
        self.directory = base_directory
        self.filenames = filenames
        self._files = {}
        self._load_filenames()

    def _load_filenames(self):
        """
        Loads the filenames and their paths from the file specified in the filenames attribute.
        """
        with open(self.filenames, mode='r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self._files[row[0]] = row[1]

    def get_file(self, filename):
        """
        Returns the path of the file with the specified filename.

        Parameters:
        filename (str): The name of the file to retrieve.

        Returns:
        str: The path of the file with the specified filename.

        Raises:
        Exception: If the specified filename is not in the dictionary of files.
        """
        return self._files.get(filename,
                               f"File '{filename}' not found. Available filenames: {list(self._files.keys())}")

    def find_files(self, name):
        """
        Finds files in the directory and subdirectories that match the specified name and updates the dictionary with the files and their paths.
        Parameters:
        name (str): The name of the files to search for.
        """
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file == name:
                    self._files[file] = os.path.join(root, file)

    @property
    def files(self):
        """
        Returns the dictionary of files and their paths.

        Returns:
        dict: The dictionary of files and their paths.
        """
        return self._files
