import json, re
from random import choice

from discord import Interaction as Itr

CUSTOMS = ["alesan", "games", "enemies", "people", "powerups", "objects"]

def loadSuggestions(custom, custom_suggestions):
    suggestionsfile = "suggestions"
    if custom_suggestions == "Just Custom":
        suggestionsfile = "suggestions_custom"

    with open(f'./{suggestionsfile}.json') as file:
        suggestions = json.load(file)

    origin, images, groups = False, False, {}
    for name in suggestions:
        if name == "_origin":
            origin = suggestions[name]
        if name == "_images":
            images = suggestions[name]
        else:
            if name in CUSTOMS:
                groups[name] = []
                if custom_suggestions != "Just Custom":
                    groups[name] += suggestions[name]
                if custom_suggestions != "Just Default":
                    if name == "alesan":
                        valname = f"custom_names"
                    else:
                        valname = f"custom_{name}"
                    if len(custom[valname]) == 0 and custom_suggestions == "Just Custom":
                        groups[name] += ["N/A"]
                    else:
                        groups[name] += custom[valname]
            else:
                groups[name] = suggestions[name]

    return origin, images, groups

def createSuggestion(itr:Itr, custom, custom_suggestions):
    origin, images, groups = loadSuggestions(custom, custom_suggestions)

    result = choice(origin)
    result_images = []
    while "{" in result:
        splited = re.split("{(.*?)}", result)
        result = ""
        text = True
        for s in splited:
            if text:
                result += s
            else:
                decision = choice(groups[s])
                if decision.startswith("$"):
                    decision, decisionimg = formatDollar(itr, decision[1:])
                    if decisionimg:
                        result_images.append(decisionimg)
                elif decision in images and images[decision] != "??":
                    result_images.append(images[decision])
                result += decision
            text = not text

    result_images = list(dict.fromkeys(result_images))
    result = result.strip()
    result = result[0].upper() + result[1:]
    return result, result_images

def formatDollar(itr:Itr, type):
    if type == "member":
        member = choice(itr.guild.members)
        return member.display_name, member.display_avatar.url
    elif type == "self":
        member = itr.user
        return member.display_name, member.display_avatar.url
    return "N/A", "N/A"