import struct

class BitMask:

    def __init__(self, width, height):
        self.__width = width
        self.__height = height

        nb_bit = self.__height * self.__width
        self.__mask = b'\x00' * ((nb_bit // 8) + 1)

    def is_set(self, offset):
        byte_id = offset // 8
        bit_id = offset % 8

        return self.__mask[byte_id] & (1 << bit_id)

    def set(self, offset):
        byte_id = offset // 8
        bit_id = offset % 8

        current = self.__mask[byte_id]
        self.__mask = self.__mask[:byte_id] + struct.pack("B", current | (1 << bit_id)) + self.__mask[byte_id+1:]

    def clear(self, offset):
        byte_id = offset // 8
        bit_id = offset % 8

        print(self.__mask, "--------")
        current = self.__mask[byte_id]
        self.__mask = self.__mask[:byte_id] + struct.pack("B", current & ~(1 << bit_id)) + self.__mask[byte_id+1:]

    def disp(self):
        print(self.__mask)
