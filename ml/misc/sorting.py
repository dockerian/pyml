"""
# misc/sorting.py

  see:
  - https://en.wikipedia.org/wiki/Sorting_algorithm
  - https://www.bigocheatsheet.com/
"""


def bubble_sort(a: list):
    """
    Bubble sorting a list. Big-O: n^2 (average/worst) time; 1 on space.
    """
    siz = len(a)
    for i in range(siz):
        swapped = False
        top = siz - i - 1
        for j in range(top):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def heap_sort(arr: list):
    """
    Heap sorting a list. Big-O: O(n log n).

    @see https://www.geeksforgeeks.org/heap-sort/
    """
    def heapify(sub: list, rdx: int, siz: int):
        """
        Heapifying range between rdx and size ([rdx:siz]).

        @param sub: a slice of list.
        @param rdx: root/parent index to start.
        @param siz: size of heap.
        """
        largest = ndx = rdx  # assuming the root is the largest
        while ndx < siz:
            l_index = 2 * ndx + 1  # child index at left = 2*i + 1
            r_index = 2 * ndx + 2  # child index at right = 2*i + 2
            # reset largest index if left child exists and is greater than root.
            if l_index < siz and sub[ndx] < sub[l_index]:
                largest = l_index
            # check if right child is greater than the value at the largest index.
            if r_index < siz and sub[largest] < sub[r_index]:
                largest = r_index
            # change root, if needed
            if largest != ndx:
                sub[ndx], sub[largest] = sub[largest], sub[ndx]  # swap
                ndx = largest  # heapify the root.
                continue
            return
        pass

    n = len(arr)
    # build a max heap.
    parent = n // 2 - 1  # the last parent (that can have children)
    for i in range(parent, -1, -1):
        heapify(arr, i, n)

    # extract elements one by one.
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, 0, i)

    return arr


def heap_sift_down(a: list, start: int, end: int):
    """
    Heap sift-down treats the entire input array as a full but "broken" heap
    and "repairs" it starting from the last non-trivial sub-heap (that is,
    the last parent node). Big-O: O(n) time complexity.
    """
    idx_root = start
    idx_child = 2 * idx_root + 1  # left child of root

    while idx_child <= end:  # while the root has at least one child
        idx_swap = idx_root  # keep track of child to swap with
        if a[idx_swap] < a[idx_child]:
            idx_swap = idx_child
        if idx_child+1 <= end and a[idx_swap] < a[idx_child+1]:  # check right child
            idx_swap = idx_child + 1
        if idx_swap == idx_root:
            # the root holds the largest element.
            # done, since assuming the heaps rooted at the children are valid.
            return
        a[idx_root], a[idx_swap] = a[idx_swap], a[idx_root]
        idx_child = 2 * idx_swap + 1  # left child of new root
        idx_root = idx_swap
    pass


def heap_sift_up(a: list, start: int, end: int):
    """
    Heap sift-up can be visualized as starting with an empty heap and
    successively inserting elements. Big-O: O(n log n).

    @param start: represents the limit of how far the heap to sift up to.
    @param end: index of the node to sift up.
    """
    size = len(a)
    if start < 0 or start >= size:
        raise ValueError('start index must be in range(0, %d)' % size)
    if end < 1 or end >= size:
        raise ValueError('end index must be in range(1, %d)' % size)
    child = end
    while child > start:
        parent = (child - 1) // 2  # get parent of the child
        if a[parent] < a[child]:  # out of max-heap order
            a[parent], a[child] = a[child], a[parent]
            child == parent  # continue sifting up the parent.
            continue
        return
    pass


def heapify_by_sift_down(a: list):
    count = len(a)
    start = (count - 1) // 2  # start from the parent of the last item
    while start >= 0:
        # sift down the node at start index to proper place so that
        # all nodes below the start index are in heap order.
        heap_sift_down(a, start, count - 1)
        start = start - 1  # go to the next parent node
    # after sifting down the root, all nodes/elements are in heap order.
    pass


def heapify_by_sift_up(a: list):
    count = len(a)
    end = 1  # start from the first (left) child of the root
    while end < count:
        # sift up the node at end index to proper place such that
        # all nodes above the end index are in heap order.
        heap_sift_up(a, 0, end)
        end = end + 1
    # after sifting up the last node, all nodes are in heap order.
    pass


def heapsort(a: list, heapify_func=heapify_by_sift_down):
    """
    Use heapify function to sort a list.

    @see https://en.wikipedia.org/wiki/Heapsort
    """
    count = len(a)
    # build the heap in array a so that largest value is at the root.
    heapify_func(a)

    # the following loop maintains the invariants that a[0:end] is a heap
    # and every element beyond end is greater than everything before it,
    # so that a[end:count] is in sorted order.
    end = count - 1
    while end > 0:
        # a[0] is the root and largest value - moves it in front of the sorted elements.
        a[end], a[0] = a[0], a[end]
        end = end - 1  # reduce heap size by one
        # restore the heap property after the swap ruined it.
        heap_sift_down(a, 0, end)

    return a


def insertion_sort(arr: list):
    """
    Insertion sorting a list. Big-O: n^2 (average/worst) time; 1 on space.
    """
    for ndx in range(1, len(arr)):
        pos = ndx
        val = arr[ndx]
        while pos > 0 and arr[pos-1] > val:
            arr[pos] = arr[pos-1]
            pos = pos-1
        arr[pos] = val
    return arr


def selection_bingo_sort(a: list):
    """
    Selection bingo sort does one pass for each value (not item): after an
    initial pass to find the biggest value, the next passes can move every item
    with that value to its final location while finding the next value.
    As a variant of selection sort, items are ordered by repeatedly looking
    through the remaining items to find the greatest value and moving all items
    with that value to their final location.

    @see https://en.wikipedia.org/wiki/Selection_sort#Variants
    """
    max = len(a) - 1

    next_value = a[max]  # holding next max value
    for i in range(max-1, -1, -1):
        if a[i] > next_value:
            next_value = a[i]  # setting to the max value
    while max > 0 and a[max] == next_value:
        max = max - 1  # shifting max index

    while max > 0:
        next_max_value = next_value
        next_value = a[max]
        for i in range(max-1, -1, -1):
            if a[i] == next_max_value:
                a[i], a[max] = a[max], a[i]
                max = max - 1
            elif a[i] > next_value:
                next_value = a[i]
        while max > 0 and a[max] == next_value:
            max = max - 1
    return a


def selection_sort(a: list) -> list:
    """
    Selection sorting a list. Big-O: n^2 (average/worst) time; 1 on space.
    """
    siz = len(a)
    for i in range(siz):
        x_min = i
        for j in range(i+1, siz):
            if a[j] < a[x_min]:
                x_min = j
        if x_min > i:
            a[i], a[x_min] = a[x_min], a[i]
    return a
