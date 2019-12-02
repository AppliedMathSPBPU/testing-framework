from tensorflow.python.keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Conv2D, MaxPooling2D
from tensorflow.python.keras.layers import Activation, Dropout, Flatten, Dense


class TestModel:
    def __init__(self):
        # Каталог с данными для обучения
        self.train_dir = 'train'
        # Размеры изображения
        self.img_width, self.img_height = 150, 150
        # Размерность тензора на основе изображения для входных данных в нейронную сеть
        # backend Tensorflow, channels_last
        self.input_shape = (self.img_width, self.img_height, 3)
        # Количество эпох
        self.epochs = 10
        # Размер мини-выборки
        self.batch_size = 16
        # Количество изображений для обучения
        self.nb_train_samples = 17500
        # Количество изображений для проверки
        self.nb_validation_samples = 3750
        # Количество изображений для тестирования
        self.nb_test_samples = 3750

        self.model = Sequential()
        self.model.add(Conv2D(32, (3, 3), input_shape=self.input_shape))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(32, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Conv2D(64, (3, 3)))
        self.model.add(Activation('relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))

        self.model.add(Flatten())
        self.model.add(Dense(64))
        self.model.add(Activation('relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

        self.model.compile(loss='binary_crossentropy',
                    optimizer='adam',
                    metrics=['accuracy'])