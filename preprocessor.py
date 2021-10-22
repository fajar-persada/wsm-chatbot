#import string
import re
from nltk import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory 

sastrawi_stopwords = StopWordRemoverFactory().get_stop_words() + ['kak', 'sih']
stemmer = StemmerFactory().create_stemmer()

def remove_punctuations(question):
    question = re.sub("(\\d|\\W)+", " ", question)
    return question

def questions_tokenization(text):
    return word_tokenize(text)

def remove_stopwords(question):
    return [word for word in question if word not in sastrawi_stopwords]

def stemming_word(question):
    return [stemmer.stem(word) for word in question]