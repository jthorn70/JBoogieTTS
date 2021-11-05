from requests.auth import HTTPBasicAuth
import requests

# data for message and voice
stuff = {"speech":"alex likes weiners","voice":"chills"}

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

# get request for new URL
p = requests.get(myURL ,auth=('pub_exufwfdjbhgtnbkhyw', 'pk_7b34d2a8-2786-480b-beeb-3e80b599fd55'))


# print(p.text)
# converting results to json. not sure if this is the best way or not
results = p.json()
# getting path of wav file (not working from cli but works if you copy paste URL)
print(results['path'])
print(myURL)



