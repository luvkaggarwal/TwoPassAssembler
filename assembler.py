"""
Code to implement a 2 Pass Assembler in Python that will take in Assembly Code and Produce a Binary Code
"""

import pandas as pd

# Functoin to add binarycode and counter value for a given hexcode
def symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions):
    bincode = ( bin(int(hexcode, 16))[2:] ).zfill(8)
    hexcodes.append(hexcode)
    bincodes.append(bincode)
    counterPositions.append(hex(counter)[2:])
    return hexcodes,bincodes,counterPositions

# Function to generate symbol table using the first pass
def firstPass(instructionSet):
    symbols = []
    lowerByte = []
    higherByte = []
    counter = 0
    code = open("SampleCode1.txt")
    for line in code:

        # Remove the carriage return from each line
        line = line.strip()

        # If referenced location, store the reference with location counter value
        # Eg - LOOP: DCX H  // Here, store 'LOOP' with LC
        if len( line.split(':') ) > 1 :
            hexcode = hex(counter)[2:]
            symbols.append(line.split(':')[0])
            lowerByte.append(hexcode[2:])
            higherByte.append(hexcode[:2])
            line = line.split(':')[1]

            # Remove reference to get actual line of code
            # Eg - LOOP: DCX H  // Here, remove 'LOOP: ' to get the actual line of code
            line = line[2:]

        # No Further commands available
        if line == 'END':
            break
        elif line.split()[0] == 'ORG':
            # Set Location Counter
            counter = int( line.split()[1],16 )
        elif len( instructionSet[ instructionSet['Mnemonic'] == line ] ) > 0:
            # For direct instructions
            # Eg - DCX H
            counter += 1
        elif len( line.split(',') ) > 1:
            # For instructions with reference to Memory or direct values
            # Eg - LXI H,XXXXH ; MVI A,XXH
            word = line.split(',')[1]
            if len( word ) == 3:
                # Direct Value Reference
                counter += 2
            else:
                # Memory Reference
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

        # Remove the carriage return from each line
        line = line.strip()

        # If referenced location, remove the reference
        # Eg - LOOP: DCX H  // Here, remove 'LOOP: ' to get the actual line of code
        if len( line.split(':') ) > 1 :
            line = line.split(':')[1]
            line = line[1:]

        # No Further commands available
        if line == 'END':
            break
        elif line.split()[0] == 'ORG':
            # Set Location Counter
            counter = int( line.split()[1],16 )
        elif len( instructionSet[ instructionSet['Mnemonic'] == line ] ) > 0:
            # For direct instructions
            # Eg - DCX H
            hexcode = instructionSet[ instructionSet['Mnemonic'] == line ]['Hex'].to_string(index=False)
            hexcodes,bincodes,counterPositions = symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions)
            lineOfCode.append(line)
            counter += 1
        elif len( line.split(',') ) > 1:
            # For instructions with reference to Memory or direct values
            # Eg - LXI H,XXXXH ; MVI A,XXH

            # Find HexCode for Mnemonic
            hexcode = instructionSet[ instructionSet['Mnemonic'] == line.split(',')[0] ]['Hex'].to_string(index=False)
            hexcodes,bincodes,counterPositions = symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions)
            lineOfCode.append(line.split(',')[0])
            counter += 1

            # Find HexCode for Memory Reference/Direct Value Reference
            word = line.split(',')[1]
            if len( word ) == 3:
                # Direct Value Reference
                hexcode = word[:2]
                hexcodes,bincodes,counterPositions = symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions)
                lineOfCode.append(line.split(',')[0])
                counter += 1
            else:
                # Memory Reference

                # For Lower Byte
                hexcode = word[2:4]
                hexcodes,bincodes,counterPositions = symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions)
                lineOfCode.append(hexcode)
                counter += 1

                # For Higher Byte
                hexcode = word[:2]
                hexcodes,bincodes,counterPositions = symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions)
                lineOfCode.append(hexcode)
                counter += 1
        else:
            # For statements like JNZ LOOP

            # Find HexCode for Mnemonic
            hexcode = instructionSet[ instructionSet['Mnemonic'] == line.split()[0] ]['Hex'].to_string(index=False)
            hexcodes,bincodes,counterPositions = symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions)
            lineOfCode.append(line.split()[0])
            counter += 1

            # Find HexCodes for Symbol(Reference to another location) from SymbolFrame
            # For Lower Byte
            symbol = symbolFrame[ symbolFrame['Symbol'] == line.split()[1] ]
            hexcode = symbol['lowerByte'].to_string(index=False)
            hexcodes,bincodes,counterPositions = symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions)
            lineOfCode.append(symbol['Symbol'].to_string(index=False))
            counter += 1
            
            # For Higher Byte
            hexcode = symbol['higherByte'].to_string(index=False)
            hexcodes,bincodes,counterPositions = symbolParser(counter,hexcode,hexcodes,bincodes,counterPositions)
            lineOfCode.append(symbol['Symbol'].to_string(index=False))
            counter += 1

    # Compile into a single Data Frame
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
