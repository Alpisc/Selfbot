import discord
from discord.ext import commands
import asyncio
import os
import json
import random
import requests
import aiohttp
from colorama import Fore
import sys
import git
import datetime
import shutil
import typing
from urllib.request import urlopen, Request

def reloadConfig():
    global config, TOKEN, PREFIX, GALAXY, ANIMEGIRL, ANIMEGIRL2, STATUS, TENORAPIKEY, TENORPOS
    try:
        config = json.load(open(".content/config.json"))
        TOKEN =  config["TOKEN"]
        PREFIX = config['PREFIX']
        GALAXY = config['GALAXY']
        ANIMEGIRL = config['ANIMEGIRL']
        ANIMEGIRL2 = config['ANIMEGIRL2']
        STATUS = config['STATUS']
        TENORAPIKEY = config['TENORAPIKEY']
        TENORPOS = config["TENORPOS"]
    except Exception:
        print("Your config file is corrupted, please either run the setup wizard or fill out empty fields by your self.\n")
        flush_config = input("Do you want to reset your config.json file? (y/N):\n")
        if(flush_config.lower() in ["y","ye","yes"]):
            if os.path.exists(".content/template_config.json"):
                with open('.content/template_config.json', 'r') as openfile:
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
            json_object = json.dumps(old_dict, indent=4)

            with open(".content/config.json", "w") as outfile:
                outfile.write(json_object)

            print("Your config has been flushed!\nPlease go ahead by yourself now!")
            sys.exit()
        reloadConfig()

reloadConfig()

client = commands.Bot(command_prefix=PREFIX, self_bot=True)

start_time = datetime.datetime.now()

TENORPOS = "" # needed for random tenor gifs

