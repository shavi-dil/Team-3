from torch import Tensor
from torch.utils.data import TensorDataset, DataLoader
from torch.nn import MSELoss
from torch.optim import Adam
import torch
from numpy import array, reshape, resize
from pandas import read_csv
from GRUmodel import GRUMODEL
import matplotlib.pyplot as plt
from data_prep import data_prep

def create_labels(data, step):
    x = array([data[i:i+step] for i in range(len(data) - step)])
    y = array(data[step:])

    return x, y

def train_model(train_data, input_size, hidden_size, output_size, learning_rate, epochs):
    train_loader = DataLoader(train_data, batch_size = 64)
    
    model = GRUMODEL(input_size = input_size, hidden_size = hidden_size, output_size = output_size)
    criterion = MSELoss()
    optimizer = Adam(model.parameters(), lr = learning_rate)

    for epoch in range(epochs):
        model.train()
        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            
            output = model(batch_x)

            loss = criterion(output, batch_y)

            loss.backward()

            optimizer.step()

        print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

    return model

def main():
    step_size = 5
    N = 41864
    forecast_start = 33492

    data = read_csv('Traffic_Count_Locations_with_LONG_LAT.csv')
    data = data_prep(data)
    values = data.values

    train, test = values[: forecast_start, :], values[forecast_start: N, :]

    x_train, y_train = create_labels(train, step_size)
    x_test, y_test = create_labels(test, step_size)

    x_train = reshape(x_train, (x_train.shape[0] * 5, 1, x_train.shape[1]))
    x_test = reshape(x_test, (x_test.shape[0] * 5, 1, x_test.shape[1]))
    y_train = reshape(y_train, (y_train.shape[0] * 5, 1))
    y_test = reshape(y_test, (y_test.shape[0] * 5, 1))

    x_train = Tensor(x_train.astype(float))
    y_train = Tensor(y_train.astype(float))
    x_test = Tensor(x_test.astype(float))
    y_test = Tensor(y_test.astype(float))

    train_data = TensorDataset(x_train, y_train)

    #Hyperparameters
    input_size = step_size
    hidden_size = 128
    output_size = 1
    epochs = 10
    learning_rate = 0.0001

    model = train_model(train_data, input_size, hidden_size, output_size, learning_rate, epochs)

    #Test
    with torch.no_grad():
        model.eval()
        testPredict = model(x_test)

    #Result visualisation
    index = range(len(y_test))
    plt.plot(index, y_test, label="Ground truth")
    plt.plot(index, testPredict.numpy(), label="Predicted")
    plt.legend()
    plt.show()

main()