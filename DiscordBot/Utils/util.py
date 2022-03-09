import yaml
from random import randint
import requests
from bs4 import BeautifulSoup

def load_bot_data(path="Reqs//bot_adj.yaml"):
    with open(path, "r") as stream: # Read YAML data
        try:
            data = yaml.safe_load(stream) # Convert YAML to list in array
            return data
        except yaml.YAMLError as exc:
            raise Exception("ERROR: "+exc)

def prettify(text):
    return "```"+str(text)+"```"

def create_list(title, items):
    message = prettify("yaml\n "+title.upper()+"\n"+"\n".join(["- "+i for i in items]))
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

def get_yt_title(url):
    r = requests.get(url)
    s = BeautifulSoup(r.text, "html.parser")
    title = s.find('h1', id="video-title").text.replace("\n", "")
    return title