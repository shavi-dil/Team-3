import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from numpy import array
from math import isnan

def are_equal(column):
    array = column.to_numpy()

    return (array[0] == array).all()

def create_dataset(data, time_step = 1):
    x, y = [], []
    for i in range(len(data) - time_step, - 1):
        x.append(data[i:(i + time_step), 0])
        y.append(data[i + time_step, 0])
    return array(x), array(y)

def data_prep(data):
    #Remove all the columns we're not training on
    for column in data.columns.difference(['YEAR_SINCE', 'AADT_ALLVE', 'LOCAL_ROAD', 'DECLARED_R', 'PER_TRUCKS']):
        data = data.drop(column, axis = 1)
    
     #remove constant columns
    for column in data.columns:
        if are_equal(data[column]):
            print("Removing ", data[column])
            del data[column]

    #Check for None
    count = 0
    for row in data.itertuples():
        if row.DECLARED_R is None or row.LOCAL_ROAD is None or row.DECLARED_R == 'Missing Data':
            data = data.drop(count)
        count += 1
    #Check for NaN
    count = 0
    for row in data.itertuples():
        if isnan(row.PER_TRUCKS):
            data = data.drop([count])
        count += 1

    roads = data.LOCAL_ROAD.unique()
    dic = dict((a, b) for a, b in enumerate(roads))
    data['LOCAL_ROAD'] = data['LOCAL_ROAD'].map(dic)
    #data['LOCAL_ROAD'] = data['LOCAL_ROAD'].factorize()[0]
    otherRoads = data.DECLARED_R.unique()
    dic = dict((a, b) for a, b in enumerate(otherRoads))
    data['DECLARED_R'] = data['DECLARED_R'].map(dic)
    #data['DECLARED_R'] = data['DECLARED_R'].factorize()[0]

    #print(data['LOCAL_ROAD'])
    #lr = data['LOCAL_ROAD']
    #lr = pd.Categorical(lr)

    x = data[['LOCAL_ROAD', 'DECLARED_R']]
    #x = lr
    y = data['PER_TRUCKS']

    return data
    

def forest_data(data):
    #Multiply PER_TRUCKS by 100, then can convert to integer so that it can be fit with random forest.
    #This is the equivalent of having the data be cars per 1500 minutes. Correlations should still be useful as they're just comparing against each other?
    data['PER_TRUCKS'] = data['PER_TRUCKS'].apply(lambda x: int(x*100))

    data, x, y = data_prep(data)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 1)

    return x_train, x_test, y_train, y_test

def gru(data):
    data, x, y = data_prep(data)

    scalar = MinMaxScaler(feature_range = (0, 1))
    scaled_data = scalar.fit_transform(data.values)

    forecast_start = 720
    train, test = scaled_data[: forecast_start, :], scaled_data[forecast_start : 850, :]

    #x, y = create_dataset(scaled_data)
    #x = x.reshape(x.shape[0], x.shape[1], 1)

    return scaled_data


def prepare_data(data, model = None):
    if model.lower() == 'forest': return forest_data(data)

    elif model.lower() == 'gru': return gru(data)