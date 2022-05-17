import bitarray as b_array

class BitMask:

    def __init__(self, width, height):
        self.__width = width
        self.__height = height

        self.__mask = b_array.bitarray(self.__height * self.__width)
        self.__mask.setall(0)

    def is_set(self, offset):
        return self.__mask[offset]

    def set(self, offset):
        self.__mask[offset] = 1

    def clear(self, offset):
        self.__mask[offset] = 0

    def __len__(self):
        return len(self.__mask)

    def disp(self):
        print(f'{self.__mask} : len -> {len(self.__mask)}')
