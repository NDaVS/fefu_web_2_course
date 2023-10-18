import tensorflow as tf
import numpy as np
import cv2
import os


class NumberRecognizer:
    model = 'new.model'

    def __init__(self, model: str = model):

        self._mnist = tf.keras.datasets.mnist
        (self.x_train, self.y_train), (self.x_test, self.y_test) = self._mnist.load_data()

        self.x_train = tf.keras.utils.normalize(self.x_train, axis=1)
        self.x_test = tf.keras.utils.normalize(self.x_test, axis=1)

        self.model = model

    def init(self, epochs: int = 10): #Инициализация модели + обучение
        if os.path.exists(f'{self.model}'):
            return
        _model = tf.keras.models.Sequential()
        _model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
        _model.add(tf.keras.layers.Dense(128, activation='relu'))
        _model.add(tf.keras.layers.Dense(128, activation='relu'))
        _model.add(tf.keras.layers.Dense(10, activation='softmax'))

        _model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        _model.fit(self.x_train, self.y_train, epochs=epochs)

        _model.save(self.model)
        _model.save('new.model')

    def load(self): #Загрузка модели
        self._model = tf.keras.models.load_model(self.model)
        loss, accuracy = self._model.evaluate(self.x_test, self.y_test)

        return (loss, accuracy)

    def recognize(self, path: str):

        try:
            # img = cv2.imread(path)[:,:,0]
            img = cv2.imread(path)
            img = cv2.resize(img, (28, 28))[:, :, 0]
            img = np.invert(np.array([img]))
            # img = Image.open(path).resize((28, 28))
            # img = np.invert(np.array([img]))

            prediction = self._model.predict(img)
            return np.argmax(prediction)
        except Exception as e:
            print(f"Error: {e}")


#EXAMPLES
# n = NumberRecognizer()
#
# n.init()
# n.load()
#
# num = n.recognize('1.png')
#
# print(num)
