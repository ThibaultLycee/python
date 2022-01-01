input = open("inputTable.txt", "rt")
output = open("outputTable.txt", "wt")


def convert(table):
    result = '<table border="1" cellpadding="4" cellspacing="0">\n    <thead>\n        <tr>\n            <th><p>'

    ligne1 = table.readline().split()

    for mot in ligne1:
        if mot == "/": result += "</p></th>\n            <th><p>"
        else: result += mot + " "

    result += "</p></th>\n        </tr>\n    </thead>\n    <tbody>\n        <tr>\n            <td><p>"

    for line in table:
        line = line.split(" ")
        print(line)
        for mot in line:
            if mot[-1] == "\n":
                mot = mot[:-1]
            if mot == "/": result += "</p></td>\n            <td><p>"
            else:
                result += mot + " "
        result += "</p></td>\n        </tr>\n        <tr>\n            <td><p>"

    if result[-38:] == "</tr>\n        <tr>\n            <td><p>":
        result = result[:-38]

    result += "</tr>\n    </tbody>\n</table>"
    output.write(result)
    return result

print(convert(input))

input.close()
output.close()