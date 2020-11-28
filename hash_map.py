# Course: CS261 - Data Structures
# Assignment: Project 5 - Your Very Own HashMap and MinHeap
# Student: Tanner Cline
# Description:  Create a hash table with a HashMap class implemented with a 
#               Dynamic Array and Linked List for chaining collisions.


# Import pre-written DynamicArray and LinkedList classes
from a5_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        The clear() method clears the underlying array of all key-value 
        pairs by creating a new empty array of the same capacity.

        Params: NA
        Return: None
        """
        
        # create new empty array
        newArr = DynamicArray()
        
        # add in empty Linked Lists
        for _ in range(self.capacity):
            newArr.append(LinkedList())
        
        # reassign new array to hash table and reset size
        self.buckets = newArr
        self.size = 0

    def get(self, key: str) -> object:
        """
        The get() method returns the value associated with the specified key.

        Params: key - string - the key to search for in the hash table
        Return: object - the value associated with the specified key
                None - if the key is not in the hash table
        """
        
        # search for the key in the hash table
        if self.contains_key(key):
            # calculate hash index and get node at that index
            hash_i = self.hash_function(key) % self.capacity
            node = self.buckets[hash_i].contains(key)
            
            # return node value associated with the key
            if node is not None:
                return node.value
        
        # if key is not in the hash table
        return None

    def put(self, key: str, value: object) -> None:
        """
        The put() method updates the specified key-value if the key already 
        exists in the hash table. The method adds the key-value pair to the 
        table if it does not exist already.

        Params: key - string - the key to update or insert in the hash table
                value - object - the value to update or insert in the hash table
        Return: None
        """
        
        # calculate the hash index of the specified key
        hash_i = self.hash_function(key) % self.capacity
        
        # search to see if the key already exists in the hash table
        if self.contains_key(key):
            # iterate through the linked list
            for link in self.buckets[hash_i]:
                # if key matches update value
                if link.key == key:
                    link.value = value
        # if key doesn't exists - insert into the hash table and update size
        else:
            self.buckets[hash_i].insert(key, value)
            self.size += 1

    def remove(self, key: str) -> None:
        """
        The remove() method searches for and removes the specified key and 
        its value if it exists within the hash table.

        Params: key - string - the key to search for and remove
        Return: None
        """
        
        # check if key exists within the hash map
        if self.contains_key(key):
            # calculate hash index 
            hash_i = self.hash_function(key) % self.capacity
            # access array hash index linked list and use remove method
            self.buckets[hash_i].remove(key)
            # update size if removed
            self.size -= 1

    def contains_key(self, key: str) -> bool:
        """
        The contains_key() method checks whether a specified key exists 
        within the hash table.

        Params: key - string - the key to search the hash table for
        Return: True - bool - if the key is found within the hash table
                False - bool - if the key is not found within the hash table
        """
        
        # calculate hash index
        hash_i = self.hash_function(key) % self.capacity
        
        # use linked list contains() method to check for key
        # return True if found
        if self.buckets[hash_i].contains(key):
            return True
        
        # return False if not found
        return False

    def empty_buckets(self) -> int:
        """
        The empty_buckets() method calculates the number of unused buckets 
        within the hash table by checking the lengths of the underlying linked 
        lists within the underlying dynamic array.

        Params: NA
        Return: int - the number of empty hash table slots
        """
        
        # set empty slot counter
        empties = 0
        
        # search all the slots in the hash tables
        for i in range(self.capacity):
            # add to empties counter if underlying Linked List is empty
            if self.buckets[i].length() == 0:
                empties += 1
        
        # return the counter
        return empties

    def table_load(self) -> float:
        """
        The table_load() method calculates the current load of the hash table.

        Params: NA
        Return: float - the current load of the hash table
        """
        
        # use current capacity and current size key data fields
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        The resize_table() method updates the hash table capacity to the 
        specified number and rehashes all current entries. The new capacity 
        must be greater than or equal to 1.

        Params: new_capacity - int - the desired new capacity of the hash table
        Return: None
        """
        
        # handle invalid capacity size
        if new_capacity < 1:
            return None
        
        # store underlying dynamic array and current capacity
        copyArr = self.buckets
        old_capacity = self.capacity
        # assign new empty dynamic array, reset size, and set new capacity
        self.buckets = DynamicArray()
        self.capacity = new_capacity
        self.size = 0
        
        # add in empty Linked Lists correlating to new capacity
        for _ in range(new_capacity):
            self.buckets.append(LinkedList())
        
        # iterate through stored dynamic array and capacity to rehash 
        # key-value pairs
        for i in range(old_capacity):
            # iterate through linked lists, rehashing key-value pairs into 
            # new array
            for link in copyArr[i]:
                self.put(link.key, link.value)

    def get_keys(self) -> DynamicArray:
        """
        The get_keys() method creates a dynamic array of all the keys 
        currently in the hash table.

        Params: NA
        Return: object -    DynamicArray instance of all the keys in the 
                            hash table
        """
        
        # establish new dynamic array
        keyArray = DynamicArray()
        
        # iterate through the hash table entries
        for i in range(self.capacity):
            # iterate through the underlying linked lists
            for link in self.buckets[i]:
                # add each key to the new array
                keyArray.append(link.key)
        
        # return the array
        return keyArray


# BASIC TESTING
# if __name__ == "__main__":

