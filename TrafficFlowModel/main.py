import pandas as pd
from data_prep import prepare_data
from feature_selection import select_features
from train import train

data = pd.read_csv("Traffic_Count_Locations_with_LONG_LAT.csv")

x_train, x_test, y_train, y_test = prepare_data(data)

#select_features(data_train)

train(x_train, x_test, y_train, y_test)