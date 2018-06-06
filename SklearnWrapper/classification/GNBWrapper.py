import numpy as np
from matplotlib.colors import ListedColormap
from sklearn.naive_bayes import GaussianNB
from MethodWrapper import MethodWrapper
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import datasets
import matplotlib.pyplot as plt
import sys

class NBWrapper(MethodWrapper, name = "GaussianNB"):
    """GaussianNB wrapper"""

    def __init__(self):
        MethodWrapper.__init__(self)
        self.validation_fraction = 0.1
        self.shuffle = True
        self.samples = 300

    def set_samples(self, value:str):
        self.samples = int(value)
    def set_validation_fraction(self, value:str):
        self.validation_fraction = float(value)
    def set_shuffle(self, value:str):
        self.shuffle = bool(value)

    def make_meshgrid(self, X, Y, h=0.2):
        x_min, x_max = X.min() - 0.5, X.max() + 0.5
        y_min, y_max = Y.min() - 0.5, Y.max() + 0.5
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        return xx, yy

    def execute(self):
        # X - набор свойств, y - результат, зависящий от X
        X, y = datasets.samples_generator.make_moons(self.samples, self.shuffle, 0.3, 0)
        file_name = "output.txt"

        X = StandardScaler().fit_transform(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = self.validation_fraction)
        X0,X1 = X[:, 0], X[:, 1]
        xx, yy = self.make_meshgrid(X0, X1)

        labels = set(y)
        colors = ListedColormap([plt.get_cmap(name = "rainbow")(each)
            for each in np.linspace(0, 1, len(labels))])

        sys.stdout = open(file_name, 'a')
        classifier = GaussianNB()

        open(file_name, 'w').close() #clear file
        # Обучение классификатора
        classifier.fit(X_train, y_train)
        Z = classifier.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
        Z = Z.reshape(xx.shape)

        plt.clf()
        plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
        plt.scatter(X_train[:,0], X_train[:,1], c=y_train, cmap=colors, s=20, edgecolors='k')
        plt.scatter(X_test[:,0], X_test[:,1], alpha=0.5, c=y_test, cmap=colors, s=20, edgecolors='k')
        plt.xlim(xx.min(), xx.max())
        plt.ylim(yy.min(), yy.max())
        # Тестирование классификатора на новых данных
        score = classifier.score(X_test, y_test)
        plt.title('Gaussian Naive Bayes Classification\n score: ' + str(round(score, 5)))
        plt.show()
        sys.stdout = sys.__stdout__