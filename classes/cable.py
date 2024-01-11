# Mercedez van der Wal & Rembrand Ruppert
# Holds the class that defines a cable segment in our case with its properties

class CableSegment():
    def __init__(self, pos_x_begin, pos_y_begin, pos_x_end, pos_y_end, price):
        self.pos_x_begin = pos_x_begin
        self.pos_y_begin = pos_y_begin
        self.pos_x_end = pos_x_end
        self.pos_y_end = pos_y_end
        self.price = price
