"""
Code to implement a 2 Pass Assembler in Python that will take in Assembly Code and Produce a Binary Code
"""

import pandas as pd
    
# Function to generate symbol table using the first pass
def firstPass(instructionSet):
    symbols = []
    lowerByte = []
    higherByte = []
    counter = 0
    code = open("SampleCode1.txt")
    for line in code:
        line = line.strip()
        if len( line.split(':') ) > 1 :
            hexcode = hex(counter)[2:]
            symbols.append(line.split(':')[0])
            lowerByte.append(hexcode[2:])
            higherByte.append(hexcode[:2])
            line = line.split(':')[1]
            line = line[2:]
        if line == 'END':
            break
        elif line.split()[0] == 'ORG':
            counter = int( line.split()[1],16 )
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
    symbolFrame = pd.DataFrame()
    symbolFrame['Symbol'] = symbols
    symbolFrame['lowerByte'] = lowerByte
    symbolFrame['higherByte'] = higherByte
    return symbolFrame

# Function to generate symbol table using the first pass
def secondPass(instructionSet,symbolFrame):
    counter = 0
    hexcodes = []
    bincodes = []
    counterPositions = []
    lineOfCode = []
    code = open("SampleCode1.txt")
    for line in code:
        line = line.strip()
        if len( line.split(':') ) > 1 :
            line = line.split(':')[1]
            line = line[1:]
        if line == 'END':
            break
        elif line.split()[0] == 'ORG':
            counter = int( line.split()[1],16 )
        elif len( instructionSet[ instructionSet['Mnemonic'] == line ] ) > 0:
            hexcode = instructionSet[ instructionSet['Mnemonic'] == line ]['Hex'].to_string(index=False)
            bincode = ( bin(int(hexcode, 16))[2:] ).zfill(8)
            hexcodes.append(hexcode)
            bincodes.append(bincode)
            counterPositions.append(hex(counter)[2:])
            lineOfCode.append(line)
            counter += 1
        elif len( line.split(',') ) > 1:
            hexcode = instructionSet[ instructionSet['Mnemonic'] == line.split(',')[0] ]['Hex'].to_string(index=False)
            bincode = ( bin(int(hexcode, 16))[2:] ).zfill(8)
            hexcodes.append(hexcode)
            bincodes.append(bincode)
            counterPositions.append(hex(counter)[2:])
            lineOfCode.append(line.split(',')[0])
            counter += 1
            word = line.split(',')[1]
            if len( word ) == 3:
                hexcode = word[:2]
                bincode = ( bin(int(hexcode, 16))[2:] ).zfill(8)
                hexcodes.append(hexcode)
                bincodes.append(bincode)
                counterPositions.append(hex(counter)[2:])
                lineOfCode.append(line.split(',')[0])
                counter += 1
            else:
                hexcode = word[2:4]
                bincode = ( bin(int(hexcode, 16))[2:] ).zfill(8)
                hexcodes.append(hexcode)
                bincodes.append(bincode)
                counterPositions.append(hex(counter)[2:])
                lineOfCode.append(hexcode)
                counter += 1
                hexcode = word[:2]
                bincode = ( bin(int(hexcode, 16))[2:] ).zfill(8)
                hexcodes.append(hexcode)
                bincodes.append(bincode)
                counterPositions.append(hex(counter)[2:])
                lineOfCode.append(hexcode)
                counter += 1
        else:
            hexcode = instructionSet[ instructionSet['Mnemonic'] == line.split()[0] ]['Hex'].to_string(index=False)
            bincode = ( bin(int(hexcode, 16))[2:] ).zfill(8)
            hexcodes.append(hexcode)
            bincodes.append(bincode)
            counterPositions.append(hex(counter)[2:])
            lineOfCode.append(line.split()[0])
            counter += 1
            symbol = symbolFrame[ symbolFrame['Symbol'] == line.split()[1] ]
            byte = symbol['lowerByte'].to_string(index=False)
            bincode = ( bin(int(byte, 16))[2:] ).zfill(8)
            hexcodes.append(byte)
            bincodes.append(bincode)
            counterPositions.append(hex(counter)[2:])
            lineOfCode.append(symbol['Symbol'].to_string(index=False))
            counter += 1
            byte = symbol['higherByte'].to_string(index=False)
            bincode = ( bin(int(byte, 16))[2:] ).zfill(8)
            hexcodes.append(byte)
            bincodes.append(bincode)
            counterPositions.append(hex(counter)[2:])
            lineOfCode.append(symbol['Symbol'].to_string(index=False))
            counter += 1
    
    frame = pd.DataFrame()
    frame['Counter'] = counterPositions
    frame['Code'] = lineOfCode
    frame['HexCode'] = hexcodes
    frame['BinaryCode'] = bincodes
    return frame

# Main working of the code begins here
instructionSet = pd.read_csv("8085InstructionSet.csv")
symbolFrame = firstPass(instructionSet)
frame = secondPass(instructionSet,symbolFrame)
print frame
