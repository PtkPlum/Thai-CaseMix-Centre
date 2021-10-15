import keras
import matplotlib.pyplot as plt

print(keras.backend.backend())

from keras.datasets import fashion_mnist, mnist

#(x_train, y_train), (x_test, y_test) = mnist.load_data() # number data
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data() # fashion data

plt.imshow(x_train[0])
plt.show()
plt.imshow(x_train[0], cmap=plt.cm.binary)
plt.show()

# normalize เพื่อ accuracy ที่ดี
x_train = x_train / 255
x_test  = x_test / 255

# Sequential คือ layer by layer not residual (Deep residual network) na
from keras.models import Sequential
from keras.layers import Flatten, Dense

model = Sequential()
model.add(Flatten(input_shape=[28,28]))
# relu คล้ายเซลล์สมองอยู่นะ
model.add(Dense(128, activation="relu"))
model.add(Dense(128, activation="relu"))
model.add(Dense(10, activation="softmax"))
model.summary()

# run model
model.compile(loss="sparse_categorical_crossentropy",
              optimizer="adam",
              metrics=["accuracy"])
model.fit(x_train, y_train, epochs=5)

# save model
model.save("number.model")
# load model
_model = keras.models.load_model("number.model")

_model.evaluate(x_test, y_test)

predictions = _model.predict([x_test])
predictions[0]

import numpy as np

predict = np.argmax(predictions[0])
print(predict)

plt.imshow(x_test[0])

