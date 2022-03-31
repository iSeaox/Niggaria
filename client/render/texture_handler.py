import pygame
import json
import os
import time

class TextureHandler:

    def __init__(self, logger):
        self.__textures_folder = r'./textures/'
        self.loaded = {}
        self.logger = logger

    def load_textures(self, part="all"):
        path = self.__textures_folder
        if(part != "all"):
            for folder in part.split("."):
                path += folder+"/"

        content = os.listdir(path)
        for file in content:
            if(os.path.isdir(path + file + "/")):
                self.load_textures(part+"."+file)

            elif(file.split(".")[1] == "json"):
                textures_info = {}
                with open(path + file, "r") as json_file:
                    textures_info = json.load(json_file)
                    self.__load(textures_info)

    def __load(self, info):
        t_type = info["type"].split("/")
        raw_image = pygame.image.load(info["file"]).convert_alpha()
        if(t_type[0] == "simple"):
            self.loaded[info["name"]] = raw_image.copy()
            self.logger.log(info["name"] + "loaded", subject="load")
        elif(t_type[0] == "strip"):
            if(t_type[1] == "textures"):
                strip = []
                cursor = 0
                while(cursor < raw_image.get_width()):
                    strip.append(raw_image.subsurface(pygame.Rect((cursor, 0, info["format"]["width"], info["format"]["height"]))).copy())
                    self.loaded[info["name"]] = strip
                    self.logger.log(info["name"] + "loaded", subject="load")
                    cursor += info["format"]["width"]

            elif(t_type[1] == "charset"):
                sequence = info["charset"]["sequence"]
                print(sequence)
                strip = {}
                cursor = 0
                it = 0
                while(cursor < len(sequence * info["format"]["width"])):
                    strip[sequence[it]] = self.resize(raw_image.subsurface(pygame.Rect((cursor, 0, info["format"]["width"], info["format"]["height"]))).copy(), size_coef=2)
                    self.loaded[info["name"]] = strip
                    self.logger.log(info["name"] + "loaded", subject="load")
                    cursor += info["format"]["width"]
                    it += 1


    def get_texture(self, path, size_coef = 1):
        if(type(size_coef) != int):
            raise TypeError("size_coef has to be an integer")

        if((path, size_coef) in self.loaded.keys()):
            return self.loaded[(path, size_coef)]
        else:
            raw_image = pygame.image.load(path).convert_alpha()
            final_image = self.resize(raw_image, size_coef)
            self.loaded[(path, size_coef)] = final_image
            return final_image

    def resize(self, surface, size_coef):
        return pygame.transform.scale(surface, (surface.get_width() * size_coef, surface.get_height() * size_coef))
        # if(size_coef == 1):
        #     return surface
        #
        # final_textures = pygame.Surface((surface.get_width() * size_coef, surface.get_height() * size_coef))
        #
        # rt_buffer = surface.get_buffer()
        #
        # temp_bytes = b''
        # current_line = b''
        # pixel_index = 0
        # while(pixel_index < rt_buffer.length / 4):
        #     if(pixel_index % surface.get_width() == 0):
        #         temp_bytes += current_line * size_coef
        #         current_line = b''
        #
        #     current_pixel = rt_buffer.raw[(pixel_index * 4):(pixel_index * 4) + 4]
        #     current_line += current_pixel * size_coef
        #     pixel_index += 1
        #
        # final_textures.get_buffer().write(temp_bytes)
        # return final_textures
