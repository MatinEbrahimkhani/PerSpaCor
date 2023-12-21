from data import CorpusHandler

c = CorpusHandler()
bij = c.get_file('bijankhan_unprocessed')
print(bij)
c.combine_files(bij)

bij = c.get_file('peykareh_unprocessed')
print(bij)
c.combine_files(bij)