def CreateStartScreen():
    os.system("cls" if os.name == "nt" else "clear")
    startscreen = ""

    if GALAXY:
        startscreen += f"""{Fore.MAGENTA}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⡴⠶⠞⠛⠛⠉⠉⠉⠉⠉⠉⠛⠛⠶⢦⣄⡀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣶⣾⠿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠈⠛⢦⡀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⢛⣩⠶⠛⠉⠀⠀⠀⣀⣤⡴⠶⠚⠛⠛⠛⠉⠛⠛⠛⢶⡟⠉⢻⡄⠀⠀⠀⠈⢻⡄
    ⠀⠀⠀⠀⠀⠀⠀⣠⡴⠟⢉⣠⠶⠋⠁⠀⠀⣠⡴⠞⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠷⡤⠾⣇⠀⠀⠀⠀⠀⣿
    ⠀⠀⠀⠀⣠⡴⠛⠁⣀⡴⠛⠁⠀⢀⣠⠶⠛⠁⠀⠀⠀⣀⣠⡤⠶⠒⠛⠛⠛⠛⠛⠶⣤⡀⠀⠀⠀⢹⡆⠀⠀⠀⠀⢸
    ⠀⢀⣴⠟⠁⠀⣠⡾⠋⠀⠀⢀⡴⠛⠁⠀⢰⠞⠳⡶⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⢈⡇⠀⠀⠀⠀⣾
    ⢴⠟⠁⠀⢀⡼⠋⠀⠀⢀⡴⠋⠀⠀⠀⣠⡾⠷⠶⠇⢀⣠⣤⠶⠖⠲⢶⣄⠀⠀⠀⠀⠀⡿⠀⠀⠀⢸⡇⠀⠀⠀⢰⡏
    ⠀⠀⠀⣰⠟⠀⠀⠀⣴⠏⠀⠀⠀⣠⠞⠉⠀⠀⣠⡶⠋⠁⠀⠀⠀⠀⢀⡿⠀⠀⠀⠀⣼⠃⠀⠀⢀⡟⠂⠀⠀⢠⡟⠀
    ⠀⢀⣼⠋⠀⠀⢀⡾⠁⠀⠀⢠⡞⠁⠀⠀⢠⡾⠁⠀⠀⠀⠀⣀⣀⣠⡾⠁⠀⠀⣠⡾⠁⠀⠀⢠⡞⠁⠀⠀⣰⠟⠀⠀
    ⠀⣾⠃⠀⢠⡟⠛⣷⠂⠀⢠⡟⠀⠀⠀⠀⢾⡀⠀⠀⠀⠀⣸⣏⣹⡏⠀⠀⣠⡾⠋⠀⠀⢀⣴⠏⠀⠀⢀⡼⠋⠀⠀⠀
    ⣸⠇⠀⠀⠈⢻⡶⠛⠀⠀⣿⠀⠀⠀⠀⠀⠈⠛⠲⠖⠚⠋⠉⠉⠉⣀⣤⠞⠋⠀⠀⢀⣴⠟⠁⠀⠀⣰⠟⠁⠀⣴⠆⠀
    ⣿⠀⠀⠀⠀⢸⡇⠀⠀⠀⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠶⠛⠉⣀⣀⡀⣀⡴⠟⠁⠀⢀⣤⠞⠁⢀⣴⠟⠁⠀⠀
    ⣿⠀⠀⠀⠀⠘⣧⠀⠀⠀⠀⠙⠳⠶⠤⣤⠤⠶⠶⠚⠋⠉⠀⠀⠀⡟⠉⠈⢻⡏⠀⠀⣀⡴⠛⠁⣠⡶⠋⠁⠀⠀⠀⠀
    ⢻⡀⠀⠀⠀⠀⠘⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⠶⠻⢦⣤⠟⣀⣤⠞⢋⣠⡴⠛⠁⠀⠀⠀⠀⠀⠀⠀
    ⠈⢿⣄⠀⠀⠀⠀⠀⠈⠛⠳⠶⠤⠤⠤⠤⠤⠴⠶⠒⠛⠉⠁⠀⠀⢀⣠⡴⣞⣋⣤⠶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠙⢷⡶⠛⠳⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣤⣴⣾⠿⠿⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠘⣧⡀⣀⣿⠦⣤⣤⣤⣤⣤⣤⠤⠶⠶⠞⠛⠋⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠈⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⡀⠀⠀⠀⡀⠀⠀⡀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⢀⠀⢀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠞⠛⠿⠟⢛⠛⠿⠻⠛⠐⠟⠟⠛⠂⠀⠈⠈⠃⠄⠈⠓⠚⠛⠚⠓⠓⠟⠀⠀⠀⠀⠀⠀⠀{Fore.RESET}\n"""
    if ANIMEGIRL:
        startscreen += """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠻⢷⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣄⣠⡤⠒⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢾⣤⣤⣤⣴⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣯⣿⣿⣿⣭⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀
    ⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⢿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀
    ⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⣿⣿⣿⣿⣿⣿⣿⠹⣿⣿⣿⣿⣿⣿⠟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠻⠆⠀⠀
    ⠀⠰⠿⠿⠿⣿⣿⣿⣿⣿⣿⡿⠀⢠⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿⠀⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀
    ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⠑⠊⠙⣿⣿⣿⠿⠿⠿⠛⠃⠙⠛⣛⣿⣿⣿⣄⡸⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
    ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡧⣴⡾⠿⠛⠛⠉⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠛⠿⢿⣻⠶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀
    ⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⡅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀
    ⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡿⠋⠉⠉⠻⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
    ⠀⠀⠀⠀⠀⠈⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣷⢾⣍⠙⠆⢸⣿⣿⣿⣿⣿⣿⣿⡆⠀
    ⠐⠀⠴⠀⠀⠀⢹⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠈⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡧⠴⠋⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀
    ⠀⠀⠦⠄⠀⠀⠀⠹⣿⣿⠿⣧⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⣿⣿⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀
    ⠀⠀⠀⠀⠀⣀⣀⠀⢀⣿⣿⣿⣿⣿⣶⣦⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⢀⣤⣴⣾⣿⣿⣿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄
    ⠀⠀⠀⠀⠀⢿⣽⠧⠾⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡄⠀⠀⠀⢸⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
    ⠀⠀⠀⠀⠀⠀⠁⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⢻⣿⠿⠛⠉⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣾⣿⣿⣿⣿⣿⠃
    ⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⠟⠁⠀⣀⣤⠴⠛⠉⠀⠀⠀⠀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠟⠋⣀⣾⣋⣤⡤⠖⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⡇⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡿⠛⠁⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⣿⡏⢸⣿⡿⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠘⢿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢻⡉⠉⠉⠉⠀⠈⠉⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠀⠀⢰⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀\n"""
    if ANIMEGIRL2:
        startscreen += """
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⠛⠛⠛⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡀⢙⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⠹⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⢓⠻⡟⡟⠀⢻⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⡟⠀⠀⠄⠀⠀⠀⠀⠀⢇⠀⠀⡄⠸⣦⠬⡄⠀⢡⠀⠈⡌⢿⣿⣿⣿
    ⣿⣿⣿⣿⡣⠀⢰⠠⠀⢀⠘⡀⠄⡏⢶⡄⢰⡠⠼⣆⣐⡄⠈⡤⠀⣅⠈⣿⣿⣿
    ⣿⣿⣿⡿⡇⠀⠸⡆⠀⢸⠊⣧⣒⣇⠈⢿⢌⡝⢻⣿⣿⡏⠀⡇⢈⡇⠀⢻⣿⣿
    ⣿⣿⣿⡇⢹⡄⠀⣷⠀⠀⣾⠛⣿⣿⡆⠈⠀⠀⢰⣿⢛⣼⠀⢡⣾⡇⠀⢸⣿⣿
    ⣿⣿⣿⠀⠀⣷⡂⠸⡀⠀⢸⣠⣌⣿⡇⠀⠀⠀⠀⠀⠁⣸⠀⠘⣿⡇⠀⢸⣿⣿
    ⣿⣿⣿⠀⠀⢿⣿⣦⡇⠀⠸⣏⠋⠉⠀⠀⠈⠁⢀⣠⣾⣿⡄⡀⣿⡇⠀⠈⣿⣿
    ⣿⣿⣿⠀⠀⢸⣿⣿⣷⢠⠀⣿⣿⣶⣶⣶⡶⠟⠋⠘⡻⣿⣷⣳⣿⡄⠀⠀⣿⣿
    ⣿⣿⣿⠀⠀⠀⣿⣿⣿⡌⡆⢿⣿⣿⣽⣾⠀⠀⠀⣰⣿⣷⣾⣯⣿⡃⠀⠀⢻⣿
    ⣿⣿⡏⠀⠀⠀⢹⣿⣿⣷⣸⣼⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣷⡇⠀⠀⢸⣿
    ⣿⣿⡇⡄⠀⠀⢸⣿⣿⣽⣿⣿⣏⠻⣿⣿⣿⠿⠛⠉⣉⣰⣿⣿⣿⣧⠀⠀⢸⣿\n"""
    startscreen += f"Bot started\nWelcome back {client.user.name}\nYour Prefix is: {PREFIX}\nYour Status is: {''.join(str(x + ' ') for x in [word.capitalize() for word in STATUS.split(' ')])}\n"
    print(startscreen)

