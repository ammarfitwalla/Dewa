import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix, recall_score, precision_score, f1_score, roc_auc_score, accuracy_score
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# df = pd.read_csv(
#     r'E:\dewa\pdfs\GCNN\ClusterGCN\OUTPUT_HOUSE_IRRIGATION\all_output_csvs\output_wo_rows\NN_section_AB36.csv')

df = pd.read_csv(r'E:\dewa\pdfs\GCNN\ClusterGCN\NN_Data\NN_final_18_pts.csv')

df = df.sample(frac=1).reset_index(drop=True)
# print(df.head())

# print(df.dtypes)

X = df.drop(['output'], axis=1)
Y = df['output']
print(X.columns)
# print(Y)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=7, shuffle=True)

# print(X_train.head())

# logreg = LogisticRegression(random_state=4294967295, fit_intercept=True)
logreg = LinearRegression()
logreg.fit(X_train, y_train)

y_predict = logreg.predict(X_test)

z = X_test.copy()
z['Observed output'] = y_test
z['Predicted output'] = y_predict

print(z.head(10))


def draw_cm(actual, predicted):
    cm = confusion_matrix(actual, predicted)
    sns.heatmap(cm, aannot=True, fmt='.2f', xticklabels=[0, 1], yticklabels=[0, 1])
    plt.ylabel('observed')
    plt.xlabel('Predicted')
    plt.show()


print()
print("Training accuracy", logreg.score(X_train, y_train))
print()
print("Testing accusacy", logreg.score(X_test, y_test))
print()

# print("Confusion Matrix")
# print(draw_cm(y_test,y_predict))
# print()
# print("Recall:", recall_score(y_test,y_predict))
# print()
# print("Precision",precision_score(y_test,y_predict))
# print()
# print("F1 Score:",f1_score(y_test,y_predict))
# print()
# print("Roc Auc Score",roc_auc_score(y_test,y_predict))

# print(X_test)
#
# h=3429
# w=5000
#
## x,y,x1,y1,x2,y2 = 731/w, 3249/h, 754/w, 2956/h, 750/w, 2943/h
# x,y,x1,y1,x2,y2 = 731/w, 3249/h, 754/w, 2956/h, 872/w, 3232/h
#
# x,y,x1,y1,x2,y2 = '{:.2f}'.format(x), '{:.2f}'.format(y), '{:.2f}'.format(x1), '{:.2f}'.format(y1), '{:.2f}'.format(x2), '{:.2f}'.format(y2)
#
# a = np.array([x,y,x1,y1,x2,y2]).astype(float)
#
# print(a)
#
# custom_data = logreg.predict([a])
#
# print(custom_data)
