from House import House
from joblib import dump, load
import pandas as pd
import numpy as np
from geopy.distance import geodesic

def getDf(area, rooms, bathrooms, garages, sel, lon, lat):
    df = pd.DataFrame({'area': [], 'rooms': [], 'bathrooms': [], 'garages': [
    ], 'sel': [], 'longitude': [], "latitude": []})
    new_row = {'area': area, 'rooms': rooms, 'bathrooms': bathrooms,
               'garages': garages, 'sel': sel, 'longitude': lon, 'latitude': lat}
    df = df.append(new_row, ignore_index=True)
    return df


def prediction(area, rooms, bathrooms, garages, sel, lon, lat):
    area1 = float(area)
    rooms1 = float(rooms)
    bathrooms1 = float(bathrooms)
    garages1 = float(garages)
    sel1 = float(sel)
    lon1 = float(lon)
    lat1 = float(lat)

    area1 = np.log1p(area1)
    rooms1 = np.log1p(rooms1)

    df = getDf(area1, rooms1, bathrooms1, garages1, sel1, lon1, lat1)
    clf = load('files/regressor.joblib')
    result = clf.predict(df)
    pred = np.expm1(result).tolist()
    return pred[0]


def getNearHouses(originLon, originLat):
    
    df = load('files/dataframe.joblib')
    df['distance'] = float('inf')
    houses = []

    coords_1 = (originLat, originLon)

    for i in df.index:
        df['distance'][i] = geodesic(
        coords_1, (df['latitude'][i], df['longitude'][i])).m

    result = df.sort_values('distance').head(5)

    for i in result.index:
        tup = [df['area'][i], df['rooms'][i], df['bathrooms'][i], df['garages'][i], df['sel'][i], 
                df['price'][i],df['latitude'][i], df['longitude'][i], df['url'][i]] 
        houses.append(tup)

    return houses
