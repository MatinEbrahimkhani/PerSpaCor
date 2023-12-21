import os
from enum import Enum

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


    def load_corpus(self, corpus_name, corpus_type: Enum):
        if corpus_type not in list(type):
            raise Exception("invalid corpus type requested")
        filename = corpus_name+"_"+str(corpus_type.name)
        if os.path.isfile(self._filehandler.get_file(filename)):
            if corpus_type.value == type.whole_raw.value:

                    with open(self._filehandler.get_file(filename), "r") as f:
                        # Reading the lines from the file
                        whole = f.read()
                    return whole
                else:
                    print(f"Requested version not found corpus_name: {corpus_name}, corpus_type: {corpus_type}")
                    whole = builder().build_corpus(corpus_name, corpus_type)

            elif corpus_type.value == type.whole_tok.value:
                if os.path.isfile(self._filehandler.get_file(filename)):
                    with open(self._filehandler.get_file(filename), "r") as f:
                        # Reading the lines from the file
                        line = f.read()
                        # Using list comprehension to split the lines by the tab character
                        whole = line.split(self._tok_delim)
                    return whole
                else:
                    print(f"Requested version not found corpus_name: {corpus_name}, corpus_type: {corpus_type}")
                    return builder().build_corpus(corpus_name, corpus_type)
            elif corpus_type.value == type.sents_raw.value:
                if os.path.isfile(self._filehandler.get_file(filename)):
                    with open(self._filehandler.get_file(filename), "r") as f:
                        # Reading the lines from the file
                        line = f.read()
                        # Using list comprehension to split the lines by the tab character
                        whole = line.split(self._tok_delim)
                    return whole
                else:
                    print(f"Requested version not found corpus_name: {corpus_name}, corpus_type: {corpus_type}")
                    return builder().build_corpus(corpus_name, corpus_type)

            elif corpus_type.value == type.sents_tok.value:
                if os.path.isfile(self._filehandler.get_file("bijankhan_sents_tok")):
                    with open(self._filehandler.get_file("bijankhan_sents_tok"), "r") as f:
                        # Reading the lines from the file
                        line = f.read()
                        # Using list comprehension to split the lines by the tab character
                        whole = line.split(self._tok_delim)
                    return whole
                else:
                    print(f"Requested version not found corpus_name: {corpus_name}, corpus_type: {corpus_type}")
                    return builder().build_corpus(corpus_name, corpus_type)

            # --------------------------------------- PEYKAREH ---------------------------------------
        elif corpus_name == "peykareh":
            if corpus_type.value == type.whole_raw.value:
                pass
            elif corpus_type.value == type.whole_tok.value:
                pass
            elif corpus_type.value == type.sents_raw.value:
                pass
            elif corpus_type.value == type.sents_tok.value:
                pass