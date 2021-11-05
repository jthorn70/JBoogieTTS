from os import error
from requests.auth import HTTPBasicAuth
import requests
import time

from requests.models import MissingSchema
from playsound import playsound



# get request return UUID
# post request return path
    # if path null, redo post until path not null



def postThatShit(text,voice):
    # data for message and voice
    stuff = {"speech":text,"voice":voice}

    # post request 
    r = requests.post('https://api.uberduck.ai/speak', auth=('pub_exufwfdjbhgtnbkhyw', 'pk_7b34d2a8-2786-480b-beeb-3e80b599fd55'),json=stuff)
    # print("THIS: ",r.request.headers)
    print(r.status_code)
    # print(r.text)

    # storing result as text and slicing the needed part of the URL
    uuid = r.text
    sliced = uuid[9:-2]
    # print("THIS: ", sliced)

    # combining URL
    myURL = "https://api.uberduck.ai/speak-status?uuid=" + sliced
    return myURL

def getThatShit(myURL):
    p = requests.get(myURL ,auth=('pub_exufwfdjbhgtnbkhyw', 'pk_7b34d2a8-2786-480b-beeb-3e80b599fd55'))


    # print(p.text)
    # converting results to json. not sure if this is the best way or not
    results = p.json()
    # getting path of wav file (not working from cli but works if you copy paste URL)
    path = results['path']

    # print("RESULTS: ",results['finished_at'])

    if str(results['finished_at']) == "None":
        print("Not done. try agin in 5")
        time.sleep(5)
        getThatShit(myURL)
    else:
        # print("Path: ",results['path'])
        # print("URL: ",myURL)
        # print("THIS IS THE PATH IN GET: ",path)

        return path

def downloadWav(path):
    print("Starting Download")
    url = path
    r = requests.get(url)
    DLPath = '/Users/Jeremiah/OneDrive/Documents/CODE/UberduckBot/wavs/file.wav'
    print("DLPATH: ",DLPath)
    with open(str(DLPath),'wb') as f:
        f.write(r.content)

def promptUser():
    text = str(input("Please enter your desired message: "))
    voice = str(input("Please enter your desired voice: "))

    return text,voice


def readFile():
    file = open('/Users/Jeremiah/OneDrive/Documents/CODE/TheRealPythonChatBot/transcript.txt')
    line = str(file.readlines())
    return line

def main():



    text,voice = promptUser()
    # text = readFile()
    # text = "poggers omgegalul titties."
    # voice = "dababy"
    myURL = postThatShit(text,voice)


    # yo why this shit not workin
    path = getThatShit(myURL)



    # print(getThatShit(myURL))
    # print("THIS IS THE PATH IN MAIN: ",path)
    downloadWav(getThatShit(myURL))
    playsound('/Users/Jeremiah/OneDrive/Documents/CODE/UberduckBot/wavs/file.wav')




if __name__ == "__main__":
    main()