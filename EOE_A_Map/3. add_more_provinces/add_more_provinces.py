from core import *

import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
import os
from PIL import Image #pip install Pillow
#import pickle #save variable memory error bad
#import joblib #save still variable memory error bad
#from itertools import takewhile
import re
import random

## REBUILD ##

## REBUILD ##
class StandardBoxForInfo(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        tk.Tk.title(self, 'HOI4 create more Provinces tool')
        
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

def get_seeds_painting_area(all_used_RGB, all_used_RGB_info, seeds_position_list, seeds_color_list):
    #dont forget to turn it back
    original_color = seeds_color_list[0]
    seeds_color_list[0] = (0,0,0)
    index_all_used_RGB = all_used_RGB.index(original_color)
    choose_RGB_info = all_used_RGB_info[index_all_used_RGB]
    choose_RGB_info_index = 0
    for i in range(len(choose_RGB_info)):
        if seeds_position_list[0] in choose_RGB_info[i][4]:
            choose_RGB_info_index = i
            break

    painting_area = choose_RGB_info[choose_RGB_info_index][4]
    painting_area_is_painted = []
    for i in painting_area:
        painting_area_is_painted.append(False)

    painting_area_for_loop = painting_area.copy()

    is_seeds_expand_end = []
    for i in range(len(seeds_position_list)):
        is_seeds_expand_end.append(False)

    #paint color for seeds
    for color1, color2 in product(seeds_position_list, painting_area):
        if color1 == color2:
            index1 = seeds_position_list.index(color1)
            index2 = painting_area.index(color2)
            painting_area_is_painted[index2] = seeds_color_list[index1]

    while sum(is_seeds_expand_end) < len(is_seeds_expand_end):
        #loop for every seed
        for i in range(len(seeds_position_list)):
            #seeds_color_list[i]
            if not is_seeds_expand_end[i]:
                painting_area_is_painted_for_loop = painting_area_is_painted.copy()
                for j in range(len(painting_area_is_painted)):
                    if not painting_area_is_painted[j]:
                        check_pixel = painting_area_for_loop[j]
                        is_next_to_seed_area = check_pixel_is_next_to_seed_area(seeds_color_list[i], check_pixel, painting_area_for_loop, painting_area_is_painted)
                        if is_next_to_seed_area:
                            index = painting_area_for_loop.index(check_pixel)
                            painting_area_is_painted_for_loop[index] = True
                
                painting_pixels_index = [i for i, x in enumerate(painting_area_is_painted_for_loop) if x == True]
                if len(painting_pixels_index) == 0:
                    is_seeds_expand_end[i] = True
                else:
                    choose_pixels = []
                    choose_pixels_distance = []
                    for item in painting_pixels_index:
                        choose_pixels.append(painting_area_for_loop[item])
                        distance = step2_genetate_rgb_area.calculate_P2P_distance(painting_area_for_loop[item], seeds_position_list[i])
                        choose_pixels_distance.append(distance)
                    
                    min_distance_index = [i for i, x in enumerate(choose_pixels_distance) if x == min(choose_pixels_distance)]
                    pick_index = random.randint(0, len(min_distance_index) - 1)
                    choosed_pixel = choose_pixels[min_distance_index[pick_index]]
                    index = painting_area_for_loop.index(choosed_pixel)
                    painting_area_is_painted[index] = seeds_color_list[i]

    for i in range(len(painting_area_is_painted)):
        if painting_area_is_painted[i] == (0,0,0):
            painting_area_is_painted[i] = original_color

    return original_color, painting_area, painting_area_is_painted





def painting_pixels():
    print('Part 6')
    all_painting_area_dict = read_dict('all_painting_area_dict')
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #full_file_name = temp_folder_location + "\\all_painting_area_dict.txt"
    #file = open(temp_folder_location + "\\all_painting_area_dict.txt", 'rb')
    #all_painting_area_dict = joblib.load(full_file_name)
    all_painting_pixels_position = all_painting_area_dict['Painting area position']
    all_painting_pixels_color = all_painting_area_dict['Painting area color']
    #read image
    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (provinces.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_width, image_height = im.size

    for i in range(len(all_painting_pixels_position)):
        for j in range(len(all_painting_pixels_position[i])):
            x = all_painting_pixels_position[i][j][0]
            y = all_painting_pixels_position[i][j][1]
            rgb = all_painting_pixels_color[i][j]
            pixels[x,y] = tuple(rgb)



    save_file = filedialog.asksaveasfilename(title = "save provinces.bmp")
    im.save(save_file)
    print('Part 6 finished')

## PART 7 ##

## PART 7 ##
def getbrace_only(text,level):
    result=[]
    stack=[]
    i=0
    while i<len(text) and text[i]=="{" and len(stack)<level:
        i+=1
        stack.append('{')
    
    while i<len(text):
        if text[i]=='{':
            stack.append('{')
        if len(stack)==level: 
            result.append(text[i])
        if text[i]=='}':
            stack.pop()
        i+=1
    return ''.join(result)

def find_inhalt_in_bracket_fcn(all_text_in_str, find_str, start_mark, end_mark):
    #all_text_in_str_initialized = all_text_in_str.replace("\t","")
    #all_text_in_str_initialized = all_text_in_str_initialized.replace("\n","") 
    find_text_position = [m.start() for m in re.finditer(find_str,all_text_in_str)]
    open_bracket_position = [m.start() for m in re.finditer(start_mark,all_text_in_str)]
    close_bracket_position = [m.start() for m in re.finditer(end_mark,all_text_in_str)]
    find_text_info = []
    #for i in range(len(find_text_position)):
    #    for j in reversed(open_bracket_position):
    ##        if j > find_text_position[i]:
    #           temp1 = j
    #           for k in reversed(close_bracket_position):
    #               if k > temp1:
    #                   temp2 = k
    #   find_text_info.append(all_text_in_str[temp1+1:temp2])


    for i in range(len(find_text_position)):
        j = 0
        while find_text_position[i] > open_bracket_position[j]:
            j = j + 1
        temp1 = open_bracket_position[j]
        k = 0
        while temp1 > close_bracket_position[k]:
            k = k + 1
        temp2 = close_bracket_position[k]
        find_text_info.append(all_text_in_str[temp1+1:temp2])
    return find_text_info

def remove_Comment(textInList):
    # remove comment
    for i in range(len(textInList)):
        if "#" in textInList[i]:
            textInList[i] = textInList[i].split("#",1)[0]
            textInList[i] = textInList[i] + "\n"
    all_text_in_str_initialized = "".join(textInList)
    return all_text_in_str_initialized

def is_this_province_coast(painging_area_RGB, painging_area_coast_type, allRGBInLst, allIsCoastTypeInLst):
    if painging_area_coast_type == 'false':
        return 'false'
    else:
        return 'true'

    #return writeCoastType

def write_definition_csv_file(exportFolderLocation, all_painting_area_dict_small, all_painting_area_dict):
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = open_file_return_str(title, filetypes)
    all_text_list = split_str_into_list(all_text_str, ';')
    definition_color_address = split_info_definition_csv(all_text_list)

    allRGBInLst = definition_color_address['RGB']
    allLandSeaLakeTypeInLst = definition_color_address['land_sea_lake']
    allIsCoastTypeInLst = definition_color_address['coast']
    allTerrainTypeInLst = definition_color_address['terrain']
    allContinentTypeInLst = definition_color_address['continent']
    newProvincesListFull = []
    
    for i in range(len(all_painting_area_dict_small)):
        defaultOriginalColor = all_painting_area_dict_small[i][0]
        originalIndex = allRGBInLst.index(defaultOriginalColor)
        
        newProvincesListFull.append([0,[]])
        newProvincesListFull[i][0] = originalIndex
        newProvincesListPart = []

        for j in range(1, len(all_painting_area_dict_small[i])):
            writeIndex = len(all_text_str)
            writeRGB = str(all_painting_area_dict_small[i][j][0]) + ';' + str(all_painting_area_dict_small[i][j][1]) + ';' + str(all_painting_area_dict_small[i][j][2])
            writeLandSeaLakeType = allLandSeaLakeTypeInLst[originalIndex]
            writeCoastType = is_this_province_coast(all_painting_area_dict_small[i][j], allIsCoastTypeInLst[originalIndex], allRGBInLst, allLandSeaLakeTypeInLst)
            
            writeTerrain = allTerrainTypeInLst[originalIndex]
            writeContinent = allContinentTypeInLst[originalIndex]
            writeLine = str(writeIndex) + ";" + writeRGB + ';' + str(writeLandSeaLakeType) + ';' + str(writeCoastType) + ';' + str(writeTerrain) + ';' + str(writeContinent) + '\n'
            all_text_str.append(writeLine)
            newProvincesListPart.append(writeIndex)

        newProvincesListFull[i][1] = newProvincesListPart


    save_file = filedialog.asksaveasfilename(title = "save definition.csv")
    f = open(save_file,'w')
    for element in all_text_str:
        f.write(element)
    f.close()

    return newProvincesListFull

def write_state_files(exportFolderLocation, newProvincesListFull, all_painting_area_dict_small):
    root = tk.Tk()
    stateFolderLocation = filedialog.askdirectory(title = "Select State Folder Location")
    stateFileList = []
    for file in os.listdir(stateFolderLocation):
        if file.endswith(".txt"):
            stateFileList.append(file)

    for bbk in range(len(stateFileList)):
        originalStateFileName = stateFileList[bbk]
        print('exporting states file: '+ str(bbk) + ' / ' + str(len(stateFileList)))
        #read original file
        temp = stateFolderLocation + "/" + originalStateFileName
        stateFileLocationIndex = open(temp)
        allTextInList = stateFileLocationIndex.readlines()
        stateFileLocationIndex.close()
        allTextInSrtNoComment = remove_Comment(allTextInList)

        #get province index
        original_provinces_ID = find_inhalt_in_bracket_fcn(allTextInSrtNoComment, "provinces", "{", "}")
        original_provinces_ID = original_provinces_ID[0].replace("\n","")
        original_provinces_ID = original_provinces_ID.replace("\t","")  
        originalProvinceID = int(original_provinces_ID)
        
        for i in range(len(all_painting_area_dict_small)):
            newFileString = allTextInSrtNoComment
            if newProvincesListFull[i][0] == originalProvinceID:
                addNewProvinceString = ''
                for j in range(len(newProvincesListFull[i][1])):
                    addNewProvinceString = addNewProvinceString + ' ' + str(newProvincesListFull[i][1][j])
                find_text_position1 = [m.start() for m in re.finditer("provinces", allTextInSrtNoComment)]

                provincedIDStartPosition = find_text_position1[0]
                shortText = allTextInSrtNoComment[int(provincedIDStartPosition):]
                find_text_position2 = [m.start() for m in re.finditer(str(originalProvinceID), shortText)]
                nearstPosition = int(find_text_position2[0]) + len(str(originalProvinceID))
                newFileString = allTextInSrtNoComment[:(provincedIDStartPosition + nearstPosition)] + addNewProvinceString + allTextInSrtNoComment[(provincedIDStartPosition + nearstPosition):]

                text_file = open(exportFolderLocation + "/export/states/" + originalStateFileName, "w")
                text_file.write(newFileString)
                text_file.close()

def write_strategicregions_files(exportFolderLocation, newProvincesListFull, all_painting_area_dict_small):
    root = tk.Tk()
    strategicregionsFolderLocation = filedialog.askdirectory(title = "Select strategicregions Folder Location")
    strategicregionsFileList = []
    for file in os.listdir(strategicregionsFolderLocation):
        if file.endswith(".txt"):
            strategicregionsFileList.append(file)

    for bbk in range(len(strategicregionsFileList)):
        originalStateFileName = strategicregionsFileList[bbk]
        print('exporting states file: '+ str(bbk) + ' / ' + str(len(strategicregionsFileList)))
        #read original file
        temp = strategicregionsFolderLocation + "/" + originalStateFileName
        strategicregionsFileLocationIndex = open(temp)
        allTextInList = strategicregionsFileLocationIndex.readlines()
        strategicregionsFileLocationIndex.close()
        allTextInSrtNoComment = remove_Comment(allTextInList)

        #get provinces index
        original_provinces_ID = find_inhalt_in_bracket_fcn(allTextInSrtNoComment, "provinces", "{", "}")
        provinces_IDs_list = original_provinces_ID.copy()
        provinces_IDs_list = provinces_IDs_list[0].split()
        for i in range(len(provinces_IDs_list)):
            if i == 0:
                province_ID_position = allTextInSrtNoComment.find('\t' + provinces_IDs_list[i] + ' ')
            else:
                province_ID_position = allTextInSrtNoComment.find(' ' + provinces_IDs_list[i] + ' ')
            for j in range(len(newProvincesListFull)):
                if str(newProvincesListFull[j][0]) == provinces_IDs_list[i]:
                    text_begin = allTextInSrtNoComment[0:(province_ID_position + len(provinces_IDs_list[i]) + 1)]
                    text_end = allTextInSrtNoComment[(province_ID_position + len(provinces_IDs_list[i]) + 1):len(allTextInSrtNoComment)]
                    text_middle = ''
                    for k in range(len(newProvincesListFull[j][1])):
                        text_middle = text_middle + ' ' + str(newProvincesListFull[j][1][k])
                    allTextInSrtNoComment = text_begin + text_middle + text_end



        text_file = open(exportFolderLocation + "/export/strategicregions/" + originalStateFileName, "w")
        text_file.write(allTextInSrtNoComment)
        text_file.close()



def modify_files():
    print('Part 7')

    all_painting_area_dict_small = read_dict('all_painting_area_dict_small')
    all_painting_area_dict = read_dict('all_painting_area_dict')

    exportFolderLocation = filedialog.askdirectory(title = "Select Export Folder Location")
    if not os.path.exists(exportFolderLocation + "/export/states"):
        os.makedirs(exportFolderLocation + "/export/states")
    if not os.path.exists(exportFolderLocation + "/export/strategicregions"):
        os.makedirs(exportFolderLocation + "/export/strategicregions")


    newProvincesListFull = write_definition_csv_file(exportFolderLocation, all_painting_area_dict_small, all_painting_area_dict)
    write_state_files(exportFolderLocation, newProvincesListFull, all_painting_area_dict_small)
    write_strategicregions_files(exportFolderLocation, newProvincesListFull, all_painting_area_dict_small)

    print('Part 7 finished')

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
    
