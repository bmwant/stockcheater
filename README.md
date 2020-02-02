### Recognize board on the screen

1. Collect as many images for pieces from any pieces sets displayed on a screen
with `grab_pieces.py`
2. Generate dataset from images after you have sorted pictures manually within
`pieces` directory. Make sure to have at least 10 examples to each type of piece
and then launch `create_dataset.py`
3. Train Keras model on your dataset with `recognizer.py`

### Launch move advisor

1. Open application
```bash
$ python main.py
```

2. Launch game on your favourite game platform (e.g. [lichess](https://lichess.org/))

3. When you need a hint just click on a tray icon as shown below


