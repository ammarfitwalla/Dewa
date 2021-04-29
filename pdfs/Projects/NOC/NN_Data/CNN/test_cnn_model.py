import numpy as np
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import tensorflow as tf

new_model = tf.keras.models.load_model(r'checkpoints\model-429-0.10')

# X_test = [[0.47,0.59,0.47,0.59,0.48,0.59,0.45,0.59,0.47,0.59,0.49,0.59,0.51,0.58,0.51,0.58,0.52,0.58]]  # output : 0

X_test = [[0.13, 0.07, 0.15, 0.07, 0.16, 0.07, 0.12, 0.06, 0.15, 0.06, 0.17, 0.06, 0.14, 0.06, 0.15, 0.06, 0.15,
           0.06]]  # output : 1

X_scale = np.array(X_test)

predictions = new_model.predict_classes(X_scale)
print(X_test)
print("output:", predictions[0][0])

"""

for txt in all_texts:
    for arrow in symbols:
        for nums in all_nums:
            some_data = [txt, arrow, nums]
            predictions = new_model.predict_classes(some_data)
            print("output:", predictions[0][0])


"""
