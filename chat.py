from preprocessor import *
import pandas as pd

class chat_responder:
    def __init__(self):
        self.constant_weight = pd.read_csv("./data/constant_weight.csv", index_col='keyword')
        self.relative_weight = pd.read_csv("./data/relative_weight.csv", index_col='keyword')
        self.weighted_sum = pd.read_csv("./data/weighted_sum.csv").values.tolist()
        
        keywords = pd.read_csv("keyword_list_csv.csv")
        self.keyword_list = keywords.values.tolist()
        self.keyword_list = [' '.join(keyword) for keyword in self.keyword_list]

        self.answer_list = pd.read_csv("questions_v3.csv", header=None)
        self.answer_list = self.answer_list[1].tolist()

    def select_keywords(self, question):
        return [word for word in question if word in self.keyword_list]

    def get_response(self, message):

        # PREPROCESS user message
        message_pro = remove_punctuations(message)
        message_pro = questions_tokenization(message_pro)
        message_pro = remove_stopwords(message_pro)
        message_pro = stemming_word(message_pro)
        message_pro = self.select_keywords(message_pro)

        print(message_pro)
        # define user's question's relative frequency
        constant_weight, relative_weight = [], []
        for word in message_pro:
            try:
                constant_weight.append(self.constant_weight.loc[word, 'weight'])
            except:
                constant_weight.append(0)
        
        # define user's question's idf
        for word in message_pro:
            try:
                relative_weight.append(self.relative_weight.loc[word, 'weight'])
            except:
                relative_weight.append(0)

        print(constant_weight, relative_weight)

        #define weighted sum of user question

        if len(constant_weight) != 0 and len(relative_weight) != 0:
            weighted_sum = 0
            for x, y in zip(constant_weight, relative_weight):
                weighted_sum += (x * y)
        
            print(weighted_sum)

            # select answer
            min_index = 0
            min_diff = 10
            for weight in self.weighted_sum:
                diff = abs(weighted_sum - weight)
                if (diff < min_diff):
                    min_diff = diff
                    min_index = self.weighted_sum.index(weight)

            answer = self.answer_list[min_index]

            return answer

        else:
            return 'Maaf, pertanyaan yang anda ajukan tidak dapat dijawab oleh sistem.\nSilahkan ajukan pertanyaan lain.'