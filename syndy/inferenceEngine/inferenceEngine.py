import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, _tree
from sklearn import preprocessing
import random
from . import nlp  # custom built module
from . import booking
resp = {
    'question': ['Do you have', 'Are you experincing', 'What about', 'How about', 'Are you suffering from', 'Any sign of']
}


data = pd.read_csv('data2.csv', encoding='ISO-8859-1')
training_feature = data.columns[2:]
label = data.Source  # column that is to be predicted
X = data[training_feature]
Y = label
le = preprocessing.LabelEncoder()
le.fit(Y)
encode_label = le.transform(Y)
dt = DecisionTreeClassifier(max_leaf_nodes=len(label), random_state=0, criterion='gini')  # classifier
classifier = dt.fit(X, Y)
tree = classifier.tree_
feature_name = [
    training_feature[i] if i != _tree.TREE_UNDEFINED else "undefined!"
    for i in tree.feature
]
########################################################################################## for children
dataChildren = pd.read_csv('dataChildren.csv')
training_feature_children = dataChildren.columns[1:]
label_children = dataChildren[dataChildren.columns[0]]  # column that is to be predicted

X_children = dataChildren[training_feature_children]
Y_children = label_children

le_children = preprocessing.LabelEncoder()
le_children.fit(Y_children)
encode_label_children = le_children.transform(Y_children)

dt_children = DecisionTreeClassifier(max_leaf_nodes=len(label_children), random_state=0, criterion='gini')  # classifier
classifier_children = dt_children.fit(X_children, Y_children)

tree_children = classifier_children.tree_
feature_name_children = [
    training_feature_children[i] if i != _tree.TREE_UNDEFINED else "undefined!"
    for i in tree_children.feature
]



def print_disease(node):
    node = node[0]
    val = node.nonzero()
    disease = le.inverse_transform(val[0])
    return disease


def print_question(age_group , node):
    if(age_group == 'children'):
        name = feature_name_children[node]
        return random.choice(resp['question']) + " " + name + " ?"
    else:
        name = feature_name[node]
        return random.choice(resp['question']) + " " + name + " ?"


def decision(age_group , node, response):  # returns the node
    if age_group == 'children':
        if tree_children.feature[node] != _tree.TREE_UNDEFINED:
            threshold = tree_children.threshold[node]
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
    elif age_group == 'adult':
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


