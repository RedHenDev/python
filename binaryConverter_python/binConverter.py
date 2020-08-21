"""
Created Fri 21st Aug 2020

"""

import math
from datetime import datetime

# Enter your own binary code.
binCode = [1,0,1]

def convFdec(_c):
  # Make sure a positive int, first:
  _c = math.floor(math.fabs(_c))
  # Build from left.
  # Reverse at end.

  # Two steps.
  # First, how many digits do we need?
  # digits = log2(_c)+1.
 
  if _c == 0:
    binaryList = [0]
    return binaryList
  digits = math.floor(math.log(_c, 2) + 1)
  #print("Digits = " + str(digits))

  # Step 2.
  # Build a list (like an array).
  # It's length = digits.
  # So, we can loop over for each digit.
  # Then, determine which 'state' digit is.
  # Have we cycled through an odd or even
  # number of times for 2^position?
  # Position starts at 0, since this is the
  # first exponent.
  # So, n = _c/2^position.
  # If even (n%2==0) then digit = 0.
  # If odd (n%2!=0) then digit = 1.
  binaryList = []
  currentD = 0
  i = 0
  while i < digits:
    if math.floor(_c/2**i)%2==0: currentD = 0
    else: currentD = 1
    binaryList.append(currentD)
    i += 1
  
  # Don't forget to reverse list!
  binaryList.reverse()
  return binaryList


def convFbin(_code):
  i = 0
  total = 0
  while i < len(_code):
    if _code[len(_code)-1-i]:
      total += 2**(i)
    i = i + 1
  return total

# Convert from binary to decimal.
print("binCode is " + 
str(binCode))
print("Converted to decimal: " + str(convFbin(binCode))) 

# Convert from decimal to binary.
x = input("\nDecimal: ")
print("\ndec = " + str(x))
print("Bin = " + str(convFdec(float(x))))

print("\nBINARY CLOCK\n")

looping = True
while looping:
    time = datetime.now().time()
    print(time.strftime('%I') + " " + time.strftime('%p') + " " + time.strftime('%M'))
    print(str(convFdec(int(time.strftime('%I')))) + " " + time.strftime('%p') + " " +
          str(convFdec(int(time.strftime('%M')))) )
    ip = input()
    if ip == 'q':
        looping = False

print("You have quit. Thank you.")

