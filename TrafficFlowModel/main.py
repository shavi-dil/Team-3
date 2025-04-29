import pandas as pd
from data_prep import prepare_data
from feature_selection import select_features

data = pd.read_csv("Traffic_Count_Locations_with_LONG_LAT.csv")

data_train, data_test = prepare_data(data)

select_features(data_train)

print(data.head(0))