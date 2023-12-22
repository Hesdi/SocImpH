import numpy
import matplotlib.pyplot as plt
import tensorflow
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import MinMaxScaler

# Fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
tensorflow.random.set_seed(seed)

# Create model
model = Sequential()
model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
model.add(Dense(8, kernel_initializer='uniform', activation='relu'))
model.add(Dense(12, input_dim=4, kernel_initializer='uniform', activation='relu'))

# Load training data
dataset = numpy.loadtxt("learned_barrier_model.csv", delimiter=",")
Y_train = dataset[:, 4]
X_train = dataset[:, 0:4]

# Scale the data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
history = model.fit(X_train, Y_train, validation_split=0.2, epochs=150, batch_size=10, verbose=0)

# Test data filename
test_data_file = "live_weather_data.csv"

# Function to load test data
def load_test_data(filename):
    test_dataset = numpy.loadtxt(filename, delimiter=",")
    test_dataset = test_dataset.reshape(1, -1)
    return test_dataset

# Load and evaluate test data
X_test = load_test_data(test_data_file)
X_test = scaler.transform(X_test)  # Scale the test data

# Print test predictions
test_predictions = model.predict(X_test)
print(test_predictions)


# Summarize history for loss


plt.title('model accuracy')
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()



plt.title('model loss')
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()










