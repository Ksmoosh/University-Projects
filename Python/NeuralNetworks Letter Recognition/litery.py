import numpy as np
import os
import cv2
from tqdm import tqdm
import random
import pickle
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import Adadelta
from matplotlib.pyplot import plot, show, xlabel, ylabel

IMG_SIZE = 50

DATADIR = "hand"

CATEGORIES = ["b", "c", "f", "l", "m", "o", "p", "r", "s", "w"]

training_data = []

def create_training_data():
    for category in CATEGORIES:

        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)

        for img in tqdm(os.listdir(path)):
            try:
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_GRAYSCALE)
                new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array, class_num])
            except Exception as e:
                pass
    return training_data


def save_training_data(training_data):
    random.shuffle(training_data)

    X = []
    y = []

    for features, label in training_data:
        X.append(features)
        y.append(label)

    X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

    pickle_out = open("X.pickle", "wb")
    pickle.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open("y.pickle", "wb")
    pickle.dump(y, pickle_out)
    pickle_out.close()

def stworz_model(X, y):
    X = X / 255.0

    model = Sequential()

    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', input_shape=X.shape[1:]))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())

    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation('softmax'))

    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=Adadelta(),
                  metrics=['accuracy'])

    x = []
    loss = []

    for i in range(15):
        x.append(model.fit(X, y, batch_size=16, epochs=1, validation_split=0.3).history.values())
        loss.append(list(x[i])[0])

    model.save('wuenodwa.h5')

    pickle_out = open("loss.pickle", "wb")
    pickle.dump(loss, pickle_out)
    pickle_out.close()

    return model, loss

def zaladuj_model():
    model = load_model('wuenodwa.h5')

    pickle_in = open("loss.pickle", "rb")
    loss = pickle.load(pickle_in)

    return model, loss


def load_training_data():
    pickle_in = open("X.pickle", "rb")
    X = pickle.load(pickle_in)

    pickle_in = open("y.pickle", "rb")
    y = pickle.load(pickle_in)

    return X, y

def plot_loss(loss):
    plot(loss)
    ylabel("loss")
    xlabel("epoch")
    show()

def predict_im(image):
    img_array = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    new_array = np.array(new_array).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    new_array = new_array / 255.0
    predictions = model.predict(new_array)
    print(CATEGORIES[np.argmax(predictions[0])])


if __name__=="__main__":
    while 1:
        nowy_obecny = int(input("Stworzyc nowy model sieci neuronowej(1), czy wykorzystać obecny(2)?: "))
        if nowy_obecny == 1:
            training_data = create_training_data()
            save_training_data(training_data)
            X, y = load_training_data()
            model, loss = stworz_model(X, y)
            plot_loss(loss)
            break
        elif nowy_obecny == 2:
            X, y = load_training_data()
            model, loss = zaladuj_model()
            break
        else:
            print("Błąd!")

    while 1:
        przykladowy_wpisz = int(input("Użyć przykładowy obrazek z literą do przetestowania sieci(1), czy konkretny(2)?: "))
        if przykladowy_wpisz == 1:
            image = "hand/s/img029-009.png"
        elif przykladowy_wpisz == 2:
            image = input("Podaj scieżkę obrazka do predykcji: ")
        else:
            print("Błąd!")
            continue
        predict_im(image)
        break

