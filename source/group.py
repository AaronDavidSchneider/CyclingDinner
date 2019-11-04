from source.couple import couple
import numpy as np
import requests
import json
import source.config as c
import googlemaps
from geopy.distance import geodesic
import itertools

gd = {"H":1,"V":0, "N":2}
gd_inv = {1:"H",0:"V", 2:"N"}
# CONVERT TIMES TO POSIX TIME
from datetime import timezone, datetime, timedelta
dinner_time = {}
for t in range(len(c.TIMES)):
    h = int(c.TIMES[t][:2])
    m = int(c.TIMES[t][3:5])
    dinner_time[gd_inv[t]] = int(datetime(int(c.YEAR),int(c.MONTH),int(c.DAY),h,m, tzinfo=timezone(timedelta(hours=c.TIMEZONE))).strftime("%s"))

class group:
    """docstring for group."""
    def __init__(self, couples, host):
        self.couples = couples
        self.dist = np.zeros((3,3))
        self.group_loss = 0
        self.gmaps_client = googlemaps.Client(key = c.API_KEY)
        self.host = host

    def get_dist(self,A,gmaps=False):
        if gmaps:
            if A.transp=="transit":
                x = self.gmaps_client.directions(A.address,self.couples[self.host].address,mode=A.transp,arrival_time=dinner_time[self.couples[self.host].food])
            else:
                x = self.gmaps_client.directions(A.address,self.couples[self.host].address,mode=A.transp)

            d = x[0]["legs"][0]["distance"]["value"]
            d_min = x[0]["legs"][0]["duration"]["value"]
        else:
            d = geodesic(A.location.point,self.couples[self.host].location.point).km
            if A.transp == "bicycling":
                v = 15/60  # km/min
            elif A.transp == "driving":
                v = 50/60  # km/min
            elif A.transp == "transit":
                v = 5/60  # km/min
            else:
                print("ERROR: false transportation was chosen")
            d_min = d / v
        return d_min

    def calc_group_loss(self,gmaps=False):
        dist = 0
        for A in self.couples:
            dist += np.square(self.get_dist(A.pre,gmaps))
        return np.sqrt(dist)

    def get_loss(self,gmaps=False):
        if self.couples[self.host].food=="V":
            self.group_loss = 0
        else:
            self.group_loss = self.calc_group_loss(gmaps)
        return self.group_loss
