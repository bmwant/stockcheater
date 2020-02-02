import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split


CLASS_NAMES = (
    'r',  # black rook
    'n',  # black night
    'b',  # black bishop
    'q',  # black queen
    'k',  # black king
    'p',  # black pawn
    'R',  # white rook
    'N',  # white night
    'B',  # white bishop
    'Q',  # white queen
    'K',  # white king
    'P',  # white pawn
    '-',  # empty cell
)
MODEL_CHECKPOINT = './checkpoints/model_weights.ckpt'


class PiecesClassifier(object):
    def __init__(self, model=None):
        self.model = model or self.load_model()

    def load_model(self):
        model = create_model()
        model.load_weights(MODEL_CHECKPOINT)
        return model

    def predict(self, image) -> int:
        predictions = self.model.predict(image)
        class_index = np.argmax(predictions[0])
        return class_index


def create_model():
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(26, 26)),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dense(len(CLASS_NAMES), activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'],
    )
    return model


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
    model.save_weights(MODEL_CHECKPOINT)
    return model


def test_predict():
    import cv2
    dc = DigitsClassifier()
    image = cv2.imread('train_images/0/058.jpg', cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (26, 26), interpolation=cv2.INTER_LINEAR)
    image = image / 255.0
    image = np.expand_dims(image, 0)
    print(dc.predict(image))


if __name__ == '__main__':
    train_model()
