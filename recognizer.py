import cv2
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


class Recognizer(object):
    def __init__(self, classifier=None):
        self.classifier = classifier or PiecesClassifier()

    def recognize_board(self, filepath: str):
        board = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        board_arr = []
        size = int(config.CELL_SIZE)
        for i in range(8):
            row = []
            for j in range(8):
                cell = board[i*size:(i+1)*size, j*size:(j+1)*size]
                image = cv2.resize(cell, config.INPUT_SHAPE,
                                   interpolation=cv2.INTER_LINEAR)
                image = image / 255.0
                image = np.expand_dims(image, 0)
                class_index = self.classifier.predict(image)
                piece = config.CLASS_NAMES[class_index]
                row.append(piece)
            board_arr.append(row)
        return board_arr


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
    print('Loading dataset...')
    with open(config.DATASET_PATH, 'rb') as f:
        dataset = np.load(f, allow_pickle=True)
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

    print('\nSaving model weights...')
    model.save_weights(config.MODEL_CHECKPOINT)
    return model


def test_predict():
    classifier = PiecesClassifier()
    image = cv2.imread('./pieces/b_/00.png', cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, config.INPUT_SHAPE,
                       interpolation=cv2.INTER_LINEAR)
    image = image / 255.0
    image = np.expand_dims(image, 0)
    print(classifier.predict(image))


if __name__ == '__main__':
    # train_model()
    test_predict()
