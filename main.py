from corpus.type import type
from corpus.handler import handler

corpusname = "bijankhan"
# c_type= type.sents_raw
c_type= type.whole_raw
c_type= type.whole_tok
# c_type= type.sents_tok

filename = corpusname+"_"+str(c_type.name)
print(handler().get_file(filename))