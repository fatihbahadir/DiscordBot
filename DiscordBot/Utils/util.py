def prettify(text):
    return "```"+str(text)+"```"

def create_list(title, items):
    message = prettify(title.upper()+"\n".join(["- "+i for i in items]))
    return message