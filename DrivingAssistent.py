import datetime

import requests
import datetime

class DrivingAssistant:
    __error = False


    def __init__(self):
        self.url = "https://maps.googleapis.com/maps/api/distancematrix/json?"
        self.home = "Iasi, Calea Dacilor, nr.14"
        self.harmony = "Bulevardul Carol I 27, Iași"
        self.pu = "Piata Unirii, Iasi"
        self.mitropolie = "Catedrala Mitropolitana, Iasi"
        self.faculty = "Automatica si Calculatoare, Iasi"
        apiFile = open("api.txt", "r")
        self.key = apiFile.readline()

        # try:
        #
        # except:
        #     self.__error = True
        # finally:
        #     print("Couldn't open the file for the API key")


    def fromHomeTo(self, destination: str) -> [str, str, str]:
        r = requests.get(self.url+"departure_time=now"
                         + "&destinations=" + destination + "&origins="+self.home
                         + "&key=" + self.key)

        if(r.json()["status"] != "OK"):
            print("Nu am reusit sa gasesc")
        else:
            distance = r.json()["rows"][0]["elements"][0]["distance"]["text"]
            time = r.json()["rows"][0]["elements"][0]["duration"]["text"]
            time_in_traffic = r.json()["rows"][0]["elements"][0]["duration_in_traffic"]["text"]
            return [distance, time, time_in_traffic]


    def fromHometoHarmony(self) -> [str, str, str]:
        return self.fromHomeTo(self.harmony)

    def fromHomeToPU(self) -> [str, str, str]:
        return self.fromHomeTo(self.pu)

    def fromHomeToMitroplie(self) -> [str, str, str]:
        return self.fromHomeTo(self.mitropolie)

    def fromHomeToFaculty(self) -> [str, str, str]:
        return self.fromHomeTo(self.faculty)

    def getError(self):
        return self.__error


