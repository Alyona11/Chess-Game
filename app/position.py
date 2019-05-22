# Клас для опису позиції клітинки
class Position(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, another):
        return (self.x, self.y) == (another.x, another.y)
