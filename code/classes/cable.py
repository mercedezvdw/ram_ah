# Mercedez van der Wal & Rembrand Ruppert
# Holds the class that defines a cable segment in our case with its properties

class CableSegment():
    def __init__(self, pos_begin, pos_end, price):
        self.pos_begin = pos_begin
        self.pos_end = pos_end
        self.price = price
