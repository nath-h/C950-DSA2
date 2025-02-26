class HashMap:
    #Constructor with no required parameters. Creates an empty 2d list with a size of 41. If we used 40, printing
    #is out of order so we use 41 for clarity.
    def __init__(self):
        self.size = 41
        self.map = [[] for _ in range(self.size)]
    #Takes an input, modulos it by the size of the hashmap and returns the value. Example: 1 % 41 key would be 1.
    def get_hash_value(self, key):
        hash_value = key % self.size
        return hash_value
    #Takes a key and maps a value to it
    def add(self, key, value):
        key_hash = self.get_hash_value(key)
        key_value= [key, value]
        #If hash doesn't exist, create a new key and value bucket
        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            #If key already exists, update the new value associated with it
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
        self.map[key_hash].append(key_value)
        return True
    #Takes the key and returns the key_value if not None
    def get(self, key):
        key_hash = self.get_hash_value(key)

        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None
    #Takes a key and deletes any key, value pair associated with the key
    def delete(self, key):
        key_hash = self.get_hash_value(key)

        if self.map[key_hash] is None:
            return False
        for i in range (0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True
    #Below are print functions on the hashmap
    def print(self):
        for item in self.map:
            if item is not None:
                for pair in item:
                 print(str(pair[1]))

    def __str__(self):
        return '\n'.join([f" {str(value)}" for value in self.map])