errorvar = "No errors yet :D"

@client.event
async def on_command_error(event, *args):
    global errorvar
    errorvar = args
    a = await event.send(content=f"View error with {PREFIX}showerror")
    await asyncio.sleep(2)
    await a.delete()


async def setStatus(STATUS):
    if STATUS.upper() == "ONLINE":
        await client.change_presence(status=discord.Status.online)
        STATUS = "online"
    elif(STATUS.upper() == "DND" or STATUS.upper() == "DO NOT DISTURB"):
        await client.change_presence(status=discord.Status.dnd)
        STATUS = "do not disturb"
    elif STATUS.upper() == "IDLE":
        await client.change_presence(status=discord.Status.idle)
        STATUS = "idle"
    elif STATUS.upper() == "INVISIBLE":
        await client.change_presence(status=discord.Status.invisible)
        STATUS = "invisible"
    if(STATUS != config["STATUS"] and STATUS in ["online", "do not disturb", "idle", "invisible"]):
        config["STATUS"] = STATUS

        json_object = json.dumps(config, indent=4)

        with open(".content/config.json", "w") as outfile:
            outfile.write(json_object)

        reloadConfig()

# os.system("cls" if os.name == "nt" else "clear")
print("Starting up, this might take a few seconds...")
@client.event
async def on_connect():
    CreateStartScreen()
    await setStatus(STATUS)

