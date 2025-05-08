from sys import argv
import pandas as pd
from data_prep import prepare_data
from feature_selection import select_features
from train import train_RandomForest, train_gru

data = pd.read_csv("Traffic_Count_Locations_with_LONG_LAT.csv")

if argv[1].lower() == 'forest': 
    x_train, x_test, y_train, y_test = prepare_data(data)
    #select_features(data_train)
    train_RandomForest(x_train, x_test, y_train, y_test)

elif argv[1].lower() == 'gru':
    x, y = prepare_data(data)
    train_gru()

else: print("Usage, python main.py <model>")