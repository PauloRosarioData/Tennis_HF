__author__ = 'paulorosario'
import csv
import numpy
import scipy
import matplotlib.pyplot as plt
from sklearn import preprocessing, cross_validation
from sklearn.cross_validation import train_test_split
from sklearn import metrics
#Imports for Module 4
from sklearn import neighbors
from sklearn.naive_bayes import GaussianNB



#Code common to all modeles from module 3 onwards
##NB. The X and yTransformed variables come from the preprocessing in the previous module.
fileName = "dataset.csv"
fileOpen = open(fileName, "rU")
csvData = csv.reader(fileOpen)
dataList = list(csvData)
dataArray =  numpy.array(dataList)
X = dataArray[1:,1:3].astype(float)
y = dataArray[1:, 0]
yTransformed = y


fileN = "trading.csv"
fileO = open(fileN, "rU")
csvD = csv.reader(fileO)
dataL = list(csvD)
dataA =  numpy.array(dataL)
T = dataA[1:,0:2].astype(float)

nbrs = neighbors.NearestNeighbors(n_neighbors=3, algorithm="ball_tree").fit(X)
distances, indices = nbrs.kneighbors(X)

print indices[:5] # the first its himself, because he is closer to himself
print distances[:5] # the first distance is zero because thats the distance to himself

#classification based on 3 nearest neighbours
knnK3 = neighbors.KNeighborsClassifier(n_neighbors=1811, weights='distance')
knnK3 = knnK3.fit(XTrain, yTrain)
predictedK3 = knnK3.predict(Xtest)
metrics.accuracy_score(yTest, predictedK3)

predictedK3 = knnK3.predict_proba(T)
a = predictedK3[0:,0:1]
a.tofile('foo.csv',sep=',',format='%10.5f')

#split into training and test data
XTrain, Xtest, yTrain, yTest = train_test_split(X, yTransformed)

#naive bayes, this is methodological wrong as Im using the dataset to predict itself
nbmodel = GaussianNB().fit(X, y)
yPredproba = nbmodel.predict_proba(T) # gives the probability estimate
a = yPredproba[0:,0:1]

a.tofile('foo.csv',sep=',',format='%10.5f')

#naive bayes, correct way with train and test dataset
nbmodel = GaussianNB().fit(XTrain, yTrain)
yPred = nbmodel.predict(Xtest)
metrics.accuracy_score(yTest, yPred)
yPredproba = nbmodel.predict_proba(Xtest) # gives the probability estimate