# Insertion sort.

li = [2,1,3,5,4,0,2,7,5,3,9]

print(li)

def insSort(_list):
    iS=0 # Sorted index, furthest to right.
    l=len(_list)

    ol=_list[0:iS]
    ul=_list[iS+1:l]

    for i in range(len(ul)):
        for j in range(len(ol)):
            if ul[i] < ol[j]:
                ol.insert(j,ul[i])
                ul.remove(i)
                break
        


    return ol

print("Ordered list, ",insSort(li))






