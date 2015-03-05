import json
import requests
import tweepy
import sys
import os
import locale
locale.setlocale(locale.LC_ALL, 'en_GB.utf8')

file_name = "full_status.json"

# If "full_status.json" exists as a file, read it and set the initial parameters

try:
    with open('full_status.json', 'r') as file:
        read_data = file.read()
        file.closed
        data_old = json.loads(read_data)
        state_old      = data_old['power_status']['cleaner_state']
        battery_old    = data_old['power_status']['battery_charge']
        distance_old   = int(data_old['tc_status']['cleaning_distance'])

except IOError as e:
    print "Unable to open 'full_status.json' - using default values"
    state_old      = ""
    battery_old    = ""
    distance_old   = 0


# Get the Status from the Roomba
IP_address = "192.168.0.123" # Change this!
API_url    = 'http://'+IP_address+'/full_status.json'
response   = requests.get(url=API_url)
data       = json.loads(response.text)
state      = data['power_status']['cleaner_state']
battery    = data['power_status']['battery_charge']
distance   = int(data['tc_status']['cleaning_distance'])

# Save the json to 
json_file = open(file_name, "w")
json_file.write(json.dumps(data))
json_file.close()

status_dict = {
    "st_base"         : "On homebase: Not Charging",
    "st_base_recon"   : "On homebase: Reconditioning Charging",
    "st_base_full"    : "On homebase: Full Charging",
    "st_base_trickle" : "On homebase: Trickle Charging",
    "st_base_wait:"   : "On homebase: Waiting",
    "st_plug"         : "Plugged in: Not Charging",
    "st_plug_recon"   : "Plugged in: Reconditioning Charging",
    "st_plug_full"    : "Plugged in: Full Charging",
    "st_plug_trickle" : "Plugged in: Trickle Charging",
    "st_plug_wait"    : "Plugged in: Waiting",
    "st_stopped"      : "Stopped",
    "st_clean"        : "Cleaning",
    "st_cleanstop"    : "Stopped with cleaning",
    "st_clean_spot"   : "Spot cleaning",
    "st_clean_max"    : "Max cleaning",
    "st_delayed"      : "Delayed cleaning will start soon",
    "st_dock"         : "Searching Homebase",
    "st_pickup"       : "Roomba picked up",
    "st_remote"       : "Remote control driving",
    "st_wait"         : "Waiting for command",
    "st_off"          : "Off",
    "st_error"        : "Error",
    "st_locate"       : "Find me!",
    "st_unknown"      : "Unknown state"
}

# Has there been a change of state?
if state != state_old :
    # Calculate the distance travelled since the change of state
    distance_new = distance - distance_old
  
    # Set the Tweet text
    tweet = "Status - "   + status_dict[str(state)] + \
            "\n" + \
            "I've moved " + locale.format("%d", distance_new, grouping=True) + " metres (" + locale.format("%d", distance, grouping=True) + " metres in total)" + \
            "\n" + \
            "Battery "    + str(battery) + "%"
  
    # Consumer keys and access tokens, used for OAuth
    consumer_key        = 'aaaaaaaaaaa'
    consumer_secret     = 'bbbbbbbbbbb'
    access_token        = 'ccccccccccc'
    access_token_secret = 'ddddddddddd'

    # OAuth process, using the keys and tokens
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Set Up Twitter
    api = tweepy.API(auth)

    # Send the Tweet
    api.update_status(status=tweet)
    #print tweet
else :
    # Nothing else to do
    sys.exit()
