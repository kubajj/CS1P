def bubbleSort(alist):
    for position, item in enumerate(alist):
        for i in range(len(alist)-1 – position):
            if alist[i]>alist[i+1]: # compare the two neighbors
                alist[i], alist[i+1] = alist[i+1], alist[i] # swap 
        print(position, alist)				
    return alist				

alist = [54,26,93,17,77,31,44,55,20]
bubbleSort(alist)
print(alist)