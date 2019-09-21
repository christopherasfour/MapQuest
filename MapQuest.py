import json
import urllib.parse
import urllib.request


class MapQuest:
    def __init__(self, key):
        self.API_KEY = key
        self.BASE_URL = "http://open.mapquestapi.com/directions/v2/route?"
        self.GEOCODE_URL = "http://www.mapquestapi.com/geocoding/v1/address?"
        self.POI_URL = "https://www.mapquestapi.com/search/v4/place?"

    def totalDistance(self, locations: list) -> float:
        totalDistance = 0
        if len(locations) == 0 or len(locations) == 1:
            return totalDistance
        else:
            for i in range(len(locations)-1):
                query_parameters = [
                    ("key", self.API_KEY), ("from", locations[i]), ("to", locations[i+1])]
                url = self.BASE_URL + urllib.parse.urlencode(query_parameters)
                response = urllib.request.urlopen(url)
                data = json.load(response)
                totalDistance += data["route"]["distance"]
            return totalDistance
                
    def totalTime(self, locations: list) -> float:
        totalTime = 0
        if len(locations) == 0 or len(locations) == 1:
            return totalTime
        else:
            for i in range(len(locations)-1):
                query_parameters = [
                    ("key", self.API_KEY), ("from", locations[i]), ("to", locations[i+1])]
                url = self.BASE_URL + urllib.parse.urlencode(query_parameters)
                response = urllib.request.urlopen(url)
                data = json.load(response)
                totalTime += data["route"]["time"]
            return totalTime
    
    def directions(self, locations: list) -> str:
        completeDirections = ""
        if len(locations) == 0 or len(locations) == 1:
            return completeDirections
        else:
            for i in range(len(locations)-1):
                query_parameters = [
                    ("key", self.API_KEY), ("from", locations[i]), ("to", locations[i+1])]
                url = self.BASE_URL + urllib.parse.urlencode(query_parameters)
                response = urllib.request.urlopen(url)
                data = json.load(response)

                for j in range(len(data["route"]["legs"])):
                    for k in range(len(data["route"]["legs"][j]["maneuvers"])):
                        completeDirections += data["route"]["legs"][0]['maneuvers'][k]["narrative"] + "\n"
            return completeDirections

    def pointOfInterest(self, locations: str, keyword: str, results: int) -> list:
        geocode_parameters = [("key", self.API_KEY), ("location", locations)]
        geocode_url = self.GEOCODE_URL + urllib.parse.urlencode(geocode_parameters)
        response = urllib.request.urlopen(geocode_url)
        data = json.load(response)
        latitude = (data["results"][0]["locations"][0]["latLng"]["lat"])
        longitude = (data["results"][0]["locations"][0]["latLng"]["lng"])
        
        query_parameters = [("location", str(longitude) + "," + str(latitude)), ("sort", "distance"),
                            ("feedback", "false"), ("key", self.API_KEY),
                            ("limit", results), ("q", keyword)]
        POI_url = self.POI_URL + urllib.parse.urlencode(query_parameters)
        response2 = urllib.request.urlopen(POI_url)
        data2 = json.load(response2)
        destinations = []
        for i in range(len(data2["results"])):
            destinations.append(data2["results"][i]["displayString"])
        return (destinations)

