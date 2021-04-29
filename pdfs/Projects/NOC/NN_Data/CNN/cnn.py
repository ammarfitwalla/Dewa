import os
import sys
import numpy as np
import pandas as pd
# from silence_tensorflow import silence_tensorflow
# silence_tensorflow()
import tensorflow as tf
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Convolution2D
from tensorflow.keras.layers import MaxPooling2D
import warnings

warnings.filterwarnings('ignore')

"""
-------------------------------------------------------------------------------------------------------
                                ONE WAY TO TRAIN WITH TRAIN/TEST/VAL SPLIT
-------------------------------------------------------------------------------------------------------
"""

df = pd.read_csv(r"../NN_final_18_pts.csv")
# df = pd.read_csv(r"D:\KS\Projects\Dewa\pdfs\Projects\NOC\NN_Data\CNN\model_18pts_data.csv")
# df = df.sample(frac=1).reset_index(drop=True)

X = df.drop(labels=["output"], axis=1)
y = df["output"]

# print(X_train.shape)
# print(type(X_train))

# min_max_scaler = preprocessing.MinMaxScaler()
# X_scale = min_max_scaler.fit_transform(X)

X_train, X_val_and_test, Y_train, Y_val_and_test = train_test_split(X, y, test_size=0.3, shuffle=True)
X_val, X_test, Y_val, Y_test = train_test_split(X_val_and_test, Y_val_and_test, test_size=0.5, shuffle=True)

# print(X_train.shape, X_val.shape, X_test.shape, Y_train.shape, Y_val.shape, Y_test.shape)

"""
X_train (18 input features, 70% of full dataset)
X_val (18 input features, 15% of full dataset)
X_test (18 input features, 15% of full dataset)
Y_train (1 label, 70% of full dataset)
Y_val (1 label, 15% of full dataset)
Y_test (1 label, 15% of full dataset)
"""

# model = Sequential([
#     Dense(18, activation='relu', input_shape=(18,)),  # (18 + 2 + 1) * 2
#     Dense(36, activation='relu'),
#     Dense(144, activation='relu'),
#     Dense(36, activation='relu'),
#     Dense(18, activation='relu'),
#     Dense(1, activation='sigmoid'), ])

model = Sequential([
    Dense(42, activation='relu', input_shape=(18,)),  # (18 + 2 + 1) * 2
    Dense(21, activation='relu'),
    Dense(144, activation='relu'),
    Dense(36, activation='relu'),
    Dense(18, activation='relu'),
    Dense(1, activation='sigmoid'), ])


filepath = 'checkpoints' + os.sep + 'model-{epoch:02d}-{val_loss:0.2f}'

cp = tf.keras.callbacks.ModelCheckpoint(filepath,
                                        monitor='val_loss',
                                        verbose=2,
                                        save_best_only=True,
                                        save_weights_only=False,
                                        mode='auto',
                                        save_freq='epoch')

# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# model.fit(X_train, Y_train, batch_size=64, epochs=700, validation_data=(X_val, Y_val), callbacks=[cp])

new_model = tf.keras.models.load_model(r'D:\KS\Projects\Dewa\pdfs\Projects\NOC\NN_Data\CNN\checkpoints\model-653-0.06')
#
# # Check its architecture
# new_model.summary()
#
# # Evaluate the restored model
loss, acc = new_model.evaluate(X_test, Y_test, verbose=2)
print('Restored model, accuracy: {:5.2f}%'.format(100 * acc))

# # new_model.save("new_model.h5")
# # print(new_model.predict(X_test).shape)
#
predictions = new_model.predict_classes(X_test)
predictions = list(predictions)
Y_test = list(Y_test)
#
# for j, k in zip(Y_test, predictions):
#     print(j, k)
#
acc = accuracy_score(Y_test, predictions)
print('Model accuracy score on test data: {:5.2f}%'.format(100 * acc))

# save model and architecture to single file

# model.save("18pts_cnn_model.h5")
# print("Saved model to disk")

"""
-------------------------------------------------------------------------------------------------------
                            ALTERNATE WAY TO TRAIN WITHOUT TRAIN/TEST/VAL SPLIT
-------------------------------------------------------------------------------------------------------
"""

# # load the dataset
# df = np.loadtxt(r"../NN_final_18_pts.csv", delimiter=",", skiprows=1)
#
# X = df[:, 0:18]
# y = df[:, 18]  # split into input (X) and output (y) variables
#
# # define the keras model
# model = Sequential()
# model.add(Dense(12, input_dim=18, activation='relu'))
# model.add(Dense(8, activation='relu'))
# model.add(Dense(1, activation='sigmoid'))
# # compile the keras model
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# # fit the keras model on the dataset
# model.fit(X, y, epochs=150, batch_size=10)
# # evaluate the keras model
# _, accuracy = model.evaluate(X, y)
# print('Accuracy: %.2f' % (accuracy * 100))
