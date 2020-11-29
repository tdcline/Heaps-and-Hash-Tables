# Course: CS261 - Data Structures
# Assignment: Project 5 - Your Very Own HashMap and MinHeap
# Student: Tanner Cline
# Description:


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initializes a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'HEAP ' + str(self.heap)

    def is_empty(self) -> bool:
        """
        Return True if no elements in the heap, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.heap.length() == 0

    def add(self, node: object) -> None:
        """
        The add() method adds a new object to the MinHeap in O(logN) time 
        while maintaining the heap property.

        Params: node - object - the object to be added to the MinHeap
        Return: None
        """
        
        # get last index position, append object to the end of the heap, and 
        # find parent of the last index 
        index = self.heap.length()
        self.heap.append(node)
        parent = (index - 1)//2
        
        # percolate new object up heap if less than parent until correct 
        # spot is found
        while index > 0 and self.heap[index] < self.heap[parent]:
            self.heap.swap(index, parent)
            index = parent
            parent = (index - 1)//2

    def get_min(self) -> object:
        """
        The get_min() method returns the minimum value in the heap in O(1) 
        time. This method will raise an error if the heap is empty.

        Params: NA
        Return: object - the minimum (highest priority) node in heap
        """
        
        # handle empty heap
        if self.is_empty():
            raise MinHeapException

        # return first value in underlying array
        return self.heap[0]

    def percolate_down(self, current):
        """
        The percolate_down() method percolates a node at the specified index 
        position in the heap down to its correct place out of all the elements 
        in that subtree of the MinHeap.

        Params: current - int - the index position of the node to percolate 
                                down from
        Return: None
        """
        
        # identify the indices of the end of the heap, and children of the 
        # current element
        last = self.heap.length()
        left = 2*current+1
        right = 2*current+2
        
        # percolate the current node down the tree until reached correct spot
        while left < last:
            # CASE 1: left child has lower value than right child and current 
            # = swap current with left child
            if right < last and self.heap[left] <= self.heap[right] and self.heap[left] < self.heap[current]:
                self.heap.swap(current, left)
                current = left
            # CASE 2: right child has lower value than left child and current 
            # = swap current with right child
            elif right < last and self.heap[left] > self.heap[right] and self.heap[right] < self.heap[current]:
                self.heap.swap(current, right)
                current = right
            # CASE 3: left child has lower value than current, no right child 
            # = swap current with left child
            elif self.heap[left] < self.heap[current]:
                self.heap.swap(current, left)
                current = left
            # CASE 4: current value has lower value than any child elements
            else:
                break
            # update child element indices
            left = 2*current+1
            right = 2*current+2

    def remove_min(self) -> object:
        """
        The remove_min() method removes the highest priority (lowest value) 
        element in the MinHeap in O(logN) time. This method will raise an 
        exception if the MinHeap is empty.
        
        Params: NA
        Return: object -    the value of the highest priority (lowest value) 
                            element in the MinHeap
        """
        
        # handle empty MinHeap
        if self.is_empty():
            raise MinHeapException

        # swap root and last element and pop root off underlying array
        end = self.heap.length() - 1
        self.heap.swap(0, end)
        root = self.heap.pop()
        
        # percolate root element back down to its correct spot
        self.percolate_down(0)

        # return popped off former root minimum element
        return root

    def build_heap(self, da: DynamicArray) -> None:
        """
        The build_heap() method replaces the current MinHeap with a MinHeap 
        created from the values in a specified DynamicArray in O(N) time. 

        Params: da - DynamicArray - unsorted array with which to build the heap
        Return: None
        """
        
        # create a copy of the array
        newArr = DynamicArray()
        
        for num in range(da.length()):
            newArr.append(da[num])
        
        # assign the heap to the copied array and find first non-leaf node
        self.heap = newArr
        current = newArr.length() // 2 - 1
        
        # percolate current down to the correct spot and decrement current 
        # until root is reached
        while current >= 0:
            self.percolate_down(current)
            current -= 1

# BASIC TESTING
# if __name__ == '__main__':

#     print("\nPDF - add example 1")
#     print("-------------------")
#     h = MinHeap()
#     print(h, h.is_empty())
#     for value in range(300, 200, -15):
#         h.add(value)
#         print(h)

#     print("\nPDF - add example 2")
#     print("-------------------")
#     h = MinHeap(['fish', 'bird'])
#     print(h)
#     for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
#         h.add(value)
#         print(h)


#     print("\nPDF - get_min example 1")
#     print("-----------------------")
#     h = MinHeap(['fish', 'bird'])
#     print(h)
#     print(h.get_min(), h.get_min())


#     print("\nPDF - remove_min example 1")
#     print("--------------------------")
#     h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
#     while not h.is_empty():
#         print(h, end=' ')
#         print(h.remove_min())


#     print("\nPDF - build_heap example 1")
#     print("--------------------------")
#     da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
#     h = MinHeap(['zebra', 'apple'])
#     print(h)
#     h.build_heap(da)
#     print(h)
#     da.set_at_index(0, 500)
#     print(da)
#     print(h)