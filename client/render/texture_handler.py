import pygame
import json
import os


class TextureHandler:
    def __init__(self, logger):
        self.__textures_folder = r'./textures/'
        self.loaded = {}
        self.logger = logger

    def load_textures(self, part="all"):
        path = self.__textures_folder
        if part != "all":
            for folder in part.split("."):
                path += folder+"/"

        content = os.listdir(path)
        for file in content:
            if os.path.isdir(path + file + "/"):
                self.load_textures(part+"."+file)

            elif file.split(".")[1] == "json":
                textures_info = {}
                with open(path + file, "r", encoding="UTF-8") as json_file:
                    textures_info = json.load(json_file)
                    self.__load(textures_info)

    def __load(self, info):
        t_type = info["type"].split("/")
        raw_image = pygame.image.load(info["file"]).convert_alpha()
        if t_type[0] == "simple":
            self.loaded[info["name"]] = self.resize(raw_image.copy(), size_coef=2)
            self.logger.log(info["name"] + " loaded", subject="load")
        elif t_type[0] == "strip":
            if t_type[1] == "textures":
                strip = []
                cursor = 0
                while cursor < raw_image.get_width():
                    strip.append(raw_image.subsurface(pygame.Rect((cursor, 0, info["format"]["width"], info["format"]["height"]))).copy())
                    self.loaded[info["name"]] = strip
                    self.logger.log(info["name"] + " loaded", subject="load")
                    cursor += info["format"]["width"]

        elif t_type[0] == "sheet":
            if t_type[1] == "charset":
                self.__load_sheet_charset(info, raw_image)

            elif t_type[1] == "gui":
                self.__load_sheet_gui(info, raw_image)

            elif t_type[1] == "block":
                self.__load_sheet_block(info, raw_image)

    def __load_sheet_block(self, info, raw_image):
        items = info["sheet"]["items"]
        self.loaded[info["name"]] = {}
        for item in items:
            new_sur = self.resize(raw_image.subsurface(pygame.Rect((item["x"], item["y"], item["width"], item["height"]))), size_coef=2)
            self.loaded[info["name"]][item['property']] = new_sur
            self.logger.log(info["name"] + ":" + str(item["property"]) + " loaded", subject="load")

    def __load_sheet_gui(self, info, raw_image):
        items = info["sheet"]["items"]

        for item in items:
            new_sur = raw_image.subsurface(pygame.Rect((item["x"], item["y"], item["width"], item["height"])))
            self.loaded[info["name"] + "." + item["name"]] = new_sur
            self.logger.log(info["name"] + "." + item["name"] + " loaded", subject="load")

    def __load_sheet_charset(self, info, raw_image):
        organization = info["charset"]["organisation"]

        new_entries = {}
        cursor_y = 0
        for line in organization:
            cursor_x = 0
            it = 0

            while cursor_x < len(line["sequence"] * line["width"]):
                concerned_area = pygame.Rect((cursor_x, cursor_y, line["width"], line["height"]))
                new_entries[line["sequence"][it]] = self.resize(raw_image.subsurface(concerned_area).copy(), size_coef=2)
                cursor_x += line["width"]
                it += 1
            cursor_y += line["height"]

        self.loaded[info["name"]] = new_entries
        self.logger.log(info["name"] + " loaded", subject="load")

    def get_texture(self, texture_path):
        t_path = texture_path.split(":")
        if len(t_path) == 2:
            if t_path[0] in self.loaded.keys() and int(t_path[1]) in self.loaded[t_path[0]].keys():
                return self.loaded[t_path[0]][int(t_path[1])]
            else:
                raise KeyError("Cette texture n'existe pas : " + texture_path)
        else:
            if t_path[0] in self.loaded.keys():
                return self.loaded[t_path[0]]
            else:
                raise KeyError("Cette texture n'existe pas : " + texture_path)

    @staticmethod
    def resize(surface, size_coef):
        return pygame.transform.scale(surface, (surface.get_width() * size_coef, surface.get_height() * size_coef))
