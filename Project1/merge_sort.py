"""Part (d): original merge sort."""


def MergeSort(A, start, end):
    if end - start <= 1:
        return 0

    mid = start + (end - start) // 2
    left_comparisons = MergeSort(A, start, mid)
    right_comparisons = MergeSort(A, mid, end)
    merge_comparisons = Merge(A, start, mid, end)

    return left_comparisons + right_comparisons + merge_comparisons


def Merge(A, start, mid, end):
    comparisons = 0
    Bl = A[start:mid]  # copy of the left half
    Br = A[mid:end]    # copy of the right half
    i = 0
    k = start

    # For every entry of Br, first copy all Bl entries that are <= Br[j]
    for j in range(len(Br)):
        while i < len(Bl):
            comparisons += 1  # one key comparison: Bl[i] <= Br[j]
            if Bl[i] <= Br[j]:
                A[k] = Bl[i]
                i += 1
                k += 1
            else:
                break
        A[k] = Br[j]
        k += 1

    # Copy remaining entries from Bl
    while i < len(Bl):
        A[k] = Bl[i]
        i += 1
        k += 1

    return comparisons
