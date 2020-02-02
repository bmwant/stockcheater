import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split

import config


class PiecesClassifier(object):
    def __init__(self, model=None):
        self.model = model or self.load_model()

    def load_model(self):
        model = create_model()
        model.load_weights(config.MODEL_CHECKPOINT)
        return model

    def predict(self, image) -> int:
        predictions = self.model.predict(image)
        class_index = np.argmax(predictions[0])
        return class_index


def create_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=config.INPUT_SHAPE),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(len(config.CLASS_NAMES), activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )
    return model


def load_data():
    with open('dataset.np', 'rb') as f:
        dataset = np.load(f)
    X = []
    y = []
    for data, label in dataset:
        X.append(data)
        y.append(label)
    X = np.array(X)
    X = X / 255.0  # normalize data
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=True)

    return X_train, y_train, X_test, y_test


def train_model():
    print('Using tensorflow', tf.__version__)
    X_train, y_train, X_test, y_test = load_data()

    model = create_model()
    model.summary()

    model.fit(X_train, y_train, epochs=10)

    test_loss, test_acc = model.evaluate(X_test, y_test)

    print('\nTest loss:', test_loss)
    print('Test accuracy:', test_acc)

    print('\nSaving model weights')
    model.save_weights(config.MODEL_CHECKPOINT)
    return model


def test_predict():
    import cv2
    classifier = PiecesClassifier()
    image = cv2.imread('train_images/b/001.png', cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, config.INPUT_SHAPE, interpolation=cv2.INTER_LINEAR)
    image = image / 255.0
    image = np.expand_dims(image, 0)
    print(classifier.predict(image))


if __name__ == '__main__':
    train_model()
