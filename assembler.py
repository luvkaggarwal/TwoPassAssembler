"""
Code to implement a 2 Pass Assembler in Python that will take in Assembly Code and Produce a Binary Code
"""

import pandas as pd
    
# Function to generate symbol table using the first pass
def firstPass(instructionSet):
    symbolTable = []
    counter = 0
    code = open("SampleCode1.txt")
    for line in code:
        line = line.strip()
        if line == 'END':
            return symbolTable
        elif line.split()[0] == 'ORG':
            counter = int( line.split()[1] )
        elif len( line.split(':') ) > 1 :
            symbolTable.append([line.split(':')[0],counter%100,counter/100])
            counter += 1
        elif len( instructionSet[ instructionSet['Mnemonic'] == line ] ) > 0:
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

# Function to generate symbol table using the first pass
def secondPass(instructionSet,symbolTable):
    counter = 0
    codeTable = []
    code = open("SampleCode1.txt")
    for line in code:
        line = line.strip()
        if line == 'END':
            return codeTable
        elif line.split()[0] == 'ORG':
            counter = int( line.split()[1] )
        elif len( line.split(':') ) > 1 :
            counter += 1
        elif len( instructionSet[ instructionSet['Mnemonic'] == line ] ) > 0:
            hexcode = instructionSet[ instructionSet['Mnemonic'] == line ]['Hex'].to_string(index=False)
            print hexcode
            bincode = ( bin(int(hexcode, 16))[2:] ).zfill(8)
            codeTable.append([counter,bincode])
            counter += 1
            print "I am here",counter
        elif len( line.split(',') ) > 1:
            word = line.split(',')[1]
            if len( word ) == 3:
                counter += 2
            else:
                counter +=3
        else:
            counter += 3
    return codeTable

# Main working of the code begins here
instructionSet = pd.read_csv("8085InstructionSet.csv")
print instructionSet
symbolTable = firstPass(instructionSet)
codeTable = secondPass(instructionSet,symbolTable)
print codeTable
