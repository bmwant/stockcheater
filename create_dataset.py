import os

import cv2
import numpy as np

import config


def get_dirs(directory):
    for file_name in os.listdir(directory):
        path = os.path.join(directory, file_name)
        if os.path.isdir(path):
            yield path


def get_files(directory, ext=''):
    for file_name in os.listdir(directory):
        if file_name.endswith(ext):
            yield os.path.join(directory, file_name)


def get_class(class_name) -> int:
    if class_name == 'dot':
        class_name = '.'
    return make_model.class_names.index(class_name)


def normalize_names():
    for d in get_dirs(config.PIECES_DIR):
        # make sure listing will not be mutated during renaming
        files = list(get_files(d, ext='png'))
        for i, f in enumerate(files):
            os.rename(
                f,
                os.path.join(os.path.dirname(f), '{:02d}.png'.format(i))
            )


def main():
    data = []
    for d in get_dirs(config.PIECES_DIR):
        class_name = os.path.basename(d)
        class_index = get_class(class_name)
        for f in get_files(d, ext='png'):
            gray_image = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
            resized_image = cv2.resize(
                gray_image, config.INPUT_SHAPE, interpolation=cv2.INTER_LINEAR)
            data.append((resized_image, class_index))

    print('Saving dataset to a file...')
    with open('dataset.np', 'wb') as f:
        np.save(f, data)


if __name__ == '__main__':
    main()
