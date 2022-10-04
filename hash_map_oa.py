# Name: Joseph Shing
# Description: Hash Map Implementation utilizing a Dynamic Array and HashEntry objects


from ds_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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

    # ------------------------------------------------------------------ #
    # ------------------------------------------------------------------ #
    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:

        """ Put method that adds a key/value pair into the hash map. The
        key/value pair is added as a HashEntry object. If the key already
        exists within the hash table, the value will be replaced. The hash
        table will auto resize when attempting to add in a node when the load
        factor is equal to or greater than 0.5. """

        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        hash = self._hash_function(key)
        index = hash % self._capacity
        initial_index = index
        j = 1

        # if the key is already in the hash table
        if self._buckets[index] is not None and self._buckets[index].key == key:
            if self._buckets[index].is_tombstone is True:
                self._buckets[index].value = value
                self._size += 1
                self._buckets[index].is_tombstone = False
            self._buckets[index].value = value

        # if the index is empty
        elif self._buckets[index] is None:
            entry = HashEntry(key, value)
            self._buckets[index] = entry
            self._size += 1

        # if the index is occupied
        else:
            # quadratic probing for the next available index
            while self._buckets[index] is not None and self._buckets[index].key != key:
                if self._buckets[index].is_tombstone is False:
                    index = (initial_index + j ** 2) % self._capacity
                    j += 1

            if self._buckets[index] is not None and self._buckets[index].key == key:
                if self._buckets[index].is_tombstone is True:
                    self._buckets[index].value = value
                    self._size += 1
                    self._buckets[index].is_tombstone = False
                self._buckets[index].value = value
            else:
                self._buckets[index] = HashEntry(key, value)
                self._size += 1

    # ------------------------------------------------------------------ #

    def table_load(self) -> float:

        """ Table load method that returns the table load of the hash table.
        The table load is the # of elements / # of buckets. """

        load_factor = self._size / self._capacity
        return load_factor

    # ------------------------------------------------------------------ #

    def empty_buckets(self) -> int:

        """ Empty buckets method that returns the # of empty buckets in the
        hash table. """

        empty_buckets = 0
        for i in range(self._capacity):
            if self._buckets[i] is None:
                empty_buckets += 1

        return empty_buckets

    # ------------------------------------------------------------------ #

    def resize_table(self, new_capacity: int) -> None:

        """ Resize table method that resizes the hash table if the load
        factor is equal to or above 0.5. After resizing, the method will
        rehash the exisiting elements into the newly resized hash table.
        The hash table will only be resized if the input capacity is valid.
        The input capacity is also processed for prime validity, and if that
        is not true, the capacity will be incremented to next highest prime
        number. """

        # if the capacity is greater than the current size
        if new_capacity < self._size:
            return

        # checks to see if the input capacity is a prime number
        if self._is_prime(new_capacity) is not True:
            self._capacity = self._next_prime(new_capacity)

        else:
            self._capacity = new_capacity

        # instantiate new hash table with greater size
        new_hash_table = DynamicArray()
        for _ in range(self._capacity):
            new_hash_table.append(None)

        # create a copy of the current hash table (self._buckets)
        original_hash_table = DynamicArray()
        for i in range(self._buckets.length()):
            original_hash_table.append(self._buckets[i])

        # reset variables for re-hashing
        self._size = 0
        self._buckets = new_hash_table

        # rehash elements into new hash table accounting for load
        # factor and prime validity per entry
        for i in range(original_hash_table.length()):
            if original_hash_table[i] is not None:
                key = original_hash_table[i].key
                value = original_hash_table[i].value 
                self.put(key, value)

    # ------------------------------------------------------------------ #

    def get(self, key: str) -> object:

        """ Get method that returns the value of a given key. Returns
        None if the key is invalid. """

        for i in range(self._capacity):
            if self._buckets[i] is not None and self._buckets[i].key == key:
                if self._buckets[i].is_tombstone is False:
                    return self._buckets[i].value 

        return None

    # ------------------------------------------------------------------ #   
    def contains_key(self, key: str) -> bool:

        """ Contains key method that returns True if the hash table contains
        the input key and False otherwise. """

        for i in range(self._capacity):
            if self._buckets[i] is not None and self._buckets[i].key == key:
                return True

        return False

    # ------------------------------------------------------------------ #   

    def remove(self, key: str) -> None:

        """ Remove method that removes a key/value pair from the hash table.
        An element is "removed" if the tombstone status of the HashEntry
        object is True. """

        for i in range(self._capacity):

            if self._buckets[i] is not None and self._buckets[i].key == key:
                if self._buckets[i].is_tombstone is False:
                    self._buckets[i].is_tombstone = True
                    self._size -= 1

    # ------------------------------------------------------------------ #   

    def clear(self) -> None:

        """ Clear method that clears the Hash Table. """

        length = self._capacity
        new_bucket = DynamicArray()

        for _ in range(length):
            new_bucket.append(None)

        self._buckets = new_bucket
        self._size = 0

    # ------------------------------------------------------------------ #   

    def get_keys_and_values(self) -> DynamicArray:

        """ Get keys and values method that returns the key/value pairs of
        the hash table. """

        answer = DynamicArray()

        for i in range(self._capacity):
            if self._buckets[i] is not None and self._buckets[i].is_tombstone is False:
                answer.append((self._buckets[i].key, self._buckets[i].value))

        return answer

# ------------------- BASIC TESTING ---------------------------------------- #

# if __name__ == "__main__":

#     print("\nPDF - put example 1")
#     print("-------------------")
#     m = HashMap(53, hash_function_1)
#     for i in range(150):
#         m.put('str' + str(i), i * 100)
#         if i % 25 == 24:
#             print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    

