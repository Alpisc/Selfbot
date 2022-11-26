import json
from os.path import exists

print("Welcome to the installation wizard, please fill out all of the fields to set up the selfbot")

token = input("Your discord token:\n").strip('"')

prefix = ""
while prefix == "":
    prefix = input("What prefix do you want to use:\n").strip('"')

status = input("Which discord status do you want (Online/Idle/Dnd/Invisible/Offline):\n").lower().strip('"')

tenorapikey = input("Enter your Tenor API key: (not needed)\n").strip('"')

galaxy = input("Do you want to enable a galaxy console ascii art (y/N):\n").lower().strip('"')

animegirl = input("Do you want to enable a animegirl console ascii art (y/N):\n").lower().strip('"')

animegirl2 = input("Do you want to enable a animegirl2 console ascii art (y/N):\n").lower().strip('"')

if tenorapikey != "":
    tenorpos = input("Do you want to use a tenor api pos argument? (leave blank if you dont know what this is):\n")

if(status not in ["online","idle","dnd","do not disturb", "invisible", "offline"]):
    print("Invalid status detected, please either run the setup again or change it in the config file")

galaxy = galaxy == "y"

animegirl = animegirl == "y"

animegirl2 = animegirl2 == "y"

if exists("template_config.json"):
    with open('template_config.json', 'r') as openfile:
        old_dict = json.load(openfile)
else:
    old_dict = {
    "TOKEN": "YOUR-TOKEN",
    "PREFIX": "YOUR-PREFIX",
    "GALAXY": False,
    "STATUS": "YOUR-DISCORD-PRESENCE",
    "TENORAPIKEY": "YOUR-TENOR-KEY",
    "ANIMEGIRL": False,
    "ANIMEGIRL2": False,
    "FUSIONANIMEGIRL": False,
    "TENORPOS": ""
}

old_dict["TOKEN"] = token
old_dict["PREFIX"] = prefix
old_dict["STATUS"] = status
old_dict["TENORAPIKEY"] = tenorapikey
old_dict["GALAXY"] = galaxy
old_dict["ANIMEGIRL"] = animegirl
old_dict["ANIMEGIRL2"] = animegirl2
old_dict["TENORPOS"] = tenorpos

json_object = json.dumps(old_dict, indent=4)

with open("config.json", "w") as outfile:
    outfile.write(json_object)