afkstatus = False
afkmessage = ""

@client.event
async def on_message(message):
    ctx = await client.get_context(message)
    if ctx.message.author != client.user:
        if (
            isinstance(ctx.channel, discord.channel.DMChannel)
            and afkstatus
        ):
            await ctx.send(afkmessage)
    else:
        if message.content.startswith(PREFIX):
            await ctx.message.delete()
            await client.process_commands(message)

snipes = {}

def snipe_filter(message):
    if message.author == client.user:
        if message.content == "https://tenor.com/view/thumbs-up-chew-eating-chika-fujiwara-kaguya-sama-gif-17941452":
            return False
        if message.content == "i finished master UwU":
            return False
        if message.content == "no more messages to be sniped":
            return False
        #could make this better but it's easier to read like this atm

    return True

@client.event
async def on_message_delete(message):
    global snipes, snipe_filter
    if message.channel.id not in snipes:
        snipes[message.channel.id] = []
    if((message.author != client.user or (not message.content.startswith(PREFIX))) and snipe_filter(message)): #thanks for making commands auto delete ╰（‵□′）╯
        snipes[message.channel.id].append(message)

@client.command()
async def snipe(ctx, count: typing.Optional[int]=1):
    """Shows you the most recently deleted message"""
    global snipes

    message = ""

    for i in range(count):
        if ctx.message.channel.id not in snipes:
            message += "no message to be sniped\n"
        else:
            try:
                sniped = snipes[ctx.message.channel.id].pop()
                message += f"""> {sniped.content}\nBy {sniped.author.mention}\n\n"""
            except:
                message += "no more messages to be sniped\n"
                break
    await ctx.send(message)

@client.command()
async def delete(ctx, amount: int):
    """deletes a given amount of messages from user"""
    original_amount = amount

    async for mss in ctx.channel.history(limit=amount +1): #get to delete amount
        if not mss.author == client.user:
            amount += 1

    async for mss in ctx.channel.history(limit=amount+1): #get to delete amount
        if mss.author == client.user:
            await mss.delete()

    print(f"Deleted {original_amount} messages")

    a = await ctx.send("i finished master UwU")
    b = await ctx.send("https://tenor.com/view/thumbs-up-chew-eating-chika-fujiwara-kaguya-sama-gif-17941452")
    await asyncio.sleep(5)
    await a.delete()
    await b.delete()

@client.command(aliases=["av"])
async def profile(ctx, member: discord.Member = None):
    """send a URL to a given users profile image"""
    if not member:
        member = ctx.author

    if member.is_avatar_animated():
        ending = "gif"
    else:
        ending = "jpg"

    filename = f"avatar1.{ending}"
    await member.avatar_url.save(filename)
    file = discord.File(fp=filename)
    await ctx.send(file=file)
    os.remove(filename)

    #await ctx.send(member.avatar_url)

@client.command()
async def ping(ctx):
    """shows latency"""
    await ctx.send(f"pong 🏓 latency: {round(client.latency * 1000)}ms")


@client.command(aliases=["aq"])
async def animequote(ctx):
  """shows a random anime quote"""
  r = requests.get("https://animechan.vercel.app/api/random")
  await ctx.send(f"{r.json()['character']} from \"{r.json()['anime']}\" once said:\n`{r.json()['quote']}`")

@client.command()
async def banner(ctx, user: discord.User):
    """shows the banner of a user"""
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"
    else:
        banner_url = "This user does not have a custom banner"
    await ctx.send(banner_url)

@client.command(aliases=["fl"])
async def friendslist(ctx):
    """sends a list with all friends of the user"""
    friends = f"I got {len(client.user.friends)} friends:\n```"
    for user in client.user.friends:
        friends += f"{user.name}#{user.discriminator}\n"
    friends += "\n```"
    await ctx.send(friends)

