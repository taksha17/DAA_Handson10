# Author Name : taksha Sachin Thosani
# UTA ID : 1002086312
# Net ID : txt6312


class Node:
    # """A node in a doubly linked list, used for chaining in the hash table."""
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class DoublyLinkedList:
    # """A simple doubly linked list for managing collisions in the hash table."""
    def __init__(self):
        self.head = None
        self.tail = None

    def insert(self, key, value):
        # """Inserts a new node with the given key and value at the end of the list."""
        new_node = Node(key, value)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def find(self, key):
        # """Finds and returns the node with the given key, if it exists."""
        current = self.head
        while current:
            if current.key == key:
                return current
            current = current.next
        return None

    def remove(self, key):
        # """Removes the node with the given key from the list."""
        current = self.find(key)
        if current:
            if current.prev:
                current.prev.next = current.next
            else:
                self.head = current.next
            if current.next:
                current.next.prev = current.prev
            else:
                self.tail = current.prev
            return True
        return False

class HashTable:
    def __init__(self, initial_capacity=8, hash_func=None):
        self.capacity = initial_capacity
        self.size = 0
        self.buckets = [None] * self.capacity
        self.load_factor = 0.75
        self.hash_func = hash_func if hash_func is not None else self.default_hash

    def hash(self, key):
        return self.hash_func(key, self.capacity)

    def default_hash(self, key, capacity):
        return (key * 2654435761 % (2**32)) % capacity
    
    def insert(self, key, value):
        # """Inserts a new key-value pair into the hash table."""
        if self.size / self.capacity >= self.load_factor:
            self._resize(2 * self.capacity)

        index = self.hash(key)
        if not self.buckets[index]:
            self.buckets[index] = DoublyLinkedList()
        if not self.buckets[index].find(key):
            self.buckets[index].insert(key, value)
            self.size += 1

    def remove(self, key):
        # """Removes the value associated with the key."""
        index = self.hash(key)
        if self.buckets[index] and self.buckets[index].remove(key):
            self.size -= 1
            if self.size <= self.capacity / 4:
                self._resize(self.capacity // 2)

    def get(self, key):
        # """Retrieves the value associated with the key."""
        index = self.hash(key)
        bucket = self.buckets[index]
        if bucket:
            node = bucket.find(key)
            if node:
                return node.value
        return None

    def _resize(self, new_capacity):
        # """Resizes the table to the new capacity and rehashes all keys."""
        new_table = HashTable(new_capacity)
        for bucket in self.buckets:
            if bucket:
                current = bucket.head
                while current:
                    new_table.insert(current.key, current.value)
                    current = current.next
        self.capacity = new_capacity
        self.buckets = new_table.buckets

hash_table = HashTable()
hash_table.insert(1, 'A')
hash_table.insert(2, 'B')
hash_table.insert(3, 'C')

print(hash_table.get(1))  
print(hash_table.get(2))  
print(hash_table.get(3))  

hash_table.remove(2)
print(hash_table.get(2))  