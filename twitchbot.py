import random
import time
from twitchio.ext import commands
from better_profanity import profanity
import simpleaudio as sa
from pynput import keyboard
from requests.auth import HTTPBasicAuth
import requests
import Bans
import Fact
import RemoveBlank

RemoveBlank.remove_empty_lines('bans.txt')
RemoveBlank.remove_empty_lines('facts.txt')
profanity.load_censor_words_from_file('SwearWords.txt')
MODS=['jboondock','n0talecks','skatehead','jbooogie','contraaa_']
vibes = ["a shitty vibe WEIRD","an insanely chill vibe peepoHappy","whoah.... his vibe levels are off the charts monkaW","Guy Fieri Vibes DxCat","no vibes monkaW","mongo pushing vibes DansGame","DawgVinci Vibes Kreygasm","Dennis Quaid type vibes DxCat","one singular vibe monkaS",'Default Gravity Vibes','Resin hit vibes','vibe like an onlyFans account Kappa']
boonVibes = ["INSANELY GOD LIKE VIBES", "DEV LIKE VIBES","8K Vibes Pog","BETTER VIBES THAN ANYONE ON THE PLANET",'H-H-H-HOLY FUCK THESE VIBES JUST MELTED THE BOT.... RESTARTING']


def on_press(key):
    key
    # try:
    #     print('alphanumeric key {0} pressed'.format(
    #         key.char))
    # except AttributeError:
    #     print('special key {0} pressed'.format(
    #         key))

def on_release(key):
    # print('{0} released'.format(
    #     key))
    if key == keyboard.Key.esc:
        sa.stop_all()
        return True

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


def postThatShit(text,voice):
    # data for message and voice
    stuff = {"speech":text,"voice":voice}

    # post request 
    r = requests.post('https://api.uberduck.ai/speak', auth=(' key goes here', 'secret goes here'),json=stuff)
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
    p = requests.get(myURL ,auth=('key goes here', 'secret goes here'))


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
        print("Path: ",results['path'])
        print("URL: ",myURL)
        # print("THIS IS THE PATH IN GET: ",path)

        return path

def downloadWav(path):
    print("Starting Download")
    r = requests.get(path)
    DLPath = '/Users/Jeremiah/OneDrive/Documents/CODE/UberduckBot/wavs/file.wav'
    print("DLPATH: ",DLPath)
    with open(str(DLPath),'wb') as f:
        f.write(r.content)








