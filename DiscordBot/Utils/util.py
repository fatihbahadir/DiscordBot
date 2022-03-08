import yaml

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
    message = prettify(title.upper()+"\n"+"\n".join(["- "+i for i in items]))
    return message

def crete_profile(member):
    return member