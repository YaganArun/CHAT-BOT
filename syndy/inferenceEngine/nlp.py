import os
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB

resp = pd.read_csv('response.csv')

#preprocessing + adding preproccesed resp as a new column
stemmer = PorterStemmer()
words = stopwords.words("english")
resp['preproctext'] = resp['response'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())

target = resp['class']
x_train, x_test, y_train, y_test = train_test_split(resp['preproctext'], target, test_size=0.30, random_state=100)

#transforming words into numeric form
vectorizer_tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)
train_tfIdf = vectorizer_tfidf.fit_transform(x_train.values.astype('U'))

dt_nlp = DecisionTreeClassifier(random_state=0)
clf = dt_nlp.fit(train_tfIdf, y_train)

def predict_text_class(string):
    string = string.strip()
    if string == 'no':
        string = string+'pe'
    resp = vectorizer_tfidf.transform([string])
    return clf.predict(resp)[0]


# for debugging 
# while True:
#     resp = input()
#     if resp == 'bye':
#         break
#     # if resp == 'no' or resp == 'n':
#     #     resp = resp+'pe'
#     ip = vectorizer_tfidf.transform([resp])
#     print('bot classifies : ',clf.predict(ip)[0])

# # print(resp)
