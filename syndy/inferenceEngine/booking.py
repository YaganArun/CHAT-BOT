import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('temp.csv')
stemmer = PorterStemmer()
words = stopwords.words("english")
data['preproctext'] = data['user_story'].apply(lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
leaf_nodes = len(data['class'].unique())
target = data['class']
train = data['preproctext']
x_train, x_test, y_train, y_test = train_test_split(data['preproctext'], target, test_size=0.30, random_state=100)

vectorizer_tfidf = TfidfVectorizer(stop_words='english', max_df=0.7 , sublinear_tf=True, norm='l2' , ngram_range=(1, 4))
train_tfIdf = vectorizer_tfidf.fit_transform(train.values.astype('U'))

dt = MultinomialNB()
clf = dt.fit(train_tfIdf,target)

def predict_appointment(inp):
    words = stopwords.words("english")
    wordList = " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", inp).split() if i not in words])
    inp1 = vectorizer_tfidf.transform([wordList])
    print('\nUSER : ' , inp)
    return  clf.predict(inp1)[0]
