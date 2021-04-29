import numpy as nm
import matplotlib.pyplot as mtp
import pandas as pd

# importing datasets
# data_set = pd.read_csv(r'E:\dewa\pdfs\GCNN\ClusterGCN\NN_Data\NN_final_18_pts.csv')
data_set = pd.read_csv(r"../NN_final_18_pts.csv")
data_set = data_set.sample(frac=1).reset_index(drop=True)
# Extracting Independent and dependent Variable
x = data_set.drop(['output'], axis=1)
y = data_set['output']
print(x.columns)

# Splitting the dataset into training and test set.
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=7)

# Fitting Decision Tree classifier to the training set
from sklearn.tree import DecisionTreeClassifier

classifier = DecisionTreeClassifier(criterion='entropy', random_state=0)
classifier.fit(x_train, y_train)

y_predict = classifier.predict(x_test)

z = x_test.copy()
z['Observed output'] = y_test
z['Predicted output'] = y_predict

print(z.head(10))

print()
print("Training accuracy:", classifier.score(x_train, y_train))
print()
print("Testing accusacy:", classifier.score(x_test, y_test))
print()

from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, f1_score, recall_score

cm = confusion_matrix(y_test, y_predict)
# print(cm)

accuracy = accuracy_score(y_test, y_predict)
print('Accuracy: %f' % accuracy)
# precision tp / (tp + fp)
precision = precision_score(y_test, y_predict)
print('Precision: %f' % precision)
# recall: tp / (tp + fn)
recall = recall_score(y_test, y_predict)
print('Recall: %f' % recall)
# f1: 2 tp / (2 tp + fp + fn)
f1 = f1_score(y_test, y_predict)
print('F1 score: %f' % f1)
