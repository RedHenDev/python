"""
Attempt at writing a hexadecimal to denary converter.
Sat 9th Jan 2021

B New
"""

"""find symbol value in hex,
else return int of number passed in"""
def hexLookup(_sym):
    _sym = _sym.strip().lower()
    if _sym=='a':
        return 10
    elif _sym=='b':
        return 11
    elif _sym=='c':
        return 12
    elif _sym=='d':
        return 13
    elif _sym=='e':
        return 14
    elif _sym=='f':
        return 15
    else: return int(_sym)

def hexToDen(_str):
    """
    So, we want to iterate over given hex string.
    Find value in syntactic conext of each index by
    16, raised to the power of each symbol's value.
    """
    # First, convert _str to a string with lowercase chars and spaces removed.
    hexS = _str.lower().strip()
    runningTot = 0
    
    for i in range(0,len(hexS)):
        currentSymbol = hexS[len(hexS)-i-1]
        currentVal = (16 ** i) * hexLookup(currentSymbol)
        print("Current symbol " + currentSymbol + "'s value is " + str(currentVal))
        runningTot += currentVal

    return runningTot

whatHex = input("What hexadecimal number to convert to denary? > ")

print("Total = " + str(hexToDen(whatHex)))
        
