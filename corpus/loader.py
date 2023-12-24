import os
from enum import Enum
import random

from .type import type
from .handler import handler
from .builder import builder


class loader:
    """
     A class to load corpora and build them if needed.

     Attributes
     ----------
     _filehandler : handler
         A file handler object to read the corpus files.
     _corpus : dict
         A dictionary containing the corpus files.
     _sent_div : set
         A set of sentence delimiters.
     _tok_delim : str
         A string representing the token delimiter.
     _sent_delim : str
         A string representing the sentence delimiter.

     Methods
     -------
     load_file_as_str(txtfile: str) -> str:
         Reads the file and returns its contents as a string.
     load_corpus(corpus_name, corpus_type: Enum, shuffle_sentences=False, shuffle_tokens=False) -> str or list:
         Loads the corpus and shuffles it if needed.
     _load_corpus(corpus_name, corpus_type: Enum) -> str or list:
         Loads the corpus and builds it if needed.
     """
    def __init__(self, tok_delim="\b", sent_delim="\n"):
        """
        Parameters
        ----------
        tok_delim : str, optional
            A string representing the token delimiter (default is "\b").
        sent_delim : str, optional
            A string representing the sentence delimiter (default is "\n").
        """
        self._filehandler = handler()
        self._corpus = {}
        self._corpus['bijankhan'] = self._filehandler.get_file("bijankhan_unprocessed")
        self._corpus['peykareh'] = self._filehandler.get_file("peykareh_unprocessed")
        self._sent_div = {".", "?", "؟", "!"}
        self._tok_delim = tok_delim
        self._sent_delim = sent_delim

    @staticmethod
    def load_file_as_str(txtfile):
        """
        Reads the file and returns its contents as a string.

        Parameters
        ----------
        txtfile : str
            The name of the file to be read.

        Returns
        -------
        str
            The contents of the file as a string.
        """
        with open(txtfile, "r") as f:
            return f.read()

    def _load_corpus(self, corpus_name, corpus_type: Enum):
        """
        Loads the corpus and builds it if needed.

        Parameters
        ----------
        corpus_name : str
            The name of the corpus to be loaded.
        corpus_type : Enum
            The type of corpus to be loaded.

        Returns
        -------
        whole : str or list
            The contents of the corpus as a string or a list of strings.
        """

        if corpus_type not in list(type):
            raise Exception("invalid corpus type requested")
        file_key = handler.get_file_key(corpus_name, corpus_type)

        if not os.path.isfile(self._filehandler.get_file(file_key)):
            print(f"Requested version not found corpus_name: {corpus_name}, corpus_type: {corpus_type}")
            print("building the corpus")
            return builder().build_corpus(corpus_name, corpus_type)

        file_path = self._filehandler.get_file(file_key)
        if corpus_type.value == type.whole_raw.value:
            with open(file_path, "r") as f:
                # Reading the lines from the file
                whole = f.read()
            return whole
        elif corpus_type.value == type.whole_tok.value:
            with open(file_path, "r") as f:
                # Reading the lines from the file
                whole = f.read()
                whole = whole.split(self._tok_delim)
            return whole
        elif corpus_type.value == type.sents_raw.value:
            with open(file_path, "r") as f:
                # Reading the lines from the file
                whole = f.read()
                whole = whole.split(self._sent_delim)
            return whole
        elif corpus_type.value == type.sents_tok.value:
            with open(file_path, "r") as f:
                # Reading the lines from the file
                whole = f.read()
                whole = whole.split(self._sent_delim)
                whole = [sentence.split(self._tok_delim) for sentence in whole]
            return whole

    def load_corpus(self, corpus_name, corpus_type: Enum, shuffle_sentences=False, shuffle_tokens=False):
        """
        Loads the corpus and shuffles it if needed.

        Parameters
        ----------
        corpus_name : str
            The name of the corpus to be loaded.
        corpus_type : Enum
            The type of corpus to be loaded.
        shuffle_sentences : bool, optional
            A boolean indicating whether to shuffle the sentences (default is False).
        shuffle_tokens : bool, optional
            A boolean indicating whether to shuffle the tokens (default is False).

        Returns
        -------
        loaded : str or list
            The contents of the corpus as a string or a list of strings.
        """
        valid_shuffle = False
        any_shuffle = shuffle_tokens and shuffle_sentences

        if corpus_name in self._filehandler.corpus_names():
            loaded = self._load_corpus(corpus_name, corpus_type)
        elif corpus_name == 'both':
            loaded = '' if corpus_type.value == type.whole_raw else []
            for name in self._filehandler.corpus_names():
                loaded += self.load_corpus(name, corpus_type)
        else:
            raise Exception('invalid corpus name')
        # Sents raw true false
        if shuffle_sentences and (corpus_type.value == type.sents_tok.value or corpus_type.value == type.sents_raw.value):
            random.shuffle(loaded)
            valid_shuffle = True

        if shuffle_tokens and (corpus_type.value == type.whole_tok.value):
            random.shuffle(loaded)
            valid_shuffle = True
        if shuffle_tokens and (corpus_type.value == type.sents_tok.value):
            for sentence in loaded:
                random.shuffle(sentence)
            valid_shuffle = True
        any_shuffle = shuffle_tokens or shuffle_sentences
        if any_shuffle and not valid_shuffle:
            raise Exception("Invalid shuffling strategy")
        return loaded

    def load_corpus__(self, corpus_name, corpus_type: Enum, shuffle_sentences=False, shuffle_tokens=False):
        valid_shuffle = False
        any_shuffle = shuffle_tokens and shuffle_sentences

        if corpus_name not in self._filehandler.corpus_names() and corpus_name != 'both':
            raise Exception('invalid corpus name')

        loaded = None
        for name in self._filehandler.corpus_names() if corpus_name == 'both' else [corpus_name]:
            corpus = self._load_corpus(name, corpus_type)
            if loaded is None:
                loaded = corpus
            else:
                loaded += corpus

            if any_shuffle:
                if corpus_type.value == type.sents_tok.value or corpus_type.value == type.sents_raw.value:
                    random.shuffle(loaded)
                    valid_shuffle = True
                elif corpus_type.value == type.whole_tok.value:
                    random.shuffle(loaded)
                    valid_shuffle = True
                elif corpus_type.value == type.sents_tok.value:
                    for sentence in loaded:
                        random.shuffle(sentence)
                    valid_shuffle = True

        if any_shuffle and not valid_shuffle:
            raise Exception("Invalid shuffling strategy")

        return loaded

