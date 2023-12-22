import os
from enum import Enum
import random

from .type import type
from .handler import handler
from .builder import builder


class loader:
    def __init__(self, tok_delim="\b", sent_delim="\n"):
        self._filehandler = handler()
        self._corpus = {}
        self._corpus['bijankhan'] = self._filehandler.get_file("bijankhan_unprocessed")
        self._corpus['peykareh'] = self._filehandler.get_file("peykareh_unprocessed")
        self._sent_div = {".", "?", "؟", "!"}
        self._tok_delim = tok_delim
        self._sent_delim = sent_delim

    @staticmethod
    def load_file_as_str(txtfile):
        # Read the file and return its contents as a string
        with open(txtfile, "r") as f:
            return f.read()

    def _load_corpus(self, corpus_name, corpus_type: Enum):
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
        ###TODO: write this one
        valid_shuffle = False
        any_shuffle = shuffle_tokens and shuffle_sentences
        loaded = loader._load_corpus(corpus_name,corpus_type)
        if shuffle_sentences and (corpus_type.value == type.sents_tok.value or corpus_type.value == type.sents_tok.value)
            random.shuffle(loaded)
            valid_shuffle = True

        if shuffle_tokens and corpus_type.value == type.whole_tok.value:
            random.shuffle(loaded)
            valid_shuffle = True
        if shuffle_tokens and corpus_type.value == type.sents_tok.value:
            for sentence in loaded:
                random.shuffle(sentence)
            valid_shuffle = True

        if not valid_shuffle or not any_shuffle:
            raise Exception("invalid shuffling strategy")


