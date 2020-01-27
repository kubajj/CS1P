def selectionSort(alist):
    for i in range(len(alist)):      
        min_so_far = i 
        # find the minimum so far in the unsorted part of the list
        for j in range(i+1, len(alist)): 
            if alist[min_so_far] > alist[j]: 
                min_so_far = j 
        alist[i], alist[min_so_far] = alist[min_so_far], alist[i]
    return alist 

alist = [54,26,93,17,77,31,44,55,20]
selectionSort(alist)
print(alist)
