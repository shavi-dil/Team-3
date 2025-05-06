import numpy as np
from sklearn.ensemble import RandomForestClassifier
from keras import Sequential
from torch import lstm
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def train_lstm(x_train, x_test, y_train, y_test):
    scalar = MinMaxScaler(feature_range = (0, 1))
    

def train_RandomForest(x_train, x_test, y_train, y_test):
    clf = RandomForestClassifier()
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    print("Random Forest classification report:")
    print(classification_report(y_test, y_pred))

    print("Random Forest confusion matrix:")
    print(confusion_matrix(y_pred, y_test))

    print("Accuracy score: ", accuracy_score(y_test, y_pred))