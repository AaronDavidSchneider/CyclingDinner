from source.couple import couple
import pandas as pd
import random
from itertools import combinations
import numpy as np

from time import sleep

gd = {"H":1,"V":0, "N":2}
gd_inv = {1:"H",0:"V", 2:"N"}

column_mapping = {
    "Straße und Hausnummer":"address",
    "Welcher Name steht auf dem Klingelschild?":"name",
    "Welchen Gang würdet ihr vorzugsweise vorbereiten? (nicht garantiert)":"food",
    "Postleitzahl":"PLZ",
    "Meldest du dich als Team an?":"single",
    "Transportmittel":"transportation",
    "relevante Infos (vegetarisch, vegan, Nussallergie, Laktoseintolerant etc.)":"notes",
    "Email": "mail",
    "Handynummer": "phone"
}

transp_mapping = {
    "Fahrrad":"bicycling",
    "Auto":"driving",
    "Bahn":"transit"
}

food_mapping = {
    "Vorspeise":"V",
    "Hauptspeise":"H",
    "Nachspeise":"N"
}

single_mapping = {
    "Ja, wir füllen das Formular zu zweit aus":False,
    "Nein, ich will zufällig zugeteilt werden":True
}

def rearange_teams(data_sorted):
    """ Rearange Teams if difference between courses is too high """
    counts = [len(x.index) for x in data_sorted]
    diff = np.max(counts) - counts
    while np.sum(diff) > np.sum(counts) % 3:
        highest = np.argmax(counts)
        lowest = np.argmin(counts)

        i = random.randint(0,counts[highest]-1)
        temp = data_sorted[highest].iloc[i].copy()
        data_sorted[highest] = data_sorted[highest].drop(data_sorted[highest].index[i])
        temp.food = gd_inv[lowest]
        data_sorted[lowest] = data_sorted[lowest].append(temp)

        counts = [len(x.index) for x in data_sorted]
        diff = np.max(counts) - counts
    return data_sorted

def combine_singles(data_sorted,singles,best_possible_rest):
    """ Not working yet!!! """
    counts = [len(x.index) for x in data_sorted]
    diff = np.max(counts) - counts
    while np.sum(diff) > best_possible_rest:
        highest = np.argmin(counts)
        lowest = np.argsort(diff)[0]
        try:
            temp = singles[singles.food==gd_inv[lowest]].sample(2,replace=False).copy()
        except ValueError:
            try:
                temp = singles[singles.food==gd_inv[lowest]].sample(1,replace=False).copy()
                temp.append(singles.sample(1,replace=False))
            except ValueError:
                temp = singles.sample(2,replace=False).copy()

        singles.drop(temp.index)
        temp.food=gd_inv[lowest]
        data_sorted[lowest].append(temp)

        counts = [len(x.index) for x in data_sorted]
        diff = np.max(counts) - counts
    return data_sorted

def create_couples(data_sorted, singles):
    # merge people
    counts = [len(x.index) for x in data_sorted]

    if len(singles.index) % 2 != 0:
        print("Problem: pairs couldnt be assigned, one person is dropped randomly:")
        i = random.randint(0,len(singles.index)-1)
        print(singles.iloc[i])
        singles.drop(i)

    diff = np.max(counts) - counts
    best_possible_rest = (np.sum(counts) + len(singles.index)/2) % 3
    print(f"the best possible arrangement has rest: {best_possible_rest}")

    if np.sum(diff)>(len(singles.index)/2):
        print("Teams need to be rearanged!")
        data_sorted = rearange_teams(data_sorted)

    #if len(singles.index)>=2:
    #    data_sorted = combine_singles(data_sorted,singles,best_possible_rest)

    return data_sorted


def import_data(file):
    # important: only works if file is well structured!!!
    data = pd.read_csv(file, dtype=str)

    data = data.rename(columns = column_mapping)
    data = data.replace({"food": food_mapping})
    data = data.replace({"transportation": transp_mapping})
    data = data.replace({"single": single_mapping})
    data = data.astype({"single": bool})

    print(data)

    V_pd = data[np.logical_and(data.food == "V",~data.single)]
    H_pd = data[np.logical_and(data.food == "H",~data.single)]
    N_pd = data[np.logical_and(data.food == "N",~data.single)]

    data_sorted = [V_pd,H_pd,N_pd]

    data_sorted = create_couples(data_sorted, data[data.single])

    counts = [len(x.index) for x in data_sorted]
    diff = np.max(counts) - counts

    V, H, N = [],[],[]

    V_pd,H_pd,N_pd = data_sorted

    print(V_pd)
    print(H_pd)
    print(N_pd)

    if np.sum(diff)!=0:
        print("ERROR: no combination possible!!!")
    else:
        for k in V_pd.to_numpy():
            V.append(couple(dict(zip(V_pd.keys(),k))))
        for k in H_pd.to_numpy():
            H.append(couple(dict(zip(H_pd.keys(),k))))
        for k in N_pd.to_numpy():
            N.append(couple(dict(zip(N_pd.keys(),k))))

    return V,H,N
