# Insertion sort.
# Would be cool to map index to position in a line
# and value to size, e.g. of a line of pumpkins.

li = [2,1,3,5,4,0,2,7,5,3,0]

print(li)
from copy import copy
def insSort(_list):

    ol=copy([_list[0]])
    ul=copy(_list[1:])
    print(ol," ",ul)
    inserted=False
    for iU in range(len(ul)):
        for iO in range(len(ol)):
            if ul[iU] <= ol[iO]:
                print('Inserting ', ul[iU])
                ol.insert(iO,ul[iU])
                inserted=True
                break 
        if not inserted:
            ol.append(ul[iU])
            print('Appending ', ul[iU])
        inserted=False
    
    return ol

print("Ordered list, ",insSort(li))