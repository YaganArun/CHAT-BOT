import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn import preprocessing
import random
from . import nlp #custom built module
from . import booking

data = pd.read_csv('data2.csv', encoding='ISO-8859-1')
training_feature = data.columns[2:]
label = data.Source #column that is to be predicted 

X = data[training_feature]
Y = label
le = preprocessing.LabelEncoder()
le.fit(Y)
encode_label = le.transform(Y)

dt = DecisionTreeClassifier(max_leaf_nodes=21, random_state=0, criterion='gini')  # classifier
classifier = dt.fit(X, Y)

resp = {
         'question':['Do you have' , 'Are you experincing' , 'What about' , 'How about' , 'Are you suffering from' , 'Any sign of']
}

tree = classifier.tree_
feature_name = [
            training_feature[i] if i != _tree.TREE_UNDEFINED else "undefined!"
            for i in tree.feature
        ]

def print_disease(node):
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return disease

def print_question(node):
    name = feature_name[node]
    return random.choice(resp['question']) +" " + name + " ?"

def decision(node , response): #returns the node
    if tree.feature[node] != _tree.TREE_UNDEFINED:
        threshold = tree.threshold[node]
        response = nlp.predict_text_class(response)
        ans = response
        if ans == 'yes':
            val = 1
        else:
            val = 0
        if val <= threshold:
            return tree.children_left[node]
        else:
            return tree.children_right[node]
    else:
        return node


def booking_appointment_response(userInput):
    return booking.predict_appointment(userInput)


