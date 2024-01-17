#we use this library to play audios
import multiprocessing
import os.path
from multiprocessing import Value
import playsound
#we use this library for date and time
from datetime import time
from datetime import date

from selenium.webdriver import Keys

#our objects
from Agenda import Agenda
from Mail import Mail
from DrivingAssistent import DrivingAssistant
#we use this library for measuring time
import time
#we use this library for requests of a html
import requests
#we use to parse
from bs4 import BeautifulSoup
#we use this to select from the result of the parsing
import re
#we use this to do some audio
from gtts import gTTS
#we use this to open the webs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class VoiceAssistant:
    __on: bool

    def __init__(self, queue: multiprocessing.Queue):
        self.audiosFolder = "D:\Germany_Erasmus\Arduino\pythonProject\\audiosFolder"
        self.musicFolder = "D:\Germany_Erasmus\Arduino\pythonProject\music"
        self.__on = False
        self.__firstclap = Value('b', False)
        self.__counter = Value('i', 0)
        self.__musicCounter = Value('i', 0)
        self.__goOutCounter = Value('i', 0)
        self.start_time = 0
        self.end_time = 0
        self.queue = queue
        self.mail = Mail()

    def turn_on(self, temperature):
        file_path = "D:\Germany_Erasmus\Arduino\pythonProject\openedToday\\" + str(date.today())
        if(os.path.isfile(file_path) == False):
            #first time opened in that day, we send agenda and temperature
            self.say_something("firstTime.mp3")
            print()
            mdate = date.today()
            print(mdate)
            agenda = Agenda(mdate)
            agenda.printAgenda()
            if(agenda.plan == "Sir, I did not find any file for today!"):
                self.say_something("didntFindPlan.mp3")
            else:
                self.say_something("Plan sent .mp3")
                text = "The temperature in your room is: " + temperature + " Celsius degrees"
                self.mail.sendMail(agenda.plan + "\n" + text)
            f = open("openedToday/"+str(date.today()), "x")
            f.write("Plan for todat sent!")
        else:
            # plan already sent, we just want to know how it can help
            self.say_something("Hello Daniel Risa he.mp3")
        self.on = True

    def count(self):
        if(self.__firstclap.value == False):
            self.say_something("I am listening .mp3")
            self.turnTimerOn()
            self.__firstclap.value = True
            p = multiprocessing.Process(target=self.countProcess, args=(self.start_time, self.queue))
            p.start()
        else:
            if(self.__firstclap.value == True):
                self.queue.put("clap")

    def countProcess(self, startTime, q: multiprocessing.Queue):
        endTime = time.time()
        elapsedTime = endTime - startTime
        while(elapsedTime < 5):
            endTime = time.time()
            elapsedTime = endTime - startTime
            if(q.empty() is not True):
                element = q.get()
                if(element == "clap"):
                    print("He clapped")
                    self.__counter.value += 1
        print("He clapped: " + str(self.__counter.value) + " times")
        if(self.__counter.value == 0):
            print("I didn't hear any clap")
            self.say_something("noclap.mp3")
            self.__counter.value = 0
            self.__firstclap.value = False
        elif(self.__counter.value == 1):
            print("I will put you some music")
            self.say_something("musichoices.mp3")
            startTime = time.time()
            songP = multiprocessing.Process(target=self.playMusic, args=(startTime, self.queue))
            songP.start()
        elif(self.__counter.value == 2):
            #sending an email with the news
            # here I want to webscrape the news and then open the links
            self.say_something("sportsnews.mp3")
            self.webScrapingTheNews()
            self.__counter.value = 0
            self.__firstclap.value = False
        elif(self.__counter.value == 3):
            print("I will give you the weather")

            self.say_something("weather.mp3")
            message = self.webScrapingWeather()
            self.mail.sendMail(message)

            self.__counter.value = 0
            self.__firstclap.value = False
        elif(self.__counter.value == 4):
            print("He wants to go out")
            self.say_something("goout.mp3")
            startTime = time.time()
            locationP = multiprocessing.Process(target=self.goOut, args=[startTime, self.queue])
            locationP.start()

        else:
            print("Too many clapes!")
            self.say_something("toomanyclapes.mp3")
            self.__counter.value = 0
            self.__firstclap.value = False


        # ce as mai vrea sa fac maine dimineata:
        # sa finalizez cu google api, poate ma folosest si de places
        # sa utilizez selenium pentru a deschide un link dat de webscraperul pentru stiri

    def playMusic(self, startTime, q: multiprocessing.Queue):
        endTime = time.time()
        elapsedTime = endTime - startTime
        while(elapsedTime < 5):
            endTime = time.time()
            elapsedTime = endTime - startTime
            if(q.empty() is not True):
                element = q.get()
                if(element == "clap"):
                    print("He clapped")
                    self.__musicCounter.value += 1
        if (self.__musicCounter.value == 0):
            print("I didn't hear any clap")
        elif (self.__musicCounter.value == 1):
            print("I will put you some The Weekend")
            self.say_something("theWeeknd.mp3")
            p = multiprocessing.Process(target=self.playSong, args=("TheWeeknd\The Weeknd - Blinding Lights (Official Audio).mp3",))
            p.start()
            self.__musicCounter.value = 0
            self.__counter.value = 0
            self.__firstclap.value = False
        elif (self.__musicCounter.value == 2):
            print("I will put you some Drake")
            self.say_something("drake.mp3")
            p = multiprocessing.Process(target=self.playSong, args=("Drake\God's Plan.mp3",))
            p.start()
            self.__musicCounter.value = 0
            self.__counter.value = 0
            self.__firstclap.value = False
        elif (self.__musicCounter.value == 3):
            print("I will put you some Post Malone")
            self.say_something("postMalone.mp3")
            p = multiprocessing.Process(target=self.playSong, args=("PostMalone\Post Malone - Circles.mp3",))
            p.start()
            self.__musicCounter.value = 0
            self.__counter.value = 0
            self.__firstclap.value = False
        elif (self.__musicCounter.value == 4):
            print("I will put you some The Motans")
            self.say_something("TheMotans.mp3")
            p = multiprocessing.Process(target=self.playSong, args=("TheMotans\Pe bune.mp3",))
            p.start()
            self.__musicCounter.value = 0
            self.__counter.value = 0
            self.__firstclap.value = False

    # this is the target function that we use if the client wants to go out

    def goOut(self, startTime, q: multiprocessing.Queue):
        driving_assistant = DrivingAssistant()
        resultList = []
        endTime = time.time()
        elapsedTime = endTime - startTime
        while (elapsedTime < 5):
            endTime = time.time()
            elapsedTime = endTime - startTime
            if (q.empty() is not True):
                element = q.get()
                if (element == "clap"):
                    print("He clapped")
                    self.__goOutCounter.value += 1

        if (self.__goOutCounter.value == 0):
            print("I didn't hear any clap")
        elif (self.__goOutCounter.value == 1):
            # faculty
            resultList = driving_assistant.fromHomeToFaculty()
            print(resultList)
            self.say_distance_and_time(resultList, "faculty")
            self.__goOutCounter.value = 0
            self.__counter.value = 0
            self.__firstclap.value = False
        elif (self.__goOutCounter.value == 2):
            # piata unirii
            resultList = driving_assistant.fromHomeToPU()
            print(resultList)
            self.say_distance_and_time(resultList, "pu")
            self.__goOutCounter.value = 0
            self.__counter.value = 0
            self.__firstclap.value = False
        elif (self.__goOutCounter.value == 3):
            # harmony
            resultList = driving_assistant.fromHometoHarmony()
            print(resultList)
            self.say_distance_and_time(resultList, "harmony")
            self.__goOutCounter.value = 0
            self.__counter.value = 0
            self.__firstclap.value = False
        elif (self.__goOutCounter.value == 4):
            # mitropolie
            resultList = driving_assistant.fromHomeToMitroplie()
            print(resultList)
            self.say_distance_and_time(resultList, "mitropolie")
            self.__goOutCounter.value = 0
            self.__counter.value = 0
            self.__firstclap.value = False

    def webScrapingWeather(self) -> str:
        url = "https://vremea.ido.ro/Iasi.htm"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        smth = soup.findAll('tr', {'class': "c2"})
        myelem = 0
        for elem in smth:
            myelem = elem
            break
        text = myelem.text.replace("Ț", "T").replace("ț", "t").replace("ș", "s").replace("Ș", "S").replace("ă", "a").replace("â", "a").replace("°", " grade Celsius\n").replace("²", "meters squared\n").replace("‹", "")
        return text

    def webScrapingTheNews(self):
        url = "https://www.flashscore.ro/stiri/"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        divs = soup.findAll("div", {"class": "fsNewsSection fsNewsSection__mostRead"})

        counter = 0
        lists_of_links = []
        for div in divs:
            links = div.find_all_next("a")
            for link in links:
                if(counter<=6):
                    lists_of_links.append(link['href'])
                    counter += 1
                else:
                    break
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)
        tabNumber = 0
        for link in lists_of_links:
            reallink = "https://www.flashscore.ro/" + link
            driver.execute_script("window.open('about:blank','" + 'tab' + str(tabNumber) + "');")
            driver.switch_to.window('tab' + str(tabNumber))
            driver.get(reallink)
            tabNumber+=1





    def turnTimerOn(self):
        self.start_time = time.time()

    def turnTimerOff(self):
        self.end_time = time.time()



    def getOn(self) -> bool:
        return self.on

    def getFirstClap(self) -> bool:
        return self.__firstclap

    def say_something(self, filename: str):
        playsound.playsound(self.audiosFolder + "\\" + filename)

    def say_distance_and_time(self, resultList: list[str, str, str], option):
        distance = resultList[0].replace("km", "kilometers")
        normalTime = resultList[1].replace("mins", "minutes")
        trafficTime = resultList[2].replace("mins", "minutes")

        myobj = gTTS(text=distance, lang="en", tld="us", slow=False)
        myobj.save("distance.mp3")

        myobj = gTTS(text=normalTime, lang="en", tld="us", slow=False)
        myobj.save("normalTime.mp3")

        myobj = gTTS(text=trafficTime, lang="en", tld="us", slow=False)
        myobj.save("trafficTime.mp3")

        if(option=="harmony"):
            playsound.playsound(self.audiosFolder +"\destinationsFolder\distanceToHarmony.mp3")
            playsound.playsound("distance.mp3")
            playsound.playsound(self.audiosFolder + "\destinationsFolder\\normalTimetoHarmony.mp3")
            playsound.playsound("normalTime.mp3")
            playsound.playsound(self.audiosFolder + "\destinationsFolder\\trafficTimetoHarmony.mp3")
            playsound.playsound("trafficTime.mp3")

        elif(option=="pu"):
            playsound.playsound(self.audiosFolder + "\destinationsFolder\distanceTopu.mp3")
            playsound.playsound("distance.mp3")
            playsound.playsound(self.audiosFolder + "\destinationsFolder\\normalTimetopu.mp3")
            playsound.playsound("normalTime.mp3")
            playsound.playsound(self.audiosFolder + "\destinationsFolder\\trafficTimetopu.mp3")
            playsound.playsound("trafficTime.mp3")

        elif (option == "mitropolie"):
            playsound.playsound(self.audiosFolder + "\destinationsFolder\distanceToMitr.mp3")
            playsound.playsound("distance.mp3")
            playsound.playsound(self.audiosFolder + "\destinationsFolder\\normalTimetoMitr.mp3")
            playsound.playsound("normalTime.mp3")
            playsound.playsound(self.audiosFolder + "\destinationsFolder\\trafficTimetoMitr.mp3")
            playsound.playsound("trafficTime.mp3")
        elif (option == "faculty"):
            playsound.playsound(self.audiosFolder + "\destinationsFolder\distanceTofaculty.mp3")
            playsound.playsound("distance.mp3")
            playsound.playsound(self.audiosFolder + "\destinationsFolder\\normalTimetofaculty.mp3")
            playsound.playsound("normalTime.mp3")
            playsound.playsound(self.audiosFolder + "\destinationsFolder\\trafficTimetofaculty.mp3")
            playsound.playsound("trafficTime.mp3")

        self.say_something("remember.mp3")

        os.remove("distance.mp3")
        os.remove("normalTime.mp3")
        os.remove("trafficTime.mp3")

    def playSong(self, filename: str):
        playsound.playsound(self.musicFolder + "\\" + filename)



