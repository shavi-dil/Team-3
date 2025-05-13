from sklearn.ensemble import RandomForestClassifier
from torch import tensor, float32
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from torch.nn import MSELoss
from torch.optim import adam
from torch.utils.data import TensorDataset, DataLoader
from torchvision.models import DenseNet
from numpy import array, reshape
from GRUmodel import GRUMODEL


def train_lstm(x_train, x_test, y_train, y_test):
    scalar = MinMaxScaler(feature_range = (0, 1))
    

def train_RandomForest(x_train, x_test, y_train, y_test):
    clf = RandomForestClassifier()

    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)

    print("Random Forest classification report:")
    print(classification_report(y_test, y_pred))

    print("Random Forest confusion matrix:")
    print(confusion_matrix(y_pred, y_test))

    print("Accuracy score: ", accuracy_score(y_test, y_pred))

def create_labels(data):
    x = array([data[i:i+4] for i in range(len(data) - 4)])
    y = array(data[4:])

    return x, y

def train_gru(scaled_data):
    step_size = 4
    N = 850
    forecast_start = 720
    
    values = scaled_data.values
    
    train, test = values[:forecast_start, :], values[forecast_start:N, :]

    x_train, y_train = create_labels(train)
    x_test, y_test = create_labels(test)

    x_train = reshape(x_train, (x_train[0], 1, x_train.shape[1]))
    x_test = reshape(x_test.shape[0], 1, x_test.shape[[1]])

    x_train_tensor = tensor(x_train, dtype = float32)
    y_train_tensor = tensor(y_train, dtype = float32)
    x_test_tensor = tensor(x_test, dtype = float32)
    y_test_tensor = tensor(y_test, dtype = float32)

    train_data = TensorDataset(x_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_data, batch_size = 64)

    #Model definition and training
    model = GRUMODEL(input_size = step_size, hidden_size = 128, output_size = 1)
    criterion = MSELoss()
    optimizer = adam(model.parameters())#Need to put in learning rate probably.

    

    #TODO
    #https://www.datatechnotes.com/2024/05/sequence-prediction-with-gru-model-in.html