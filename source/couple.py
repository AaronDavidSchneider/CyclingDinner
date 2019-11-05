import numpy as np
import source.config as c
from geopy.geocoders import GoogleV3
import wget
from slugify import slugify
geolocator = GoogleV3(api_key=c.API_KEY)

gang_dict = {"V": 0, "H": 1, "N": 2}


class couple:
    def __init__(self, data):
        self.address = "{street}, {PLZ}".format(street=data["address"],
                                                PLZ=data["PLZ"])
        self.name = data["name"]
        self.food = data["food"]
        self.phone = data["phone"]
        self.mail = data["mail"]
        self.transp = data["transportation"]
        self.note = data["notes"]
        self.pre = None
        self.location = geolocator.geocode(self.address)
        if self.location is None:
            print(self.address)

    def print_info(self, gang):
        result = ""
        #result += "Adresse: {}\n".format(self.address)
        result += "Name: {}\n".format(self.name)
        #result += "Unterwegs mit: {}\n".format(self.transp)
        result += "Unverträglichkeiten, etc: {}\n".format(self.note)
        if gang == gang_dict[self.food]:
            result += "Host:\n"
            result += "Adresse: {}\n".format(self.address)
            #result += "Name: {}\n".format(self.name)
        return result

    def set_final_combination(self, combination):
        self.dinner = {
            "V": combination.combination_get_host(self, 0),
            "H": combination.combination_get_host(self, 1),
            "N": combination.combination_get_host(self, 2)
        }
        self.guests = combination.combination_get_guests(self)

        print(self.name+" provides {}".format(self.food))
        print(self.name+" has dinner at: {}, {}, {}".format(*[self.dinner[c].name for c in ["V","H","N"]]))
        print(self.name+" has these guests: {}, {}, {}".format(*[self.guests[c].name for c in ["V","H","N"]]))
        print("")

    def print_met_people(self,combination):
        self.teams_met = combination.met_people(self)
        teams_met_string = [f"{couple.name}, " for couple in self.teams_met]
        result = self.name+" hat gesehen: "
        for i in range(len(self.teams_met)):
            result += teams_met_string[i]
        result += " ({} Teams)".format(len(self.teams_met))
        print(result)


    def print_map(self):
        locs = [self.dinner[c].location for c in ["V","H","N"]]
        long, lat = [l.longitude for l in locs], [l.latitude for l in locs]

        address = [f"{lat[i]},{long[i]}" for i in range(3)]

        url = f"https://maps.googleapis.com/maps/api/staticmap?zoom=12&scale=2&size=600x600&maptype=roadmap&key={c.API_KEY}&format=png&visual_refresh=true&markers=size:mid%7Ccolor:0xff0000%7Clabel:V%7C{address[0]}&markers=size:mid%7Ccolor:0xff0000%7Clabel:H%7C{address[1]}&markers=size:mid%7Ccolor:0xff0000%7Clabel:N%7C{address[2]}"
        wget.download(url, "maps/{}.png".format(slugify(self.mail)))