class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token='access token goes here', prefix='!', initial_channels=['jboondock'])

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    # async def event_message(self, message):
    #     print(message.content)

    @commands.command(name='trick')
    async def trick(self, ctx: commands.Context):
        trickRequest = str(ctx.message.content)[6:]
        insults = ["This little bitch named ","hey boogie, ", "ay bud, ", "oi bruvvah, ", "jboogie? are you there? eh. i dont care.", "Hey put down the drink, ", "wow. really? ","oh man. what a good one. i cant believe that ","oh no.","This guy again? really bro?","uh oh. stinky!","HEY FUCKO,","behold. the dumbest trick. "]
        suffix = ["What a cuckold.", "that's probably gonna suck.", "even i could do that one.", "can't these people come up with anything better?", "try not to break your controller this time. kappa.", "man, thats kinda cringe.","what the actual fuck.","wow okay. jesus.","uh oh. stinky!","whatever, its the cringe pilled boomer energy for me.","sub with twitch prime.","dans game. so gross."]
        randInsult = random.choice(insults)
        randSuffix = random.choice(suffix)
        message = randInsult + ctx.author.name +", requested" + trickRequest + ". " + randSuffix
        currentTrick = "Current Trick: " + trickRequest + ", Requested by " + ctx.author.name
        if (ctx.author.name.lower() in Bans.banList):
            await ctx.channel.send("ACCESS DENIED")
            message=""

        if (ctx.author.name.lower not in Bans.banList):
            

            if (len(ctx.message.content)>200):
                await ctx.channel.send("Message too long jabroni")
                message = "Message too long jabroni."
                currentTrick = ""
                

            if (profanity.contains_profanity(ctx.message.content)):
                censored = profanity.censor(trickRequest,'za')
                message = randInsult + ctx.author.name +", requested" + censored + ". " + randSuffix
                await ctx.channel.send(ctx.author.name + ", thank you for your request")
                # print(ctx)
                j = open("transcript.txt","w")
                j.write(message)
                j.close()
            else:
                myURL = postThatShit(message,'boogie')
                print('URL: ',myURL)
                time.sleep(10)
                if "https" not in str(getThatShit(myURL)):
                    time.sleep(5)
                    newURL = (getThatShit(myURL))
                    downloadWav(newURL)
                downloadWav(getThatShit(myURL))
                wave_obj = sa.WaveObject.from_wave_file("/Users/Jeremiah/OneDrive/Documents/CODE/UberduckBot/wavs/file.wav")
                play_obj = wave_obj.play()
                play_obj.wait_done()
                # playsound('/Users/Jeremiah/OneDrive/Documents/CODE/UberduckBot/wavs/file.wav')
                
                # print(ctx)
                f = open("trick.txt","w")
                f.write(currentTrick)
                f.close()

                j = open("transcript.txt","w")
                j.write(message)
                j.close()


                # await ctx.send(f'{message}')
                
                await ctx.channel.send(ctx.author.name + ", thank you for your request")
        else:
            await ctx.channel.send(ctx.author.name + ": ACCESS DENIED")


    @commands.command(name='size')
    async def size(self, ctx: commands.Context):
        longth = random.randint(1,12)
        thickness = random.randint(1,5)
        curve = random.randint(0,30)
        
        if (longth == 0 and thickness == 0):
            await ctx.channel.send(ctx.author.name + " is cockless LUL")
        elif(longth < 5):
            await ctx.channel.send(ctx.author.name + " is about " +str(thickness)+ " inches thicc, and "+ str(longth)+ " inches wide. With a curve of " + str(curve) + " degrees." )
        elif(longth==thickness):
            await ctx.channel.send(ctx.author.name + " is about " +str(thickness)+ " inches thicc, and "+ str(longth)+ " inches wide.With a curve of " + str(curve) + " degrees." + " SQUARE COCK GANG ")
        else:
            await ctx.channel.send(ctx.author.name + " is about " +str(thickness)+ " inches thicc, and "+ str(longth)+ " inches wide.With a curve of " + str(curve) + " degrees.")
    
    @commands.command(name='vibecheck')
    async def newvibe(self, ctx: commands.Context):
        randVibe = random.choice(vibes)
        randBoon = random.choice(boonVibes)
        vibeTarget = str(ctx.message.content)[10:]

        if (vibeTarget == ""):
            vibeTarget = ctx.author.name

        if (ctx.author.name == "jboondock" or ctx.author.name == "jbooogie"):
            await ctx.channel.send(vibeTarget +" has "+ randBoon)
        else:
            await ctx.channel.send(vibeTarget +" has "+ randVibe)


    @commands.command(name='loadfacts')
    async def loadfacts(self, ctx: commands.Context):
        if(ctx.author.name in MODS):
            Fact.loadFacts()
            await ctx.channel.send("Facts Loaded!")

    @commands.command(name='addfact')
    async def addfact(self, ctx: commands.Context):
        fact=str(ctx.message.content)[9:]
        if(ctx.author.name in MODS):
            Fact.addFact(fact)
        # await ctx.channel.send(fact+" added to list")

    @commands.command(name='remfact')
    async def remfact(self, ctx: commands.Context):
        fact=str(ctx.message.content)[9:]
        if(ctx.author.name in MODS):
            Fact.removeFact(fact)
            Fact.saveFacts()
        # await ctx.channel.send(fact+" removed from list")



    @commands.command(name='loadbans')
    async def loadbans(self, ctx: commands.Context):
        if(ctx.author.name in MODS):
            Bans.loadBans()
            await ctx.channel.send("Bans Loaded!")


    @commands.command(name='addban')
    async def addban(self, ctx: commands.Context):
        name=str(ctx.message.content)[8:]
        if(ctx.author.name in MODS):
            Bans.addBan(name)
            Bans.saveBans()
        # await ctx.channel.send(name+" added to list")

    @commands.command(name='remban')
    async def remban(self, ctx: commands.Context):
        name=str(ctx.message.content)[8:]
        if(ctx.author.name.lower() in MODS):
            Bans.removeBan(name)
            Bans.saveBans()
        # await ctx.channel.send(name+" removed from list")

    @commands.command(name='bans')
    async def bans(self, ctx: commands.Context):
        if(ctx.author.name in MODS):
            await ctx.channel.send(Bans.banList)


    @commands.command(name='randfact')
    async def randfact(self, ctx: commands.Context):
        randFact = random.choice(Fact.facts)
        await ctx.channel.send(randFact)

    @commands.command(name='TTS')
    async def TTS(self, ctx: commands.Context):
        await ctx.channel.send("Created by JBoondock, Github repository: https://github.com/jthorn70/JBoogieTTS, Donate: https://paypal.me/jboondock?country.x=US&locale.x=en_US" )

bot = Bot()
bot.run()