@client.command()
async def nuke(ctx):
    """deletes all channels & categories in the selected server"""
    if not ctx.message.author.guild_permissions.manage_channels:
        print("You dont have the permission to do that!")
        return
    channels = ctx.guild.channels
    chanam = len(ctx.guild.channels)
    for channel in channels:
        await channel.delete()
    chanam2 = len(ctx.guild.channels)

    await ctx.guild.create_text_channel(name="done")

    print(f"Done, deleted {chanam-chanam2} channels")

@client.command()
async def playing(ctx, *, text: str):
    """sets your presence as the text you entered"""
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=text))

@client.command()
async def watching(ctx, *, text: str):
    """sets your presence as the text you entered"""
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=text))

@client.command()
async def listening(ctx, *, text: str):
    """sets your presence as the text you entered"""
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=text))

@client.command()
async def statusnormal(ctx):
    """changes your status back to normal"""
    await client.change_presence(activity=None)

@client.command()
async def msgfriends(ctx, *, text: str):
    """sends the text to all of your friends"""
    for user in client.user.friends:
        await client.get_user(int(user.id)).send(text)

@client.command()
async def blockuser(ctx, user: discord.User):
    """blocks the user you mentioned"""
    await user.block()

@client.command()
async def clearblockeds(ctx):
    """unblocks everyone you have blocked"""
    blockedlen = len(client.user.blocked)
    for user in client.user.blocked:
        await user.unblock()
    print(f"Unblocked {blockedlen-len(client.user.blocked)} users")

@client.command()
async def addemoji(ctx, emoji_name, emoji_url=None):
    """adds given emoji to the guild"""
    if ctx.message.attachments:
        image = await ctx.message.attachments[0].read()
    elif emoji_url:
        async with aiohttp.ClientSession() as session, session.get(emoji_url) as resp:
            image = await resp.read()
    emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=image)
    await ctx.send(f"Emoji {emoji.name} created!")

@client.command()
async def deletefriends(ctx):
    """removes everyone in your friends list"""
    friendlen = len(client.user.friends)
    for user in client.user.friends:
        await user.remove_friend()
    print(f"Removed {friendlen-len(client.user.friends)} friends")

@client.command()
async def leaveservers(ctx):
    """leaves all servers that you are not the owner of"""
    guilds = 0
    for guild in client.guilds:
        if not guild.owner == ctx.message.author:
            await guild.leave()
            guilds += 1
    print(f"Left {guilds} guilds")

@client.command()
async def nitrogen(ctx):
    """generates a fake nitro for troll 😍"""
    await ctx.send("https://discord.gift/" + ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for i in range(16)))

@client.command()
async def createchannel(ctx, amount: int):
    """creates amount channel with ✰ in their name"""
    guild = ctx.guild
    for i in range(amount):
        star = "✰"
        for j in range(1,10000):
            if(i < amount-j and i >= j):
                star += "✰"
            else:
                break
        await guild.create_text_channel(name=star)
    print(f"Done, created {amount} channel")

@client.command(aliases=["lag"])
async def leaveallgroups(ctx):
    """leaves all groups"""
    amount = 0
    for guild in client.private_channels:
        if guild.type == discord.ChannelType.group:
            amount += 1
            await guild.leave()
    print(f"Left {amount} Groups")

@client.command(aliases=["cf"])
async def coinflip(ctx):
    """flips either head or tails"""
    a = await ctx.send("https://c.tenor.com/tewn7lzVDgcAAAAM/coin-flip-flip.gif")
    await asyncio.sleep(3)
    choices = [
        "https://cdn.discordapp.com/attachments/973679382650581102/1007593939299221564/unknown.png?size=4096",
        "https://cdn.discordapp.com/attachments/973679382650581102/1007593981267427328/unknown.png?size=4096"
    ]
    await a.edit(content=f'{random.choice(choices)}')
    await asyncio.sleep(3)
    await a.delete()

@client.command()
async def uptime(ctx):
    """shows how long the bot is running"""
    time_now = datetime.datetime.now()
    await ctx.send(f'My uptme is {time_now - start_time}')

