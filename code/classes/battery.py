# Mercedez van der Wal & Rembrand Ruppert
# Holds the class that defines a battery in our case with its properties

class Battery():
    def __init__(self, position, capacity):
        self.position = position
        self.capacity = capacity
        self.used_capacity = 0
        
    def add_used_capacity(self, added_capacity):
        self.used_capacity += added_capacity
        return self.used_capacity
        
    def remove_used_capacity(self, removed_capacity):
        self.used_capacity =- removed_capacity
        
    def get_capacity(self):
        return self.used_capacity
        
    def reset_capacity(self):
        self.used_capacity = 0

    def __str__(self):
        return f"{self.position}, {self.capacity}"