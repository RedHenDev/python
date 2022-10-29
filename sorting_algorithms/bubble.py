"""
Bubble Sort 1.0
Oct 2022
"""
import time
from random import randint

my_list = []

# NB list of 10K takes 65-74 seconds by bubble.
n=10
for i in range(n):
    my_list.append(randint(0,9))

print("My list is, ", my_list)

swapped = True

t0=time.process_time()
while swapped == True:
    swapped = False
    for i in range(len(my_list)-1):
        if my_list[i] > my_list[i+1]:
            temp = my_list[i]
            my_list[i]=my_list[i+1]
            my_list[i+1]=temp
            swapped=True
t1=time.process_time()
r=(t1-t0)
print("All done, sir. Have a nice day. Your ordered list: ",my_list)
print("Bubble Sort algorithm took " + str(r) + "seconds.")