@client.command(aliases=["reboot"])
async def restart(ctx):
    """reboots the bot and fetches the newest updates"""
    g = git.cmd.Git(os.getcwd().replace('\\', '/'))
    g.pull()
    os.execv(sys.executable, ["python"] + sys.argv)

@client.command()
async def clearconsole(ctx):
    """clears the console"""
    CreateStartScreen()

@client.command()
async def showerror(ctx):
    """displays the latest error from the console"""
    await ctx.send(errorvar)

@client.command()
async def copyusrav(ctx, userid: int):
    """steals the profile image of given id"""
    member = client.get_user(int(userid))

    if member.is_avatar_animated():
        ending = "gif"
    else:
        ending = "jpg"

    filename = f"avatar1.{ending}"
    await member.avatar_url.save(filename)

    with open(filename, 'rb') as image:
        await client.user.edit(avatar=image.read())

    print("set profile picture from "+ member.name)
    os.remove(filename)

@client.command()
async def changeav(ctx, url: str):
    """changes your profile to the image from url"""
    res = requests.get(url, stream = True)

    if res.status_code == 200:
        if url.endswith(".gif"):
            ending = "gif"
        else:
            ending = "png"

        filename = f"avatar.{ending}"

        with open(filename,'wb') as f:
            shutil.copyfileobj(res.raw, f)

        with open(filename, 'rb') as image:
            await client.user.edit(avatar=image.read())

        os.remove(filename)
        print("set new profile picture")

    else:
        print('Image Couldn\'t be retrieved')

@client.command()
async def pip(ctx, package_name: str):
    """installs python packages (this can be dangerous)"""
    os.system(f"pip install {package_name}")
    print(f"Package {package_name} installed")

@client.command()
async def afkdm(ctx, *, msg: typing.Optional[str] = afkmessage): #pwz cant remember syntax
    """set your afk status and automatically send others a message"""
    global afkmessage, afkstatus
    afkstatus = not afkstatus
    afkmessage = msg
    print("You are not currently AFK" if not afkstatus else f"Your afk message will be \"{afkmessage}\"")

