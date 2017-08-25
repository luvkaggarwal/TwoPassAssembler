"""
Code to implement a 2 Pass Assembler in Python that will take in Assembly Code and Produce a Binary Code
"""

# Function to return label
def processLine(line):
    return line.split(',')[0]
    
# Function to generate symbol table using the first pass
def firstPass(code):
    symbolTable = []
    counter = 0
    flag = -1
    for line in code:
        for word in line.split():
            if word == 'ORG':
                flag = 1
            elif flag == 1:
                counter = int(word) - 1
                flag = -1
            elif word == 'DEC' or word == 'HEX':
                symbolTable.append([processLine(line),counter])
        counter += 1            
    return symbolTable

# Main working of the code begins here
code = open("AssemblyLanguageCode.txt")

symbolTable = firstPass(code)
print symbolTable
