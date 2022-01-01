input = open("input.txt", "rt")
output = open("output.txt", "wt")

class simpleModif():
    def __init__(self, caractere, toReplace, iteration, name):
        self.name = name
        self.caractere = caractere
        self.toReplace = toReplace
        self.iteration = iteration

class toChange():
    def __init__(self, caractere, toReplace, iteration, name):
        self.name = name
        self.caractere = caractere
        self.toReplace = toReplace
        self.iteration = iteration


class balisesComplexes():
    def __init__(self, caractere, toReplace, name):
        self.name = name
        self.caractere = caractere
        self.toReplace = toReplace

bold = simpleModif("/", ("<b>", "</b>"), 0, "bold")
italique = simpleModif("$", ("<i>", "</i>"), 0, "italique")
br = simpleModif("!", ("<br/>", "<br/>"), 0, "break")
underline = simpleModif("_", ("<u>", "</u>"), 0, "underline")
exposant = simpleModif("^", ("<sup>", "</sup>"), 0, "exposant")


titre1 = toChange("1", ("<h1>", '</h1>\n<p class="indent">\n    '), 0, "titre1")
titre2 = toChange("2", ("<h2>", '</h2>\n<p class="indent">\n    '), 0, "titre2")
titre3 = toChange("3", ("<h3>", '</h3>\n<p class="indent">\n    '), 0, "titre3")
titre4 = toChange("4", ("<h4>", '</h4>\n<p class="indent">\n    '), 0, "titre4")
titre5 = toChange("5", ("<h5>", '</h5>\n<p class="indent">\n    '), 0, "titre5")
titre6 = toChange("6", ("<h6>", '</h6>\n<p class="indent">\n    '), 0, "titre6")

img = balisesComplexes("?", '<img src="" height="px">', "image")

toShow = {}

dansParagraphe = [bold, italique, br, underline, exposant]
changements = [titre1, titre2, titre3, titre4, titre5, titre6]
changementsComplexes = [img]

for i in changements:
    toShow[i.name] = i.caractere

for i in changementsComplexes:
    toShow[i.name] = i.caractere

for i in dansParagraphe:
    toShow[i.name] = i.caractere


def convert(entree):
    global output
    texte = entree.read().split(" ")

    result = '<p class="indent">\n    '

    for mot in texte:
        toChange = True
        if mot[0] == "-":
            for command in changements:
                if mot == "-" + command.caractere:
                    if result[-23:] == '<p class="indent">\n    ':
                        result = result[:-23] + "\n"
                    elif result[-1] != ">" and command.iteration % 2 == 0:
                        result += "\n</p>\n"
                    result += command.toReplace[command.iteration % 2]
                    command.iteration += 1
                    toChange = False
                    break

            for command in changementsComplexes:
                if mot == "-" + command.caractere:
                    if result[-23:] == '<p class="indent">\n    ':
                        result = result[:-23] + "\n"
                    elif result[-1] != ">":
                        result += "\n</p>\n"
                    result += command.toReplace + '<p class="indent">\n    '
                    toChange = False
                    break

            for command in dansParagraphe:
                if mot == "-" + command.caractere:
                    result += command.toReplace[command.iteration % 2]
                    command.iteration += 1
                    toChange = False
                    break

        if toChange:
            result += " " + mot

    if result[-4:] != "</p>" and result[-1] == ">":
        result += "\n</p>"

    if result[0] == "\n":
        result = result[1:]

    output.write(result)
    return result

print([i for i in toShow.items()])

print(convert(input))

output.close()