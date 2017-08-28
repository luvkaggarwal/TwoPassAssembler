"""
Code to implement a 2 Pass Assembler in Python that will take in Assembly Code and Produce a Binary Code
"""

import pandas as pd
    
# Function to generate symbol table using the first pass
def firstPass(code,instructionSet):
    symbolTable = []
    counter = 0
    
    for line in code:
        if line.split()[0] == 'ORG':
            counter = int( line.split()[1] )
        elif len( line.split(':') ) > 1 :
            symbolTable.append([line.split(':')[0],counter%100,counter/100])
            counter += 1
        elif len( instructionSet[ instructionSet['Mnemonic'] == line ] ) > 1:
            counter +=1
        elif len( line.split(',') ) > 1:
            word = line.split(',')[1]
            if len( word ) == 3:
                counter += 2
            else:
                counter +=3
        else:
            counter += 3
    return symbolTable

# Main working of the code begins here
code = open("SampleCode1.txt")
instructionSet = pd.read_csv("8085InstructionSet.csv")
symbolTable = firstPass(code,instructionSet)
print symbolTable
