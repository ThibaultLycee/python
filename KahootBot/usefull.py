"""A short file with a few things for the main program

CONTENT:
    FUNCTION:
        None
    
    DECORATORS:
        ConsoleLogger

    CLASS:
        ConsoleContent:
            __init__ => 
                args:
                    line_length {int}: the max length of a line
                return:
                    nothing
                recommand:
                    nothing

            __repr__ =>
                args:
                    nothing
                return:
                    a string version of the content
                recommand:
                    don't directly call, use 'print'
            
            add_line =>
                args:
                    line {string}: the new line to be added
                return:
                    nothing
                recommand:
                    nothing
            
            formatContent =>
                args:
                    nothing
                return:
                    the content of the console
                recommand:
                    use getContent instead
            
            getContent =>
                args:
                    nothing
                return:
                    the content of the console
                recommand:
                    nothing

"""

import functools

class ConsoleContent:
    """A class that handle the content of the console
    """
    def __init__(self, line_length):
        self.content = []
        self.line_length = line_length

    def add_line(self, line):
        """Add a new line to the console
        """
        while line != "":
            self.content.append(line[:self.line_length])
            line = line[self.line_length:]

    def formatContent(self):
        """Format the content of the console
        """
        toReturn = ""
        for line in self.content: toReturn += f'{line} \n'
        return toReturn

    def getContent(self):
        """Return the content of the console
        """
        return self.formatContent()

    def __repr__(self):
        toReturn = ""
        for line in self.content: toReturn += f'{line} \n'
        return toReturn
