import os

symbolTable = {"SCREEN": 16384,
               "KBD": 24576,
               "SP": 0,
               "LCL": 1,
               "ARG": 2,
               "THIS": 3,
               "THAT": 4,
               "R0": 0,
               "R1": 1,
               "R2": 2,
               "R3": 3,
               "R4": 4,
               "R5": 5,
               "R6": 6,
               "R7": 7,
               "R8": 8,
               "R9": 9,
               "R10": 10,
               "R11": 11,
               "R12": 12,
               "R13": 13,
               "R14": 14,
               "R15": 15}
currentSymbol = 16
curLine = 0


def openFile(filename):
    lines = open(filename).read().splitlines()
    withoutComments = []
    for curline in lines:
        if not curline.startswith("//") and not isEmpty(curline):
            withoutComments.append(curline.strip())
    return withoutComments


def isEmpty(s):
    return (s == "")


def decimalToBinary(n):
    n = bin(n)
    n = n.split("b")[1]
    return n


def aCodeToHack(aop):
    aop = aop.split("@")[1]
    if not aop.isnumeric():
        insertVarLabel(aop)
        aop = int(symbolTable[aop])
    aop = int(aop)
    aop = decimalToBinary(aop)
    while (len(aop) < 16):
        aop = "0" + aop
    return aop


def main():
    ourFile = openFile(
        "/Users/ivy/Desktop/LearningPython/Assembler/test.asm")
    # print(ourFile)
    print(openFile)
    generateSymbolTable(ourFile)
    print(symbolTable)
    assembled = parseFile(ourFile)
    writeFile("/Users/ivy/Desktop/LearningPython/Assembler/test.hack", assembled)
    print(symbolTable)
    print(assembled)


def writeFile(filename, list):
    with open(filename, 'w') as f:
        for item in list:
            f.write("%s\n" % item)


def commandToBinary(command):
    if (command == "0"):
        return "0101010"
    elif (command == "1"):
        return "0111111"
    elif (command == "-1"):
        return "0111010"
    elif (command == "D"):
        return "0001100"
    elif (command == "A"):
        return "0110000"
    elif (command == "!D"):
        return "0001101"
    elif (command == "!A"):
        return "0110001"
    elif (command == "-D"):
        return "0001111"
    elif (command == "-A"):
        return "0110011"
    elif (command == "D+1"):
        return "0011111"
    elif (command == "A+1"):
        return "0110111"
    elif (command == "D-1"):
        return "0001110"
    elif (command == "A-1"):
        return "0110010"
    elif (command == "D+A"):
        return "0000010"
    elif (command == "D-A"):
        return "0010011"
    elif (command == "A-D"):
        return "0000111"
    elif (command == "D&A"):
        return "0000000"
    elif (command == "D|A"):
        return "0010101"
    elif (command == "M"):
        return "1110000"
    elif (command == "!M"):
        return "1110001"
    elif (command == "-M"):
        return "1110011"
    elif (command == "M+1"):
        return "1110111"
    elif (command == "M-1"):
        return "1110010"
    elif (command == "D+M"):
        return "1000010"
    elif (command == "D-M"):
        return "1010011"
    elif (command == "M-D"):
        return "1000111"
    elif (command == "D&M"):
        return "1000000"
    elif (command == "D|M"):
        return "1010101"


def destinationToBinary(dest):
    if (dest == "M"):
        return "001"
    elif (dest == "D"):
        return "010"
    elif (dest == "MD"):
        return "001"
    elif (dest == "A"):
        return "100"
    elif (dest == "AM"):
        return "101"
    elif (dest == "AD"):
        return "110"
    elif (dest == "AMD"):
        return "111"


def jmpLocToBinary(jmp):
    if (jmp == ""):
        return "000"
    elif (jmp == "JGT"):
        return "001"
    elif (jmp == "JEQ"):
        return "010"
    elif (jmp == "JGE"):
        return "011"
    elif (jmp == "JLT"):
        return "100"
    elif (jmp == "JNE"):
        return "101"
    elif (jmp == "JLE"):
        return "110"
    elif (jmp == "JLE"):
        return "110"
    elif (jmp == "JMP"):
        return "111"


def nonJumpToBinary(cmd):
    destination = cmd.split("=")[0]
    destination = destinationToBinary(destination)
    cmd = cmd.split("=")[1]
    cmd = commandToBinary(cmd)
    return ("111"+cmd + destination + "000")


def jmpToBinary(cmd):
    destination = cmd.split(";")[0]
    jmp = cmd.split(";")[1]
    destination = commandToBinary(destination)
    jmp = jmpLocToBinary(jmp)
    return ("111" + destination + "000" + jmp)


def parseFile(file):
    global curLine
    output = []
    for line in file:
        asBinary = ""
        if ";" in line:
            asBinary = jmpToBinary(line)
        elif "=" in line:
            asBinary = nonJumpToBinary(line)
        elif "@" in line:
            asBinary = aCodeToHack(line)
        else:
            asBinary = line
            asBinary = ""
        if not asBinary == "":
            output.append(asBinary)
        curLine += 1
    return output


def subStringBetween(str, a, b):
    return str[str.find(a)+1:str.find(b)]


def insertVarLabel(str):
    global currentSymbol
    global symbolTable
    if not str in symbolTable:
        symbolTable[str] = currentSymbol
        currentSymbol += 1


def insertLabel(label):
    global symbolTable
    global curLine
    if not label in symbolTable:
        symbolTable[label] = curLine


def generateSymbolTable(list):
    global curLine
    global symbolTable
    for line in list:
        if "(" in line:
            line = subStringBetween(line, "(", ")")
            insertLabel(line)
            curLine -= 1
        curLine += 1


main()
