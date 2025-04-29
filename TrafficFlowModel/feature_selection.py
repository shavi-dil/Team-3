import seaborn as sns
import matplotlib.pyplot as plt

def select_features(data):
    #data.hist()
    #plt.show()

    #Show correlation heatmap, ignoring the particular intersection
    #This will show what things contribute to traffic ignoring the actual location.
    dataHeat = data
    del dataHeat['TFM_DESC']
    del dataHeat['TFM_TYP_DE']
    del dataHeat['MOVEMENT_T']
    del dataHeat['SITE_DESC']
    del dataHeat['DECLARED_R']
    del dataHeat['LOCAL_ROAD']
    del dataHeat['DATA_SRC_C']
    del dataHeat['DATA_SOURC']
    del dataHeat['TIME_CATEG']

    sns.heatmap(dataHeat.corr(), cmap = 'Greens', annot = True)
    plt.show()#Not much correlation really

    #Next, we need to find the amount of traffic per intersection, which I think will perform better
    intersections = []#A list of each intersection
    for intersection in data['SITE_DESC']:
        intersections.append(data['SITE_DESC'].unique())

    for intersection in intersections:
        print(intersection)#Test