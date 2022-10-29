"""
Merge sort
Oct 2022

Thank you to...
https://medium.com/@amirziai/
merge-sort-walkthrough-with-code-in-python-e4f76d90a4ea
"""
import time
from random import randint

my_list = []

# NB list of 10K takes 65-74 seconds by bubble sort.
# NB list of 10K takes 4.5 seconds by insertion sort.
# NB list of 10K takes 0.2 seconds by merge sort.
# NB list of 100K takes 2 seconds by merge sort.
n=999
for i in range(n):
    my_list.append(randint(0,9))

print("My list is, ", my_list)

def splitList(_list):
    pivot=len(_list)//2
    list1=_list[:pivot]
    list2=_list[pivot:]
    return list1, list2

def mergeSorted(_l1,_l2):
    if len(_l1)==0:
        return _l2
    elif len(_l2)==0:
        return _l1
    
    merged_list=[]
    target_len=len(_l1)+len(_l2)
    index_r = index_l = 0
    while len(merged_list) < target_len:
        if _l1[index_l] <= _l2[index_r]:
            merged_list.append(_l1[index_l])
            index_l+=1
        else:
            merged_list.append(_l2[index_r])
            index_r+=1

        if index_r==len(_l2):
            merged_list += _l1[index_l:]
            break
        elif index_l==len(_l1):
            merged_list += _l2[index_r:]
        # print('iL ',index_l)
        # print('iR ',index_r)
    return merged_list

def mergeSort(_l):
    if len(_l) <= 1:
        return _l
    else: 
        l, r = splitList(_l)
        return mergeSorted(mergeSort(l),mergeSort(r))

splits=splitList(my_list)
print(  '\n And split is ', splits)

t0=time.process_time()
ms = mergeSort(my_list)
t1=time.process_time()
r=t1-t0
print(  '\n Final merged list: ', ms)
print('Merge sort completed in ',r,'seconds.')