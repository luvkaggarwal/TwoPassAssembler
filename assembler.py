"""
Code to implement a 2 Pass Assembler in Python that will take in Assembly Code and Produce a Binary Code
"""

import pandas as pd

# Function to return label
def processLine(line):
    return line.split(',')[0]
    
# Function to generate symbol table using the first pass
def firstPass(code):
    symbolTable = []
    counter = 0
    flag = -1

    for line in code:
        if line.split()[0] == 'ORG':
            counter = int( line.split()[1] ) - 1
        elif len( line.split(',') ) > 1 :
            symbolTable.append([line.split(',')[0],counter])
        counter += 1            
    return symbolTable

# Main working of the code begins here
code = open("SampleCode1.txt")
instructionSet = pd.read_csv("8085InstructionSet.csv")
symbolTable = firstPass(code)
print code
print instructionSet
