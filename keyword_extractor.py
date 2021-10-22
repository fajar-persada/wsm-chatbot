import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from preprocessor import remove_punctuations

class extractor:
    def __init__(self):
        df = pd.read_csv("questions_v3.csv", header = None)
        df = df[0].str.lower()
        df = df.apply(remove_punctuations)
