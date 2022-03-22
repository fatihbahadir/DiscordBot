import yaml
from random import randint
import requests
from bs4 import BeautifulSoup
import urllib.request
import re

def load_bot_data(path="Reqs//bot_adj.yaml"):
    with open(path, "r") as stream: # Read YAML data
        try:
            data = yaml.safe_load(stream) # Convert YAML to list in array
            return data
        except yaml.YAMLError as exc:
            raise Exception("ERROR: "+exc)

def prettify(text):
    return "```"+str(text)+"```"

def create_list(title, items, numeric=False):
    if numeric:
        text = "\n"+title.upper()
        for index, item in enumerate(items, 1):
            text += f"\n{index}) {item}"
        message = prettify(text)
    else:
        message = prettify("\n "+title.upper()+"\n"+"\n".join(["- "+i for i in items]))
    return message

def get_random_color():
    color_list = load_bot_data()["random-colors"]
    selected_color = color_list[randint(0,len(color_list)-1)]
    return selected_color

def get_max_lenght(names):
    max = 0
    for name in names:
        if len(name) > max:
            max = len(name)
    return max

def adjust_commands(max_lenght, cog_commands):
    pattern = "- {:<"+str(max_lenght)+"} : {}"
    commands_text = "\n".join([pattern.format(*command) for command in cog_commands])
    return "```" + commands_text + "```"

def get_yt_ids(url):
    html = urllib.request.urlopen(url)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())[:5]
    return video_ids[:5]

def get_yt_title(urls):
    
    video_data = []

    for url in urls:
        html = urllib.request.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string[:-10]
        video_data.append((title, url))
    
    return video_data

def check_steam_profile(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    error_message = soup.find("div", {"id": "message"})

    return soup

def get_steam_profile(ctx):
    
    profile_meta = {}
    profile_meta["name"] = ctx.find("div", {"class": "persona_name"}).span.text
    profile_meta['avatar-url'] = ctx.find("div", {"class":"playerAvatarAutoSizeInner"}).find_all("img")[-1]['src']
    profile_meta["level"] = ctx.find("div", {"class":"friendPlayerLevel"}).text

    all_counters = ctx.find("div", {"class":"profile_content"}).find_all("span", {"class": "profile_count_link_total"})
    counter_vars = [item.text.replace("\t","").replace("\r","").replace("\n","").replace(" ","") for item in all_counters]
    profile_meta['rozet'] = counter_vars[0]
    profile_meta['games'] = counter_vars[1]

    game_data = []
    for game_class in ctx.find_all("div", {"class":"game_info"}):
        game_cap_url = game_class.find("div", {"class":"game_info_cap"}).find("a").find("img")['src']
        game_info_detail = game_class.find("div", {"class":"game_info_details"}).text.replace("\n","").replace("\r","").split("\t")
        game_info = [i for i in game_info_detail if i]
        game_name = game_class.find("div", {"class":"game_name"}).find("a").text

        game_data.append((game_cap_url, game_info,game_name))

    profile_meta['recent-games'] = game_data

    return profile_meta

def remove_chars(text):
    replace_chars = [ ('ı','i'), ('İ','I'), ('ü','u'), ('Ü','U'), ('ö','o'), ('Ö','O'), ('ç','c'), ('Ç','C'), ('ş','s'), ('Ş','S'), ('ğ','g'), ('Ğ','G') ]
    for search, replace in replace_chars:
        text = text.replace(search, replace)
    return text

def get_channels(bot):
    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append((channel.name, channel.id))
    return text_channel_list

def convert_time(date):
    if date > 3600:
        result = str(round(date/3600,1))+" h"
    elif date > 60:
        result = str(round(date/60 ,1))+" m"
    else:
        result = str(round(date, 1))+" s"
    return result


def fetch_json_data():
    pass

def dump_json_data ():
    pass