import pandas as pd
import numpy as np
from preprocessor import *
from sklearn.feature_extraction.text import CountVectorizer

# PREPROCESSING AND KEYWORD EXTRACTION WITH TF

def select_keywords(question):
    return [word for word in question if word in keyword_list]


df = pd.read_csv("questions_v3.csv", header = None)

df = df[0].str.lower()

df = df.apply(remove_punctuations)

tokenized_data = df.apply(questions_tokenization)

removed_stopwords_data = tokenized_data.apply(remove_stopwords)

stemmed_data = removed_stopwords_data.apply(stemming_word)

df_cv = [' '.join(sentence) for sentence in stemmed_data]
count_vectorizer = CountVectorizer(min_df=0.005, stop_words=sastrawi_stopwords)
word_count_vector = count_vectorizer.fit_transform(df_cv)
keyword_list = count_vectorizer.get_feature_names()
print(keyword_list[:10])

full_processed_data = stemmed_data.apply(select_keywords)

# DEFINE CONSTANT WEIGHT WITH RELATIVE FREQUENCY

keyword_dict = dict((keyword, 0) for keyword in keyword_list)
keyword_constant_weight = keyword_dict

# store frequency of keyword in all questions
for question in full_processed_data:
    for word in question:
        keyword_dict[word] += 1
        
# calculate constant weight of each keyword
keyword_sum = sum(keyword_dict.values())
for keyword, frequency in keyword_dict.items():
    keyword_constant_weight[keyword] = frequency / keyword_sum

print(sum(keyword_constant_weight.values()))

# DEFINE RELATIVE WEIGHT WITH IDF

# store term's number of occurence in all question
num_of_question = len(full_processed_data)

keyword_dict = dict.fromkeys(keyword_dict, 0)
keyword_relative_weight = dict.fromkeys(keyword_dict, 0)
relative_weight_index = dict.fromkeys(keyword_relative_weight, [0] * num_of_question)

for keyword in keyword_list:
    for question in full_processed_data:
        if keyword in question:
            keyword_dict[keyword] += 1

print(keyword_dict)

# apply idf to questions
for keyword, frequency in keyword_dict.items():
    for i in range(5):
        keyword_relative_weight[keyword] = np.log10(num_of_question / frequency)
        if keyword in full_processed_data[i]:
            relative_weight_index[keyword][i] = np.log10(num_of_question / frequency)
    

v_relative_weight_index = pd.DataFrame.from_dict(relative_weight_index)
v_relative_weight_index.to_csv("./visual/relative_weight_index.csv")


# APPLY WEIGHTED-SUM MODEL FOR EACH QUESTION
series_to_2d_list = full_processed_data.tolist()
WS_of_ques = []

for question in series_to_2d_list:
    total_weight = 0
    for word in question:
        total_weight += (keyword_constant_weight[word] * keyword_relative_weight[word])

    WS_of_ques.append(total_weight)

print(WS_of_ques[:5])

# Save all result into path ./DATA

constant_weight_list = pd.DataFrame(list(keyword_constant_weight.items()), columns=['keyword', 'weight'])
constant_weight_list.to_csv("./data/constant_weight.csv", index=False)

relative_weight_list = pd.DataFrame(list(keyword_relative_weight.items()), columns=['keyword', 'weight'])
relative_weight_list.to_csv("./data/relative_weight.csv", index=False)

pd.DataFrame(WS_of_ques, columns=['sum_of_weight']).to_csv("./data/weighted_sum.csv", index=False)
pd.DataFrame(keyword_list, columns=['keywords']).to_csv("keyword_list_csv.csv", index=False)
