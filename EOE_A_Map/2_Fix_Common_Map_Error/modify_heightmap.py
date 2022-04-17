from core import *

from tkinter import filedialog
import PIL
from PIL import Image

def modify_heightmap():

    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = open_file_return_str(title, filetypes)
    all_text_list = split_str_into_list(all_text_str, ';')
    definition_color_address = split_info_definition_csv(all_text_list)
    used_RGB = definition_color_address['RGB']
    used_land_sea_lake = definition_color_address['land_sea_lake']

    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (province.bmp)", filetypes={("HOI Map file", ".bmp")})
    im_map = Image.open(full_filename)
    pixels_map = im_map.load()
    full_filename = filedialog.askopenfilename(title = "Choose heightmap Map File (heightmap.bmp)", filetypes={("heightmap file", ".bmp")})
    im_heightmap = Image.open(full_filename)
    im_heightmap2 = im_heightmap.quantize(colors = 256)
    pixels_heightmap = im_heightmap2.load()

    a = 1
    image_width, image_height = im_map.size
    pixel_sea_level_color = pixels_heightmap[0, 0]
    for pixel_y in range(1, image_height - 1):
        print('Modify line ' + str(pixel_y) + ' / ' + str(image_height))
        for pixel_x in range(1, image_width - 1):
            pixel_map_color = list(pixels_map[pixel_x, pixel_y])
            pixel_map_land_sea_lake_type = used_land_sea_lake[used_RGB.index(pixel_map_color)]

            pixel_heightmap_color = pixels_heightmap[pixel_x, pixel_y] #89 as sea level
            if pixel_map_land_sea_lake_type == 'sea' and pixel_heightmap_color != pixel_sea_level_color:
                pixels_heightmap[pixel_x, pixel_y] = pixel_sea_level_color

            elif pixel_map_land_sea_lake_type == 'lake' and pixel_heightmap_color != pixel_sea_level_color:
                pixels_heightmap[pixel_x, pixel_y] = pixel_sea_level_color
            elif pixel_map_land_sea_lake_type == 'land' and pixel_heightmap_color == pixel_sea_level_color:
                pixel_left = pixels_heightmap[pixel_x - 1, pixel_y]
                pixel_right = pixels_heightmap[pixel_x + 1, pixel_y]
                pixel_up = pixels_heightmap[pixel_x, pixel_y - 1]
                pixel_down = pixels_heightmap[pixel_x, pixel_y + 1]
                pixel_height_average = int((pixel_left + pixel_right + pixel_up + pixel_down)/4)
                #if pixel_height_average == pixel_sea_level_color:
                #    pixel_height_average = pixel_sea_level_color + 1
                pixels_heightmap[pixel_x, pixel_y] = pixel_height_average

    im_heightmap3 = im_heightmap2.convert('L')
    im_heightmap3.save("heightmap_new.bmp")



def main():
    modify_heightmap()

if __name__ == "__main__":
    main()