#     print("\nPDF - empty_buckets example 1")
#     print("-----------------------------")
#     m = HashMap(100, hash_function_1)
#     print(m.empty_buckets(), m.size, m.capacity)
#     m.put('key1', 10)
#     print(m.empty_buckets(), m.size, m.capacity)
#     m.put('key2', 20)
#     print(m.empty_buckets(), m.size, m.capacity)
#     m.put('key1', 30)
#     print(m.empty_buckets(), m.size, m.capacity)
#     m.put('key4', 40)
#     print(m.empty_buckets(), m.size, m.capacity)


#     print("\nPDF - empty_buckets example 2")
#     print("-----------------------------")
#     m = HashMap(50, hash_function_1)
#     for i in range(150):
#         m.put('key' + str(i), i * 100)
#         if i % 30 == 0:
#             print(m.empty_buckets(), m.size, m.capacity)


#     print("\nPDF - table_load example 1")
#     print("--------------------------")
#     m = HashMap(100, hash_function_1)
#     print(m.table_load())
#     m.put('key1', 10)
#     print(m.table_load())
#     m.put('key2', 20)
#     print(m.table_load())
#     m.put('key1', 30)
#     print(m.table_load())


#     print("\nPDF - table_load example 2")
#     print("--------------------------")
#     m = HashMap(50, hash_function_1)
#     for i in range(50):
#         m.put('key' + str(i), i * 100)
#         if i % 10 == 0:
#             print(m.table_load(), m.size, m.capacity)

#     print("\nPDF - clear example 1")
#     print("---------------------")
#     m = HashMap(100, hash_function_1)
#     print(m.size, m.capacity)
#     m.put('key1', 10)
#     m.put('key2', 20)
#     m.put('key1', 30)
#     print(m.size, m.capacity)
#     m.clear()
#     print(m.size, m.capacity)


#     print("\nPDF - clear example 2")
#     print("---------------------")
#     m = HashMap(50, hash_function_1)
#     print(m.size, m.capacity)
#     m.put('key1', 10)
#     print(m.size, m.capacity)
#     m.put('key2', 20)
#     print(m.size, m.capacity)
#     m.resize_table(100)
#     print(m.size, m.capacity)
#     m.clear()
#     print(m.size, m.capacity)


#     print("\nPDF - put example 1")
#     print("-------------------")
#     m = HashMap(50, hash_function_1)
#     for i in range(150):
#         m.put('str' + str(i), i * 100)
#         if i % 25 == 24:
#             print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


#     print("\nPDF - put example 2")
#     print("-------------------")
#     m = HashMap(40, hash_function_2)
#     for i in range(50):
#         m.put('str' + str(i // 3), i * 100)
#         if i % 10 == 9:
#             print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


#     print("\nPDF - contains_key example 1")
#     print("----------------------------")
#     m = HashMap(10, hash_function_1)
#     print(m.contains_key('key1'))
#     m.put('key1', 10)
#     m.put('key2', 20)
#     m.put('key3', 30)
#     print(m.contains_key('key1'))
#     print(m.contains_key('key4'))
#     print(m.contains_key('key2'))
#     print(m.contains_key('key3'))
#     m.remove('key3')
#     print(m.contains_key('key3'))


#     print("\nPDF - contains_key example 2")
#     print("----------------------------")
#     m = HashMap(75, hash_function_2)
#     keys = [i for i in range(1, 1000, 20)]
#     for key in keys:
#         m.put(str(key), key * 42)
#     print(m.size, m.capacity)
#     result = True
#     for key in keys:
#         # all inserted keys must be present
#         result &= m.contains_key(str(key))
#         # NOT inserted keys must be absent
#         result &= not m.contains_key(str(key + 1))
#     print(result)


#     print("\nPDF - get example 1")
#     print("-------------------")
#     m = HashMap(30, hash_function_1)
#     print(m.get('key'))
#     m.put('key1', 10)
#     print(m.get('key1'))


#     print("\nPDF - get example 2")
#     print("-------------------")
#     m = HashMap(150, hash_function_2)
#     for i in range(200, 300, 7):
#         m.put(str(i), i * 10)
#     print(m.size, m.capacity)
#     for i in range(200, 300, 21):
#         print(i, m.get(str(i)), m.get(str(i)) == i * 10)
#         print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


#     print("\nPDF - remove example 1")
#     print("----------------------")
#     m = HashMap(50, hash_function_1)
#     print(m.get('key1'))
#     m.put('key1', 10)
#     print(m.get('key1'))
#     m.remove('key1')
#     print(m.get('key1'))
#     m.remove('key4')


#     print("\nPDF - resize example 1")
#     print("----------------------")
#     m = HashMap(20, hash_function_1)
#     m.put('key1', 10)
#     print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
#     m.resize_table(30)
#     print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


#     print("\nPDF - resize example 2")
#     print("----------------------")
#     m = HashMap(75, hash_function_2)
#     keys = [i for i in range(1, 1000, 13)]
#     for key in keys:
#         m.put(str(key), key * 42)
#     print(m.size, m.capacity)

#     for capacity in range(111, 1000, 117):
#         m.resize_table(capacity)

#         m.put('some key', 'some value')
#         result = m.contains_key('some key')
#         m.remove('some key')

#         for key in keys:
#             result &= m.contains_key(str(key))
#             result &= not m.contains_key(str(key + 1))
#         print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


#     print("\nPDF - get_keys example 1")
#     print("------------------------")
#     m = HashMap(10, hash_function_2)
#     for i in range(100, 200, 10):
#         m.put(str(i), str(i * 10))
#     print(m.get_keys())

#     m.resize_table(1)
#     print(m.get_keys())

#     m.put('200', '2000')
#     m.remove('100')
#     m.resize_table(2)
#     print(m.get_keys())