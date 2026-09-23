def HybridMergeSort(A, left, right, S):
    size = right - left + 1 # size of the array
    if size <= S: # size smaller than a certain set value
        return InsertionSort(A, left, right) # use Insertion sort
    else:
        # MergeSort
        mid = (left + right) // 2
        # recursive calls for MergeSort
        left_comparisons = HybridMergeSort(A, left, mid, S)
        right_comparisons = HybridMergeSort(A, mid + 1, right, S)

        merge_comparisons = Merge(A, left, mid, right)

        return left_comparisons + right_comparisons + merge_comparisons

def InsertionSort(A, left, right):
    comparisons = 0
    for i in range(left+1, right+1): # python does not include last value, so want right to be included
        key = A[i] # selecting element to sort
        j = i-1 # pointer to element before
        while j >= left: # ensure pointer j is not out of range
            comparisons += 1
            if A[j] > key: # checking if the value is bigger than the key saved in A[i]
                A[j + 1] = A[j]
                j -= 1 # shifting pointer j to the left to compare with value to the left
            else: # value is not bigger than the key
                break

        A[j + 1] = key
    return comparisons

def Merge(A, left, mid, right):
    comparisons = 0
    # python slicing 
    L = A[left:mid+1]
    R = A[mid+1:right+1]
    i = j = 0  # initialise starting pointers
    k = left # starting point
    while i < len(L) and j < len(R):
        comparisons += 1
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        else:
            A[k] = R[j]
            j += 1

        k += 1

    # filling in remaining elements
    # Copy anything remaining in L
    while i < len(L):
        A[k] = L[i]
        i += 1
        k += 1

    # Copy anything remaining in R
    while j < len(R):
        A[k] = R[j]
        j += 1
        k += 1

    return comparisons