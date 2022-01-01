import time

instructions = {
    9: 'inp',
    10: 'add',
    11: 'sub',
    12: 'dup',
    13: 'cond',
    14: 'gotou',
    15: 'outn',
    16: 'outa',
    17: 'rol',
    18: 'swap',
    20: 'mul',
    21: 'div',
    23: 'pop',
    24: 'gotos',
    25: 'push',
    27: 'ror'
}

class Stack:
    def __init__(self):
        self.stack = []
    
    def __len__(self):
        return len(self.stack)

    def push(self, val):
        self.stack.insert(0, val)

    def outn(self):
        return self.stack.pop(0)

    def outa(self):
        return chr(self.stack.pop(0))
    
    def add(self):
        self.stack.insert(0, self.stack.pop(1) + self.stack.pop(0))

    def sub(self):
        self.stack.insert(0, self.stack.pop(1) - self.stack.pop(0))

    def mul(self):
        self.stack.insert(0, self.stack.pop(1) * self.stack.pop(0))

    def div(self):
        self.stack.insert(0, self.stack.pop(1) / self.stack.pop(0))
    
    def swap(self):
        self.stack[1], self.stack[0] = self.stack[0], self.stack[1]
    
    def pop(self):
        self.stack.pop(0)
    
    def rol(self):
        start = self.stack[0]
        for i in range(1, len(self.stack)):
            self.stack[i-1] = self.stack[i]
        self.stack[-1] = start

    def ror(self):
        end = self.stack[-1]
        for i in range(len(self.stack)-2, -1, -1):
            self.stack[i+1] = self.stack[i]
        self.stack[0] = end
    
    def dup(self):
        self.push(self.stack[0])

    def cond(self):
        return self.stack.pop(0) != 0



class Program:
    def __init__(self, file):
        self.currentLine = 0
        self.code = []
        self.stack = Stack()
        with open(file, "rt") as file_:
            self.file = file_.read().split('\n')
        for i in range(len(self.file)):
            self.code.append(len(self.file[i]))
    
    def run(self):
        self.lineCorrespondancies = {}
        curLine = 0
        for line in range(1, len(self.code)):
            if self.code[line - 1] not in (25,):
                self.lineCorrespondancies[curLine] = line
                curLine += 1
        self.runLine(self.currentLine)
    
    def runLine(self, line):
        runNext = True
        if line >= len(self.code):
            print('\nExited with code 0')
            return
        if self.code[line] in instructions.keys():
            instr = instructions[self.code[line]]
            if instr == 'inp':
                self.stack.push(ord(input('Input: ')[0]))
            elif instr == 'add':
                if len(self.stack) >= 2:
                    self.stack.add()
                else:
                    print(f'Error on line {line + 1}, not enougth values in stack !')
                    return
            elif instr == 'sub':
                if len(self.stack) >= 2:
                    self.stack.sub()
                else:
                    print(f'Error on line {line + 1}, not enougth values in stack !')
                    return
            elif instr == 'dup':
                if len(self.stack) >= 1:
                    self.stack.dup()
                else:
                    print(f'Error on line {line + 1}, not enougth values in stack !')
                    return
            elif instr == 'cond':
                verified = self.stack.cond()
                if not verified:
                    if self.code[line + 1] in (14, 25):
                        self.currentLine = line + 3
                        runNext = False
                        self.runLine(self.currentLine)
                    else:
                        self.currentLine = line + 2
                        runNext = False
                        self.runLine(self.currentLine)
                else:
                    self.currentLine = line + 1
                    runNext = False
                    self.runLine(self.currentLine)
            elif instr == 'gotou':
                if line < len(self.code):
                    if self.code[line + 1] - 1 < len(self.code):
                        self.currentLine = line + 1
                        runNext = False
                        if self.currentLine in self.lineCorrespondancies.keys():
                            self.runLine(self.code[self.lineCorrespondancies[self.currentLine]])
                        else:
                            time.sleep(.1)
                            self.runLine(self.code[self.currentLine])
                    else:
                        self.runLine(len(self.code) + 120)
                else:
                    self.currentLine = 0
                    self.runLine(0)
            elif instr == 'outn':
                if len(self.stack) >= 1:
                    print(self.stack.outn())
                else:
                    print(f'Error on line {line + 1}, not enougth values in stack !')
                    return
            elif instr == 'outa':
                if len(self.stack) >= 1:
                    print(self.stack.outa())
                else:
                    print(f'Error on line {line + 1}, not enougth values in stack !')
                    return
            elif instr == 'rol':
                if len(self.stack) >= 1:
                    self.stack.rol()
            elif instr == 'swap':
                if len(self.stack) >= 1:
                    self.stack.swap()
            elif instr == 'mul':
                if len(self.stack) >= 2:
                    self.stack.mul()
                else:
                    print(f'Error on line {line + 1}, not enougth values in stack !')
                    return
            elif instr == 'div':
                if len(self.stack) >= 2:
                    self.stack.div()
                else:
                    print(f'Error on line {line + 1}, not enougth values in stack !')
                    return
            elif instr == 'pop':
                if len(self.stack) >= 1:
                    self.stack.pop()
            elif instr == 'gotos':
                self.currentLine = self.stack.stack[0] - 1
                runNext = False
                self.runLine(self.lineCorrespondancies[self.stack.stack.pop(0) - 1])
            elif instr == 'push':
                if line < len(self.code):
                    self.stack.push(self.code[line + 1])
                    self.currentLine = line + 2
                    runNext = False
                    self.runLine(self.currentLine)
                else:
                    print(f'Missing value after line {line}')
                    return
            elif instr == 'ror':
                if len(self.stack) >= 1:
                    self.stack.ror()
            if runNext:
                self.currentLine = line + 1
                self.runLine(self.currentLine)