"""
Sun 10th Jan 2021
B New
"""

"""pass in 0-15, return hex 
symbol as string"""
def giveHexSym(_num):
  # Convert to + if -.
  if _num < 0: _num = abs(_num)
  
  # Beyond max, return max.
  if _num > 15: return 'f'
  
  # Below 10 return number as string.
  elif _num < 10: return str(_num)
  
  # OK now the proper stuff.
  elif _num == 10: return str('a')
  elif _num == 11: return str('b')
  elif _num == 12: return str('c')
  elif _num == 13: return str('d')
  elif _num == 14: return str('e')
  elif _num == 15: return str('f')
  
whatNum = input("What denary value\nto convert to hexadecimal? >")
#print(giveHexSym(int(whatNum)))

tot = 0   # Running integer total.
hx = [0,0,0,0,0,0,0,0]  # Integer list.
          # This will be used to build
          # resultant hex string.

wip = 0   # Index being worked on.
hip = 0   # Highest index as non-zero.
        # Maybe I don't even need this.

while tot < int(whatNum):
  # Why don't we iterate over length of
  # hx list, and decide what needs to
  # happen to each item based on what
  # neighbouring items' values are?
  
  """
  When does an item (i) increment?
  (a) 
  when i == hx[0] and hx[0] < 15. Break.
  
  (aa) When hx[0] == 15...then the next
  lowest item < 15 should increment, also
  all items behind reset to 0. Break.
  
  (d)special: when i == len-1 and is 15
  and all preceding items are 15, then
  hx.append(1) and also set all preceding
  items lower than new len-1 to 0.
  
  I need to combine (b) and (c) -- 
  generalise.
  Plus, I need to account for when 
  hx[0] == 15
  Oh -- think accomplished both in one
  fell swoop: see (aa).
  Oh.2 -- and (d) looks to be a special
  case of (aa).
  
  """
  for i in range(0,len(hx)):
    # a
    if i==0 and hx[i]<15:
      hx[i]+=1
      break
    # aa
    elif i==0 and hx[i]==15:
      for j in range(1,len(hx)):
        if hx[j]<15:
          hx[j]+=1
          for k in range(0,j):
            hx[k]=0
          break

  tot+=1
  
#print("hx = " + str(hx))
#print("Length of hx = " + str(len(hx)))

# Now let's correct the symbols.
for i in range(len(hx)):
  hx[i] = giveHexSym(hx[i])

# Shave off dead zeroes.
# NB we break as soon as hitting our first non-zero.
for i in range(len(hx)-1,-1,-1):
  if hx[i] == '0':
    hx.pop(i)
  else: break

# Reverse and render list to string.
hx.reverse()
sTemp = ''
finalHexString = sTemp.join(hx)
print("hex = " + finalHexString)
