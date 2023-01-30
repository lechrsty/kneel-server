class Order():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, metal_id, size_id, style_id, timestamp):
        self.id = id
        self.metal_id = metal_id
        self.size_id = size_id
        self.style_id = style_id
        self.timestamp = timestamp