#     print("\nPDF - put example 2")
#     print("-------------------")
#     m = HashMap(41, hash_function_2)
#     for i in range(50):
#         m.put('str' + str(i // 3), i * 100)
#         # print(m.get_size())
#         # print(i, 'str' + str(i // 3))
#         # print('\n')
#         # print(m)
#         if i % 10 == 9:
#             print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

#     print("\nPDF - table_load example 1")
#     print("--------------------------")
#     m = HashMap(101, hash_function_1)
#     print(round(m.table_load(), 2))
#     m.put('key1', 10)
#     print(round(m.table_load(), 2))
#     m.put('key2', 20)
#     print(round(m.table_load(), 2))
#     m.put('key1', 30)
#     print(round(m.table_load(), 2))

#     print("\nPDF - table_load example 2")
#     print("--------------------------")
#     m = HashMap(53, hash_function_1)
#     for i in range(50):
#         m.put('key' + str(i), i * 100)
#         if i % 10 == 0:
#             print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

#     print("\nPDF - empty_buckets example 1")
#     print("-----------------------------")
#     m = HashMap(101, hash_function_1)
#     print(m.empty_buckets(), m.get_size(), m.get_capacity())
#     m.put('key1', 10)
#     print(m.empty_buckets(), m.get_size(), m.get_capacity())
#     m.put('key2', 20)
#     print(m.empty_buckets(), m.get_size(), m.get_capacity())
#     m.put('key1', 30)
#     print(m.empty_buckets(), m.get_size(), m.get_capacity())
#     m.put('key4', 40)
#     print(m.empty_buckets(), m.get_size(), m.get_capacity())

#     print("\nPDF - empty_buckets example 2")
#     print("-----------------------------")
#     m = HashMap(53, hash_function_1)
#     for i in range(150):
#         m.put('key' + str(i), i * 100)
#         if i % 30 == 0:
#             print(m.empty_buckets(), m.get_size(), m.get_capacity())

#     print("\nPDF - resize example 1")
#     print("----------------------")
#     m = HashMap(23, hash_function_1)
#     m.put('key1', 10)
#     print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
#     m.resize_table(30)
#     print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))


#     print("\nPDF - resize example 2")
#     print("----------------------")
#     m = HashMap(79, hash_function_2)
#     keys = [i for i in range(1, 1000, 15)]
#     for key in keys:
#         m.put(str(key), key * 42)
#     print(m.get_size(), m.get_capacity(), round(m.table_load(),2))
#     # print(f"Original m: {m}")


#     for capacity in range(111, 1000, 117):
#         m.resize_table(capacity)

#         if m.table_load() > 0.5:
#             print(capacity)
#             print(f"Check that the load factor is acceptable after the call to resize_table().\n"
#                   f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

#         m.put('some key', 'some value')
#         result = m.contains_key('some key')
#         m.remove('some key')

#         for key in keys:
#             # all inserted keys must be present
#             result &= m.contains_key(str(key))
#             # NOT inserted keys must be absent
#             result &= not m.contains_key(str(key + 1))
#         print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

#     print("\nPDF - get example 1")
#     print("-------------------")
#     m = HashMap(31, hash_function_1)
#     print(m.get('key'))
#     m.put('key1', 10)
#     print(m.get('key1'))

#     print("\nPDF - get example 2")
#     print("-------------------")
#     m = HashMap(151, hash_function_2)
#     for i in range(200, 300, 7):
#         m.put(str(i), i * 10)
#     print(m.get_size(), m.get_capacity())
#     for i in range(200, 300, 21):
#         print(i, m.get(str(i)), m.get(str(i)) == i * 10)
#         print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

#     print("\nPDF - contains_key example 1")
#     print("----------------------------")
#     m = HashMap(11, hash_function_1)
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
#     m = HashMap(79, hash_function_2)
#     keys = [i for i in range(1, 1000, 20)]
#     for key in keys:
#         m.put(str(key), key * 42)
#     print(m.get_size(), m.get_capacity())
#     result = True
#     for key in keys:
#         # all inserted keys must be present
#         result &= m.contains_key(str(key))
#         # NOT inserted keys must be absent
#         result &= not m.contains_key(str(key + 1))
#     print(result)

#     print("\nPDF - remove example 1")
#     print("----------------------")
#     m = HashMap(53, hash_function_1)
#     print(m.get('key1'))
#     m.put('key1', 10)
#     print(m.get('key1'))
#     m.remove('key1')
#     print(m.get('key1'))
#     m.remove('key4')

#     print("\nPDF - clear example 1")
#     print("---------------------")
#     m = HashMap(101, hash_function_1)
#     print(m.get_size(), m.get_capacity())
#     m.put('key1', 10)
#     m.put('key2', 20)
#     m.put('key1', 30)
#     print(m.get_size(), m.get_capacity())
#     m.clear()
#     print(m.get_size(), m.get_capacity())

#     print("\nPDF - clear example 2")
#     print("---------------------")
#     m = HashMap(53, hash_function_1)
#     print(m.get_size(), m.get_capacity())
#     m.put('key1', 10)
#     print(m.get_size(), m.get_capacity())
#     m.put('key2', 20)
#     print(m.get_size(), m.get_capacity())
#     m.resize_table(100)
#     print(m.get_size(), m.get_capacity())
#     m.clear()
#     print(m.get_size(), m.get_capacity())

#     print("\nPDF - get_keys_and_values example 1")
#     print("------------------------")
#     m = HashMap(11, hash_function_2)
#     for i in range(1, 6):
#         m.put(str(i), str(i * 10))
#     print(m.get_keys_and_values())

#     m.resize_table(2)
#     print(m.get_keys_and_values())

#     m.put('20', '200')
#     m.remove('1')
#     m.resize_table(12)
#     print(m.get_keys_and_values())
