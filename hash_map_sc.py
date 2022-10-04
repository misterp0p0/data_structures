# Name: Joseph Shing
# Description: Hash Map Implementation utilizing a Dynamic Array of LinkedLists


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        """
        return self._capacity

    def put(self, key: str, value: object) -> None:

        """ Put method that adds a key/value node to the appropriate index
        in the hash table, which has a linked list at each index. If the
        given key already exists in the linked list, the value is simply
        replaced. """

        hash = self._hash_function(key)
        index = hash % self._capacity

        # if the key already exists in the LinkedList
        if self._buckets[index].contains(key):
            node = self._buckets[index].contains(key)
            node.value = value
        else:
            self._buckets[index].insert(key, value)
            self._size += 1

    # ------------------------------------------------------------------ #

    def empty_buckets(self) -> int:

        """ Empty buckets method that returns the # of empty buckets in
        the hash table. """

        empty_buckets = self._capacity

        length = self._buckets.length()
        for i in range(0, length):
            if self._buckets[i].length() > 0:
                empty_buckets -= 1

        return empty_buckets

    # ------------------------------------------------------------------ #

    def table_load(self) -> float:

        """ Table load method that returns the load factor of the hash
        table. """

        load = self._size / self._capacity

        return load 
    # ------------------------------------------------------------------ #

    def clear(self) -> None:

        """ Clear method that clears the hash table. """

        new_bucket = DynamicArray()
        for _ in range(0, self._capacity):
            new_bucket.append(LinkedList())

        self._buckets = new_bucket
        self._size = 0

    # ------------------------------------------------------------------ #

    def resize_table(self, new_capacity: int) -> None:

        """ Resize table method that resizes the hash table with the input
        capacity. The hash table is then rehashed into the new hash table
        according to the new capacity of the hash table. """

        # if the proposed capacity is invalid
        if new_capacity < 1:
            return

        # check to see if the capacity is prime    
        else:
            if self._is_prime(new_capacity):
                self._capacity = new_capacity
            else:
                new_capacity = self._next_prime(new_capacity)
                self._capacity = new_capacity
        
        # instantiate resized hash table
        new_size = 0
        new_bucket = DynamicArray()
        for _ in range(self._capacity):
            new_bucket.append(LinkedList())

        # rehash the old hash table into the new hash table
        for i in range(self._buckets.length()):
            if self._buckets[i].length() != 0:
                for node in self._buckets[i]:
                    current_key = node.key
                    current_value = node.value

                    # rehash and get new index
                    hash = self._hash_function(current_key)
                    new_index = hash % new_capacity

                    # check to see if the key is already present in the hash table
                    if new_bucket[new_index].contains(current_key):
                        node = new_bucket[new_index].contains(current_key)
                        node.value = current_value
                    else:
                        new_bucket[new_index].insert(current_key, current_value)
                        new_size += 1

        self._buckets = new_bucket
        self._size = new_size

    # ------------------------------------------------------------------ #

    def get(self, key: str) -> object:

        """ Get method that returns the value of a given key. """

        for i in range(0, self._buckets.length()):
            if self._buckets[i].contains(key):
                node = self._buckets[i].contains(key)
                return node.value
        return None

    # ------------------------------------------------------------------ #

    def contains_key(self, key: str) -> bool:

        """ Contains key method that returns True if the given key is
        present in the hash table and False otherwise. """

        for i in range(0, self._buckets.length()):
            if self._buckets[i].contains(key):
                return True
        return False

    # ------------------------------------------------------------------ #

    def remove(self, key: str) -> None:

        """ Remove method that removes a given key/value pair from the hash
        table. Nothing happens if the key is invalid. """

        for i in range(0, self._buckets.length()):
            if self._buckets[i].contains(key):
                self._buckets[i].remove(key)
                self._size -= 1

    # ------------------------------------------------------------------ #

    def get_keys_and_values(self) -> DynamicArray:

        """ Returns a tuple of the key/value pairs of the hash table. """

        answer = DynamicArray()

        for i in range(self._buckets.length()):
            for node in self._buckets[i]:
                answer.append((node.key, node.value))
        return answer

    def get_buckets(self):

        """ Helper method for returning the hash table. """

        return self._buckets

    # ------------------------------------------------------------------ #

def find_mode(da: DynamicArray) -> (DynamicArray, int):

    """ Find mode function that finds the mode of an array utilizing a
    hash map. Resizes if the load factor of the hash table exceeds 1 to
    ensure that at a best case that there is not more than 1 node at each
    index, meaning that each LinkedList at a best case would only have 1 node,
    resulting in a O(n) complexity. """

    map = HashMap()
    da_length = da.length()
    mode = 1
    answer = DynamicArray()

    for i in range(da_length):
        # compute hash and index
        hash = hash_function_1(da[i])
        index = hash % map.get_capacity()

        # add the elements of the array into the hash table
        if map.get_buckets()[index].contains(da[i]):
            node = map.get_buckets()[index].contains(da[i])
            node.value += 1

            if node.value >= mode:
                mode = node.value

        else:
            map.put(da[i], 1)

        # resize if the load factor of the hash table exceeds 1
        if map.table_load() > 1:
            map.resize_table(map.get_capacity() * 2)

    # account for multiple nodes
    for i in range(map.get_buckets().length()):
        for node in map.get_buckets()[i]:
            if node.value == mode:
                answer.append(node.key)

    return (answer, mode)

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # i = 8
    # m = HashMap(10, hash_function_1)
    # m.put("dragon", 100)
    # m.put('str' + str(i), i * 100)
    # m.put('str' + str(i), i * 200)

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         # print(f" i: {i}, Empty buckets: {m.empty_buckets()}, Table Load: {round(m.table_load(), 2)}, Size: {m.get_size()}, Capacity: {m.get_capacity()}")
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # m = HashMap(5, hash_function_1)
    # m.put("hi", 200)
    # m.put("dragon", 2000)
    # m.resize_table(10)

    # m = HashMap(5, hash_function_1)
    # print(m._is_prime(2))

    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(f"Size: {m.get_size()}, Capacity: {m.get_capacity()}, Value at key: {m.get('key1')}, Is Key in list: {m.contains_key('key1')}")
    # m.resize_table(30)
    # m.put('key2', 10)
    # print(f"Size: {m.get_size()}, Capacity: {m.get_capacity()}, Value at key: {m.get('key1')}, Is Key in list: {m.contains_key('key1')}")
    # # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(50, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 10)
    # print(f"Size: {m.get_size()}, Capacity: {m.get_capacity()}\n")

    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())

    # m.resize_table(1)
    # print(m.get_keys_and_values())

    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["grape", "apple", "melon", "peach", "grape"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )

    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
