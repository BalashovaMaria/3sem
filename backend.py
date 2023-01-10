
import pip
pip install numpy

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier


class Analyzer:
    def __init__(self, path):
        self.data = pd.read_csv(path).drop(columns=["Unnamed: 0"])
        self.model_KNN = KNeighborsClassifier()
        self.model_GNB = GaussianNB()
        self.model_CART = DecisionTreeClassifier()
        self.array = self.data.values
        self.X = self.array[:, 1:5]
        self.Y = self.array[:, 0]
        self.status_flags = [False, False, False]

    def predict_KNN(self, proba):
        if not self.status_flags[0]:
            self.model_KNN.fit(self.X, self.Y)
            self.status_flags[0] = True
        return self.model_KNN.predict(proba)

    def predict_GNB(self, proba):
        if not self.status_flags[1]:
            self.model_GNB.fit(self.X, self.Y)
            self.status_flags[1] = True
        return self.model_GNB.predict(proba)

    def predict_CART(self, proba):
        if not self.status_flags[2]:
            self.model_CART.fit(self.X, self.Y)
            self.status_flags[2] = True
        return self.model_CART.predict(proba)


from tkinter import filedialog

#tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
#
#folder_path = filedialog.askopenfilename()
#p#rint(folder_path)
#an = Analyzer(folder_path)
#print(an.predict_CART(np.array([[0, 0, 0, 0]])))
