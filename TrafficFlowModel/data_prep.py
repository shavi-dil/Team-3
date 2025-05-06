import pandas as pd
from sklearn.model_selection import train_test_split

def are_equal(column):
    array = column.to_numpy()

    return False#(array[0] == array).all()

def prepare_data(data):
    #remove constant columns
    for column in data.columns:
        if are_equal(data[column]):
            print("Removing ", data[column])
            del data[column]

    #Should also add a function to remove null values
    count = 0
    for row in data.itertuples():
        if row.DECLARED_R is None or row.LOCAL_ROAD is None or row.DECLARED_R == 'Missing Data':
            data = data.drop(count)
        count += 1

    #roads = data.LOCAL_ROAD.unique()
    #dic = dict((a, b) for a, b in enumerate(roads))
    #data['LOCAL_ROAD'] = data['LOCAL_ROAD'].map(dic)
    #data['LOCAL_ROAD'] = data['LOCAL_ROAD'].factorize()[0]

    #print(data['LOCAL_ROAD'])
    lr = data[['LOCAL_ROAD', 'DECLARED_R']]
    lr = pd.Categorical(lr)

    #x = data[['LOCAL_ROAD', 'DECLARED_R']]
    x = lr
    y = data['PER_TRUCKS']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 1)

    return x_train, x_test, y_train, y_test