import bitarray as b_array

class BitMask:

    def __init__(self, width, height):
        self.__width = width
        self.__height = height

        self.__mask = b_array.bitarray(self.__height * self.__width)
        self.__mask.setall(0)

    def is_set(self, *args):
        if len(args) == 1:
            return self.__mask[args[0]]
        elif len(args) == 2:
            return self.__mask[self.convert_pos(args[0], args[1])]
        else:
            raise AttributeError()

    def convert_offset(self, offset):
        return (offset % self.__width, offset // self.__width)

    def convert_pos(self, x, y):
        if y >= self.__height:
            y = self.__height - 1
        elif y < 0:
            y = 0

        return (x % self.__width) + (y * self.__width)


    def set(self, *args):
        if len(args) == 1:
            self.__mask[args[0]] = 1
        elif len(args) == 2:
            self.__mask[self.convert_pos(args[0], args[1])] = 1
        else:
            raise AttributeError()

    def clear(self, *args):
        if len(args) == 1:
            self.__mask[args[0]] = 0
        elif len(args) == 2:
            self.__mask[self.convert_pos(args[0], args[1])] = 0
        else:
            raise AttributeError()

    def __len__(self):
        return len(self.__mask)

    def disp(self):
        print(f'{self.__mask} : len -> {len(self.__mask)}')
