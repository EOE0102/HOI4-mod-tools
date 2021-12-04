from core import *

import tkinter
from tkinter import ttk

## REBUILD ##

## REBUILD ##
class StandardBoxForInfo(tk.Tk):

    def __init__(self):
        tkinter.Tk.__init__(self)

        tkinter.Tk.title(self, 'HOI4 create more Provinces tool')
        
        #butten 1
        a0_0_label = ttk.Label(self, text = "STEP1: Generate all available RGB, and write into a file")
        a0_0_label.grid(column = 0, row = 0)
        action = ttk.Button(self, text = "Click Me", command = step_save_all_color_into_file)
        action.grid(column = 0, row = 1)

        #butten 2
        a0_1_label = ttk.Label(self, text = "STEP2: get the painting area for every color in map")
        a0_1_label.grid(column = 0, row = 2)
        action = ttk.Button(self, text = "Click Me", command = step_get_RGB_area_for_every_color)
        action.grid(column = 0, row = 3)

        #butten 3
        a0_2_label = ttk.Label(self, text = "STEP3: get states info")
        a0_2_label.grid(column = 0, row = 4)
        action = ttk.Button(self, text = "Click ME", command = step_get_states_info)
        action.grid(column = 0, row = 5)

        #butten 4
        a0_2_label = ttk.Label(self, text = "STEP4: get seeds for every painting area")
        a0_2_label.grid(column = 0, row = 6)
        action = ttk.Button(self, text = "Click ME", command = step_get_seeds_in_every_area)
        action.grid(column = 0, row = 7)

        #butten 5
        a0_2_label = ttk.Label(self, text = "STEP5: get seeds painting area")
        a0_2_label.grid(column = 0, row = 8)
        action = ttk.Button(self, text = "Click ME", command = step_get_seeds_painting_area)
        action.grid(column = 0, row = 9)

        #butten 6
        a0_2_label = ttk.Label(self, text = "STEP6: painting pixels on map")
        a0_2_label.grid(column = 0, row = 10)
        action = ttk.Button(self, text = "Click ME", command = painting_pixels)
        action.grid(column = 0, row = 11)

        #butten 7
        a0_2_label = ttk.Label(self, text = "STEP7: modify files")
        a0_2_label.grid(column = 0, row = 12)
        action = ttk.Button(self, text = "Click ME", command = modify_files)
        action.grid(column = 0, row = 13)

        #butten 8
        a0_2_label = ttk.Label(self, text = "STEP8: modify supplie line")
        a0_2_label.grid(column = 0, row = 14)
        action = ttk.Button(self, text = "Click ME", command = modify_supply_lines)
        action.grid(column = 0, row = 15)


def check_pixel_is_next_to_seed_area(seeds_color, check_pixel, painting_area, painting_area_is_painted):
    #painting_area = dict.fromkeys(painting_area,True) 
    check_pixel_x = check_pixel[0]
    check_pixel_y = check_pixel[1]

    north_pixel = [check_pixel_x, check_pixel_y - 1]
    south_pixel = [check_pixel_x, check_pixel_y + 1]
    west_pixel = [check_pixel_x - 1, check_pixel_y]
    east_pixel = [check_pixel_x + 1, check_pixel_y]

    bol_north = False
    bol_south = False
    bol_west = False
    bol_east = False

    #around_pixels = [north_pixel, south_pixel, west_pixel, east_pixel]
    #for around_pixel, painting_area_1 in product(around_pixels, painting_area):
    #    if around_pixel == painting_area_1:
    #        if painting_area_is_painted[painting_area.index(painting_area_1)] == seeds_color:
    #            return True

    #return False

    #is_next_to_seed_area = bool( \
    #    ((north_pixel in painting_area) and painting_area_is_painted[painting_area.index(north_pixel)]) or \
    #    ((south_pixel in painting_area) and painting_area_is_painted[painting_area.index(south_pixel)]) or \
    #    ((west_pixel in painting_area) and painting_area_is_painted[painting_area.index(west_pixel)]) or \
    #    ((east_pixel in painting_area) and painting_area_is_painted[painting_area.index(east_pixel)])
    #    )
        
    if north_pixel in painting_area:
        if painting_area_is_painted[painting_area.index(north_pixel)] == seeds_color:
            bol_north = True
    if south_pixel in painting_area:
        if painting_area_is_painted[painting_area.index(south_pixel)] == seeds_color:
            bol_south = True
    if west_pixel in painting_area:
        if painting_area_is_painted[painting_area.index(west_pixel)] == seeds_color:
            bol_west = True
    if east_pixel in painting_area:
        if painting_area_is_painted[painting_area.index(east_pixel)] == seeds_color:
            bol_east = True
    is_next_to_seed_area = bol_north or bol_south or bol_west or bol_east

    return is_next_to_seed_area


def main():
    debug = False
    if debug == True:
        step_save_all_color_into_file()
        #all_RGB_and_Area_dict = step_get_RGB_area_for_every_color()
        step_get_RGB_area_for_every_color()
        #all_new_seeds_dict = step_get_seeds_in_every_area(all_RGB_and_Area_dict)
        step_get_seeds_in_every_area()
        #all_painting_area_dict, all_painting_area_dict_small = step_get_seeds_painting_area(all_RGB_and_Area_dict, all_new_seeds_dict)
        step_get_seeds_painting_area()
        painting_pixels()
        modify_files()
            
    else:
        windows = StandardBoxForInfo()
        windows.mainloop()


if __name__ == "__main__":
    main()
    
