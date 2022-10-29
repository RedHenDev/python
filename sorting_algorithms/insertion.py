"""
Insertion sort
Oct 2022
"""
import time
from random import randint

my_list = []

# NB list of 10K takes 65-74 seconds by bubble sort.
# NB list of 10K takes 4.5 seconds by insertion sort.
# n=10
# for i in range(n):
#     my_list.append(randint(0,9))
my_list=['a','b','x','r']

print(my_list)
from copy import copy
def insSort(_list):
    ol=copy([_list[0]])
    ul=copy(_list[1:])
    print(ol," ",ul)
    inserted=False
    for iU in range(len(ul)):
        for iO in range(len(ol)):
            if ul[iU] <= ol[iO]:
                # print('Inserting ', ul[iU])
                ol.insert(iO,ul[iU])
                inserted=True
                break
        if not inserted:
            ol.append(ul[iU])
            # print('Appending ', ul[iU])
        inserted=False
    
    return ol

t0=time.process_time()
print("Ordered list, ",insSort(my_list))
t1=time.process_time()
r=(t1-t0)
print("Insertion Sort algorithm took " + str(r) + "seconds.")