@client.command()
async def stealbanner(ctx, user: discord.User): # banner stuff is not documentated
    """steals a users banner"""
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}?size=1024"

        req = Request(banner_url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64")
        ending =  urlopen(req).info()['Content-Type'].split('/')[1]

        res = requests.get(banner_url, stream = True)

        if res.status_code == 200:

            filename = f"banner.{ending}"

            with open(filename,'wb') as f:
                shutil.copyfileobj(res.raw, f)

            with open(filename, 'rb') as image:
                await client.user.edit(banner=image.read())

            os.remove(filename)

    else:
        print("User does not have a custom banner")
        return

@client.command()
async def savebanner(ctx, userid: int):
    """saves the given users banner to fokder ./banner"""
    req = await client.http.request(discord.http.Route("GET", "/users/{uid}", uid=userid))
    banner_id = req["banner"]
    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{userid}/{banner_id}?size=1024"

        res = requests.get(banner_url, stream = True)

        if res.status_code == 200:
            req = Request(banner_url)
            req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; Win64; x64")
            ending =  urlopen(req).info()['Content-Type'].split('/')[1]

            if not os.path.exists("./banner"):
                os.makedirs("banner")
            num = len([name for name in os.listdir('./banner') if os.path.isfile(os.path.join("./banner", name))])

            filename = f"banner/banner{num}.{ending}"

            with open(filename,'wb') as f:
                shutil.copyfileobj(res.raw, f)

            a = await ctx.send("Saved banner")
            await a.delete()
    else:
        a = await ctx.send("User has no custom banner")
        await a.delete()


@client.command()
async def savepfp(ctx, userid: int):
    """saves the given users profile image to folder ./pfps"""
    member = client.get_user(userid)
    if not member:
        member = ctx.author

    if member.is_avatar_animated():
        ending = "gif"
    else:
        ending = "jpg"

    if not os.path.exists("./pfps"):
        os.makedirs("pfps")
    num = len([name for name in os.listdir('./pfps') if os.path.isfile(os.path.join("./pfps", name))])

    filename = f"pfps/avatar{num}.{ending}"
    await member.avatar_url.save(filename)
    a = await ctx.send("Saved image")
    await a.delete()


@client.command()
async def gitstash(ctx):
    """stashes your current version (might help if you cant update)"""
    os.chdir(os.getcwd().replace('\\', '/'))
    os.system("git stash")

@client.command()
async def animegifpfpgen(ctx):
    """takes a random anime gif from tenor and sets it as profile image"""
    # https://tenor.com/developer/dashboard
    r = requests.get("https://tenor.googleapis.com/v2/search?q=anime&key=%s&random=true&limit=1&pos=%s" % (TENORAPIKEY, TENORPOS), stream=True)

    if r.status_code == 200:
        result = json.loads(r.content)

        config["TENORPOS"] = result['next']

        json_object = json.dumps(config, indent=4)

        with open(".content/config.json", "w") as outfile:
            outfile.write(json_object)

        reloadConfig()

        filename = "tmpav.gif"
        r2 = requests.get(result["results"][0]["media_formats"]["gif"]["url"], stream=True)
        with open(filename,'wb') as f:
            shutil.copyfileobj(r2.raw, f) # thanks Mystikfluu 

        with open(filename, 'rb') as image:
            await client.user.edit(avatar=image.read())

        os.remove(filename)
    else:
        await ctx.message.edit("An error occured")

@client.command(alias=["changeprefix"])
async def setprefix(ctx, new_prefix: str):
    """changes the current prefix"""
    config["PREFIX"] = new_prefix

    json_object = json.dumps(config, indent=4)

    with open(".content/config.json", "w") as outfile:
        outfile.write(json_object)

    reloadConfig()

    client.command_prefix = new_prefix
    CreateStartScreen()

@client.command()
async def settenorapi(ctx, key: str):
    """sets the tenor api key"""
    config["TENORAPIKEY"] = key

    json_object = json.dumps(config, indent=4)

    with open(".content/config.json", "w") as outfile:
        outfile.write(json_object)

    reloadConfig()


@client.command()
async def changestatus(ctx, *, status: str):
    """changes your status to the given one"""
    if(status.lower() in ["online", "dnd", "do not disturb", "idle", "invisible"]):
        await setStatus(status)
        CreateStartScreen()
    else:
        print("unkown status")


@client.command(alias=["configbackup"])
async def backupconfig(ctx):
    """creates a backup of the current config in ./configbackups"""
    if not os.path.exists("./configbackups"):
        os.makedirs("configbackups")

    json_object = json.dumps(config, indent=4)

    num = len([name for name in os.listdir('./configbackups') if os.path.isfile(os.path.join("./configbackups", name))])

    with open(f"configbackups/backup_{num}.json", "w") as outfile:
        outfile.write(json_object)


    print(f"Created backup no. {num}")


@client.command()
async def applyconfig(ctx, number: int):
    """loads a previously saved config from ./configbackups"""
    if not os.path.exists(f"./configbackups/backup_{number}.json"):
        print("No config with that number found")
        return

    json_object = json.dumps(json.load(open(f'configbackups/backup_{number}.json', 'r')), indent=4)

    with open(".content/config.json", "w") as outfile:
        outfile.write(json_object)

    reloadConfig()
    CreateStartScreen()

    print(f"Loaded config {number}")


@client.command()
async def viewconfig(ctx, show_token: typing.Optional[str] = ""):
    """sends the entire config except the token if send_token is not yes"""
    with open('.content/config.json', 'r') as openfile:
        config = json.load(openfile)

    if (show_token.lower() not in ["y", "ye", "yes"]):
        config["TOKEN"] = "Hidden"
    config = json.dumps(config)
    config = config.replace("{","{\n ").replace("}","\n}").replace(",",",\n")

    await ctx.send(f"```{config}```")


@client.command(alias=["print"])
async def printtocmd(ctx, *, text: str):
    print(text + "\n")

@client.command()
async def shutdown(ctx):
    sys.exit()

client.run(TOKEN)
