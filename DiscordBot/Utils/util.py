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

def crete_profile(member):
    return member

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

def remove_chars(text):
    replace_chars = [ ('ı','i'), ('İ','I'), ('ü','u'), ('Ü','U'), ('ö','o'), ('Ö','O'), ('ç','c'), ('Ç','C'), ('ş','s'), ('Ş','S'), ('ğ','g'), ('Ğ','G') ]
    for search, replace in replace_chars:
        text = text.replace(search, replace)
    return text