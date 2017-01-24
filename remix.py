import nltk
import pdb

# from nltk.download()
# - punkt
# - averaged_perceptron_tagger
# - maxent_ne_chunker
# - words
# pip deps
# - pip install numpy
# - pip install nltk
# - pip install beautifulsoup4
# - pip install requests


text = "Joseph Jarriel and Fakename went to Publix"

for sent in nltk.sent_tokenize(text):
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
        if hasattr(chunk, 'label'):
            if chunk.label() == 'PERSON':
                print(chunk)
        #    print(chunk.node, ' '.join(c[0] for c in chunk.leaves()))

pdb.set_trace()
