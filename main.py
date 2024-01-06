# import itertools

from corpus.builder import Builder
from corpus.type import Type
from corpus.handler import Handler

from utils.labeler import Labeler
#
# bul = Builder()
# bul.build_all()
# bul.build_corpus("bijankhan",type.whole_raw)
# from  corpus.handler import handler
from corpus.loader import Loader
from utils.label_evaluator import Evaluator


def test_all_inputs(func, twoD_list: list):
    for inputs in itertools.product(*twoD_list):
        print(*inputs)
        try:
            result = func(*inputs)
            print(result[:50])
            print(Type(result))
            print("\n\n\n\n\n")
            return result
        except:
            print("------------------------Error????   ", *inputs)


from corpus.loader import Loader
from corpus.type import Type

# corpus_loader = Loader()
# corpus_type = Type.whole_raw
#
# bijankhan = corpus_loader.load_corpus(corpus_name='bijankhan',
#                                       corpus_type=corpus_type)
#
# peykareh = corpus_loader.load_corpus(corpus_name="peykareh",
#                                      corpus_type=corpus_type)

# all_corpora = corpus_loader.load_corpus(corpus_name="all",
#                                         corpus_type=corpus_type,
#                                         shuffle_sentences= True)
#
# print(len(bijankhan))
# print(len(peykareh))
# print(len(peykareh) + len(bijankhan))
# print(len(all_corpora))
# print(all_corpora[:50])
corpus_type = Type.sents_raw
dataset_path = "./built_datasets/all.01/"
data = Loader().load_corpus("all", corpus_type=corpus_type, shuffle_sentences=True)
print(data[:10])