import pandas as pd

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

    data_test = data.sample(n = 10000)
    data_test = data_test.reset_index(drop = True)

    return data, data_test