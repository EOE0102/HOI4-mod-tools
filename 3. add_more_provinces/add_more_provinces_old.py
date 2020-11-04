import tkinter as tk 
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog
import os
from PIL import Image
#import pickle #save variable memory error bad
#import joblib #save still variable memory error bad
import json #finally find one
from itertools import product
#from itertools import takewhile
from time import time
import math
import random
import re
import numpy as np

def miller_cylinder_forward_projection(theta_in_rand):
    longitude_in_what = 1.25 * np.log(np.tan(np.pi / 4 + 0.4 * theta_in_rand))
    return longitude_in_what

def miller_cylinder_inverse_projection(longitude_in_what):
    theta_in_rand = 2.5 * (np.arctan(np.exp(0.8 * longitude_in_what)) - np.pi / 4)
    return theta_in_rand

#im.save("pixel_grid.bmp")
iterate_amount = 2
#equatorialPosition = 1350
longitude_north = 72
longitude_south = 57
longitude_north_in_rand = longitude_north/ 180 * np.pi
longitude_south_in_rand = longitude_south/ 180 * np.pi
longitude_north2D = miller_cylinder_forward_projection(longitude_north_in_rand)
longitude_south2D = miller_cylinder_forward_projection(longitude_south_in_rand)

default_province_size = 24 #pixel on equator
max_new_provinces_per_state = 5

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
        a0_2_label = ttk.Label(self, text = "STEP2.5: get states info")
        a0_2_label.grid(column = 0, row = 4)
        action = ttk.Button(self, text = "Click ME", command = step_get_states_info)
        action.grid(column = 0, row = 5)

        #butten 4
        a0_2_label = ttk.Label(self, text = "STEP3: get seeds for every painting area")
        a0_2_label.grid(column = 0, row = 6)
        action = ttk.Button(self, text = "Click ME", command = step_get_seeds_in_every_area)
        action.grid(column = 0, row = 7)

        #butten 5
        a0_2_label = ttk.Label(self, text = "STEP4: get seeds painting area")
        a0_2_label.grid(column = 0, row = 8)
        action = ttk.Button(self, text = "Click ME", command = step_get_seeds_painting_area)
        action.grid(column = 0, row = 9)

        #butten 6
        a0_2_label = ttk.Label(self, text = "STEP5: painting pixels on map")
        a0_2_label.grid(column = 0, row = 10)
        action = ttk.Button(self, text = "Click ME", command = painting_pixels)
        action.grid(column = 0, row = 11)

        #butten 7
        a0_2_label = ttk.Label(self, text = "STEP6: modify files")
        a0_2_label.grid(column = 0, row = 12)
        action = ttk.Button(self, text = "Click ME", command = modify_files)
        action.grid(column = 0, row = 13)

## PART 1 ##

## PART 1 ##

def list_all_RGB():
    #R range 0-10 42-52, 84-94, 126-136, 168-178 + 210-220
    #G range 0-210
    #B range 0,5,10,15,20 ...225
    all_color_R = []
    all_color_G = []
    all_color_B = []
    all_color = []
    for i in range(40):
        all_color_R.append((5*i))

    for i in range(50):
        all_color_G.append(4*i)

    #for i in range(46):
    for i in range(40):
        all_color_B.append(5*i)

    for i in all_color_R:
        for j in all_color_G:
            for k in all_color_B:
                all_color.append([i,j,k])
                
    all_color.remove([0,0,0])
    return all_color

def save_color_into_file(all_color):
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = open_file_return_str(title, filetypes)
    all_text_list = split_str_into_list(all_text_str, ';')
    definition_color_address = split_info_definition_csv(all_text_list)
    used_RGB = definition_color_address['RGB']


    save_file = filedialog.asksaveasfilename(title = "save all_RGB_list.txt")
    with open(save_file, 'w') as filehandle:
        for i in range(len(all_color)):
            R = str(all_color[i][0])
            G = str(all_color[i][1])
            B = str(all_color[i][2])
            #filehandle.write(R + ','+ G+',' + B +'\n')
            #if i % 5 == 4:

            if not([int(R),int(G),int(B)] in used_RGB):
                filehandle.write("%s;%s;%s\n" % (R,G,B))
    filehandle.close()

def step_save_all_color_into_file():
    all_color = list_all_RGB()
    save_color_into_file(all_color)
    print('Part 1 finished')

## PART 2 ##

## PART 2 ##

def open_file_return_str(dialog_title, file_filetypes):
    root = tk.Tk()
    root.filename = filedialog.askopenfilename(title = dialog_title, filetypes = file_filetypes)
    file_str_original = open(root.filename , encoding='gb18030', errors='ignore')
    all_text_str = file_str_original.readlines()
    file_str_original.close()
    return all_text_str

def split_str_into_list(textlist, spliter):
    textlist2 = textlist.copy()
    for i in range(len(textlist2)):
        textlist2[i] = textlist2[i].split(spliter)
    return textlist2

def split_info_definition_csv(all_text_list):
    all_used_RGB = []
    all_land_sea_lake_type = []
    all_is_coast_type = []
    all_terrain_type = []
    all_continent_index = []
    for i in range(len(all_text_list)):
        R = int(all_text_list[i][1])
        G = int(all_text_list[i][2])
        B = int(all_text_list[i][3])
        all_used_RGB.append([R,G,B])

        LandSeaLake = all_text_list[i][4]
        all_land_sea_lake_type.append(LandSeaLake)

        Coast = all_text_list[i][5]
        all_is_coast_type.append(Coast)

        Terrain = all_text_list[i][6]
        all_terrain_type.append(Terrain)

        Continent = int(all_text_list[i][7])
        all_continent_index.append(Continent)

    return {
        'RGB':all_used_RGB,
        'land_sea_lake':all_land_sea_lake_type,
        'coast':all_is_coast_type,
        'terrain':all_terrain_type,
        'continent':all_continent_index
    }

def msgbox_prepare_aviliable_RGB_file():
    a = tkinter.messagebox.askquestion('Do you have generated allRGBList file', 'click NO to generated file (takes time)')
    print(a)
    if a == "yes":
        return True
    else:
        return False

def __splitRGBOutOfLst2(all_text_list):
    allRGBInLst = []
    for i in range(len(all_text_list)):
        R = int(all_text_list[i][0])
        G = int(all_text_list[i][1])
        B = int(all_text_list[i][2])
        allRGBInLst.append((R,G,B))
    return allRGBInLst

def floodfill(pixels, oldColor, newColor, xMax, yMax, defaultX, defaultY):
    # assume surface is a 2D image and surface[x][y] is the color at x, y.
    #(pixels, pixel_RGB, image_width, image_height, count_image_width, count_image_height, (0,0,0))
    x = defaultX
    y = defaultY
    theStack = [ (x, y) ]
    theArea = []
    while len(theStack) > 0:
        x, y = theStack.pop()
        if (x < 0) or (x >= xMax) or (y < 0) or (y >= yMax):
        #if x >= xMax or y >= yMax:
            arront = (0,0,0)
        else:
            arront = list(pixels[x,y])
        if arront == list(oldColor):
            pixels[x,y] = newColor
            theArea.append([x,y])
            theStack.append( (x + 1, y) )  # right
            theStack.append( (x - 1, y) )  # left
            theStack.append( (x, y + 1) )  # down
            theStack.append( (x, y - 1) )  # up
    return theArea, pixels

def calculate_point_of_gravity(RGBAreaPointOfGravityList):
    avgX = 0
    avgY = 0
    for item in range(len(RGBAreaPointOfGravityList)):
        avgX = RGBAreaPointOfGravityList[item][0] + 0.5 + avgX
        avgY = RGBAreaPointOfGravityList[item][1] + 0.5 + avgY
    avgX = avgX/len(RGBAreaPointOfGravityList) - 0.001 #0.5 >> 0
    avgY = avgY/len(RGBAreaPointOfGravityList) - 0.001 #2.5 >> 2
    return [avgX, avgY]

def calculate_P2P_distance(Point1, Point2):
    #Point1 = get_real_POG(Point1)
    
    #x1 = Point1[0]
    #x2 = Point2[0]
    #y1 = Point1[1]
    #y2 = Point2[1]
    distance = math.pow((Point1[0]-Point2[0]),2) + math.pow((Point1[1]-Point2[1]),2)
    if distance == 0:
        return 0
    else:
        distance = math.pow(distance,0.5)
    return distance

def calculate_P2P_energy(Point1, Point2):
    #x1 = Point1[0]
    #x2 = Point2[0]
    #y1 = Point1[1]
    #y2 = Point2[1]

    distance = math.pow((Point1[0]-Point2[0]),2) + math.pow((Point1[1]-Point2[1]),2)

    if distance == 0:
        return 10000000000 #float('inf') + float('inf') = inf
    else:
        energy = 1 / distance
        return energy
    


def  calculate_sum_p2p_distances(coreOfNewSeed):
    allCoreOfSeedDistance = 0
    for i in range(len(coreOfNewSeed)):
        for j in range(i+1, len(coreOfNewSeed)):
            allCoreOfSeedDistance = allCoreOfSeedDistance + calculate_P2P_distance(coreOfNewSeed[i], coreOfNewSeed[j])
    return allCoreOfSeedDistance

def calculate_sum_p2p_distances_v2(coreOfNewSeed):
    sum_distances = 0
    for point1, point2 in product(coreOfNewSeed, coreOfNewSeed):
        sum_distances = sum_distances + calculate_P2P_distance(point1, point2) / 2
    return sum_distances

def calculate_sum_p2p_energy(coreOfNewSeed):
    sum_energy = 0
    for point1, point2 in product(coreOfNewSeed, coreOfNewSeed):
        sum_energy = sum_energy + calculate_P2P_energy(point1, point2) / 2
    return sum_energy


def get_real_POG(Point):
    x = Point[0] + 0.5
    y = Point[1] + 0.5
    return [x,y]

def get_nearest_POG(rgb_area_POG, rgb_area_p):
    distanceList = []
    for item in rgb_area_p:
        p2pDistance = calculate_P2P_distance(rgb_area_POG, get_real_POG(item))
        distanceList.append(p2pDistance)
    minPos = distanceList.index(min(distanceList))
    rgb_area_nearest_POG = rgb_area_p[minPos]
    return rgb_area_nearest_POG

def save_dict(some_variable, variable_str):
    ftypes = [('txt', '.txt'),('All files', '*')]
    path = filedialog.asksaveasfilename(title = ("save Variable " + str(variable_str)), filetypes = ftypes)
    print('Be patient, saving: ' + str(variable_str))
    with open(path, 'w') as f:
        json.dump(some_variable, f)

def read_dict(variable_str):
    ftypes = [('txt', '.txt'),('All files', '*')]
    path = filedialog.askopenfilename(title = ("load Variable " + str(variable_str)), filetypes = ftypes)
    print('Be patient, reading: ' + str(variable_str))
    with open(path) as f:
        some_variable = json.load(f)
    return some_variable

def step_get_RGB_area_for_every_color():
    #read image
    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (provinces.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_width, image_height = im.size

    ##get all RGB Area
    all_RGB_and_Area_list = []
    used_RGB_list = []
    #all_RGB_and_Area_list.append([(0,0,0),[(0,0),(0,0),(0,0),0]]) #[RGB, [_startPoint, PointOfGravity, NearestPointOfGravity, Count]]
    for count_image_height in range(image_height):
        print("Part2: get PaintArea for every color | line = " + str(count_image_height) +' / '+str(image_height))
        for count_image_width in range(image_width):
            #print("Modifying Part1: x = " + str(count_image_width) + ' / ' + str(image_width) + ', y = ' + str(count_image_height) +' / '+str(image_height))

            pixel_old_RGB = pixels[count_image_width, count_image_height]

            if pixel_old_RGB != (0,0,0):
                rgb_area_info_list = []
                if pixel_old_RGB in used_RGB_list:
                    
                    _startPoint = (count_image_width, count_image_height)
                    rgb_area_p = []
                    rgb_area_p, pixels = floodfill(pixels, pixel_old_RGB, (0,0,0), image_width, image_height, count_image_width, count_image_height)

                    rgb_area_POG = calculate_point_of_gravity(rgb_area_p)
                    rgb_area_nearest_POG = get_nearest_POG(rgb_area_POG, rgb_area_p)
                    rgb_area_info_list.append(_startPoint)
                    rgb_area_info_list.append(rgb_area_POG)
                    rgb_area_info_list.append(rgb_area_nearest_POG)
                    rgb_area_info_list.append(len(rgb_area_p))
                    rgb_area_info_list.append(rgb_area_p)

                    tempIndex = used_RGB_list.index(pixel_old_RGB)
                    all_RGB_and_Area_list[tempIndex].append(rgb_area_info_list)
                    
                else:
                    #first time of meeting this color
                    _startPoint = (count_image_width, count_image_height)
                    rgb_area_p = []
                    rgb_area_p, pixels = floodfill(pixels, pixel_old_RGB, (0,0,0), image_width, image_height, count_image_width, count_image_height)
                    rgb_area_POG = calculate_point_of_gravity(rgb_area_p)
                    rgb_area_nearest_POG = get_nearest_POG(rgb_area_POG, rgb_area_p)
                    rgb_area_info_list.append(_startPoint)
                    rgb_area_info_list.append(rgb_area_POG)
                    rgb_area_info_list.append(rgb_area_nearest_POG)
                    rgb_area_info_list.append(len(rgb_area_p))
                    rgb_area_info_list.append(rgb_area_p)
                    
                    tempRGB = []
                    tempRGB.append(pixel_old_RGB)
                    temp = []
                    temp.append(rgb_area_info_list)
                    all_RGB_and_Area_list.append(temp)
                    used_RGB_list.append(pixel_old_RGB)
    all_RGB_and_Area_dict = {
        'RGB':used_RGB_list,
        'Seeds Info':all_RGB_and_Area_list
    }

    save_dict(all_RGB_and_Area_dict, 'all_RGB_and_Area_dict')
    #get local folder location
    #all_RGB_and_Area_list
    #[[R,G,B],[  [(startX,startY),[POGX,POGY],[POGinareaX, POGinareaY],AmountOfPoints, [points area]],  [another part]]]
    #used_RGB_list
    #[(R,G,B), (R,G,B) ...]
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #if not os.path.exists(temp_folder_location):
    #    os.makedirs(temp_folder_location)
    #full_file_name = temp_folder_location + "\\all_RGB_and_Area_dict.txt"
    #joblib.dump(all_RGB_and_Area_dict, full_file_name)
    #fp = open(full_file_name, 'wb'):
    #pickle.dump(all_RGB_and_Area_dict, fp)
    #fp.close()
    print('Part 2 finished')
    #return all_RGB_and_Area_dict


## PART 2.5 ##

## PART 2.5 ##

def str_initialize(_all_text_in_lst):
    # remove comment
    for i in range(len(_all_text_in_lst)):
        if "#" in _all_text_in_lst[i]:
            _all_text_in_lst[i] = _all_text_in_lst[i].split("#",1)[0]
            _all_text_in_lst[i] = _all_text_in_lst[i] + "\n"
    all_text_in_str_initialized = "".join(_all_text_in_lst)
    return all_text_in_str_initialized

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
    #        if j > find_text_position[i]:
    #            temp1 = j
    #            for k in reversed(close_bracket_position):
    #                if k > temp1:
    #                    temp2 = k
        
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


def read_state_info(all_text_in_lst):
    all_text_in_str_initialized = str_initialize(all_text_in_lst)
    #state basic info 1
    text_in_level_1 = getbrace_only(all_text_in_str_initialized,1)
    text_in_level_1_nospace = text_in_level_1.replace(" ","")
    original_state_id = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "id", "=", "\n")
    #original_state_name = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "name", "=", "\n")
    #original_state_manpower = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "manpower", "=", "\n")
    original_state_category = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "state_category", "=", "\n")
    original_state_category[0] = original_state_category[0].replace("\"", "")
    #original_buildings_max_level_factor = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "buildings_max_level_factor", "=", "\n")
    original_impassable = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "impassable", "=", "\n")
    

    # resources & provinces ID & VPs
    original_resources = find_inhalt_in_bracket_fcn(all_text_in_str_initialized, "resources", "{", "}")
    original_provinces_ID = find_inhalt_in_bracket_fcn(all_text_in_str_initialized, "provinces", "{", "}")
    original_provinces_ID = original_provinces_ID[0].replace("\n","")
    original_provinces_ID = original_provinces_ID.replace("\t","")  
    original_victory_points = find_inhalt_in_bracket_fcn(all_text_in_str_initialized, "victory_points", "{", "}")

    text_in_level_2 = getbrace_only(all_text_in_str_initialized,2)
    text_in_level_2_nospace = text_in_level_2.replace(" ","")
    original_state_owner = find_inhalt_in_bracket_fcn(text_in_level_2_nospace, "owner", "=", "\n")
    original_add_core_of_country_tag = find_inhalt_in_bracket_fcn(text_in_level_2_nospace, "add_core_of", "=", "\n")
    #dont forget
    #original_set_demilitarized_zone = find_inhalt_in_bracket_fcn(text_in_level_2_nospace, "set_demilitarized_zone", "=", "\n")

    state_info_dict = {
        'id': original_state_id,
        'state_category': original_state_category,
        'impassable': original_impassable,
        'resources': original_resources,
        'provinces': original_provinces_ID,
        'victory_points': original_victory_points,
        'owner': original_state_owner,
        'add_core_of': original_add_core_of_country_tag
    }
    #provinces, impassable, state_category, victory_points, owner, add_core_of
    return state_info_dict

def sum_state_info_dict(states_info_dict, state_info_dict):
    states_info_dict['id'].append(state_info_dict['id'])
    states_info_dict['state_category'].append(state_info_dict['state_category'])
    states_info_dict['impassable'].append(state_info_dict['impassable'])
    states_info_dict['resources'].append(state_info_dict['resources'])
    states_info_dict['provinces'].append(state_info_dict['provinces'])
    states_info_dict['victory_points'].append(state_info_dict['victory_points'])
    states_info_dict['owner'].append(state_info_dict['owner'])
    states_info_dict['add_core_of'].append(state_info_dict['add_core_of'])

    return states_info_dict

def read_states_info():
    states_folder_location = filedialog.askdirectory(title = "Select State Folder Location")
    states_file_lst = []
    for file in os.listdir(states_folder_location):
        if file.endswith(".txt"):
            states_file_lst.append(file)

    #read every state in folder
    states_info_dict = {
        'id': [],
        'state_category': [],
        'impassable': [],
        'resources': [],
        'provinces': [],
        'victory_points': [],
        'owner': [],
        'add_core_of': []
    }
    for base_state_file_name in states_file_lst:
        #read original file
        temp = states_folder_location + "/" + base_state_file_name
        file_state_original = open(temp)
        all_text_in_lst = file_state_original.readlines()
        file_state_original.close()
        state_info_dict = read_state_info(all_text_in_lst)
        states_info_dict = sum_state_info_dict(states_info_dict, state_info_dict)

    return states_info_dict

def read_definition_info():
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = open_file_return_str(title, filetypes)
    all_text_list = split_str_into_list(all_text_str, ';')
    definition_color_address = split_info_definition_csv(all_text_list)
    return definition_color_address

def step_get_states_info():
    states_info_dict = read_states_info()
    save_dict(states_info_dict, 'states_info_dict')
    definition_info_dict = read_definition_info()
    save_dict(definition_info_dict, 'definition_info_dict')

    print('PART 2.5 finished')

## PART 3 ##

## PART 3 ##

def no_iteration_get_seed(iterate_amount, startItem, coreOfSeed, rgb_area_p):
    coreOfNewSeed = coreOfSeed.copy()
    for i in range(iterate_amount):
        for j in range(startItem, len(coreOfNewSeed)):
            #old_mutil_sum_energy = calculate_sum_p2p_energy(coreOfNewSeed)
            replacedNewCoreList = coreOfNewSeed.copy()
            new_mutil_sum_energy_list = []
            for k in range(len(rgb_area_p)):
                replacedNewCoreList[j] = rgb_area_p[k]
                new_sum_energy = calculate_sum_p2p_energy(replacedNewCoreList)
                new_mutil_sum_energy_list.append(new_sum_energy)
            min_energy = min(new_mutil_sum_energy_list)
            min_energy_index = [UUK for UUK, x in enumerate(new_mutil_sum_energy_list) if x == min_energy]
            
            #pickNumber = random.randint(0, len(min_energy_index) - 1)
            pickNumber = 0
            choosedMinDistanceIndex = min_energy_index[pickNumber]
            randomPickedNewCore = rgb_area_p[choosedMinDistanceIndex]
            coreOfNewSeed[j] = randomPickedNewCore

    return coreOfNewSeed


def is_province_land(original_color, voll_rgb_list, land_sea_lake_type):
    index = voll_rgb_list.index(list(original_color))
    landSeaLakeType = land_sea_lake_type[index]
    if landSeaLakeType == 'land':
        return True
    else:
        return False

def is_province_coast(original_color, voll_rgb_list, coast_type):
    index = voll_rgb_list.index(list(original_color))
    coastType = coast_type[index]
    if coastType == 'true':
        return True
    else:
        return False

def get_coast_points_collection(_rgb_area_main_RGB, _seeds_painting_area, _pixels, _all_color_area_RGB, _all_color_area_land_sea_lake_type):
    _coast_points_collection = []
    for _check_pixel in _seeds_painting_area:
        _bol_is_pixel_coast = False
        x = _check_pixel[0]
        y = _check_pixel[1]
        north_pixel_color = list(_pixels[x, y+1])
        south_pixel_color = list(_pixels[x, y-1])
        west_pixel_color = list(_pixels[x-1, y])
        east_pixel_color = list(_pixels[x+1, y])
        _north_pixel_index = _all_color_area_RGB.index(north_pixel_color)
        _south_pixel_index = _all_color_area_RGB.index(south_pixel_color)
        _west_pixel_index = _all_color_area_RGB.index(west_pixel_color)
        _east_pixel_index = _all_color_area_RGB.index(east_pixel_color)
        _north_pixel_sea_type = _all_color_area_land_sea_lake_type[_north_pixel_index]
        _south_pixel_sea_type = _all_color_area_land_sea_lake_type[_south_pixel_index]
        _west_pixel_sea_type = _all_color_area_land_sea_lake_type[_west_pixel_index]
        _east_pixel_sea_type = _all_color_area_land_sea_lake_type[_east_pixel_index]
        if _north_pixel_sea_type == 'sea' or _south_pixel_sea_type == 'sea' or _west_pixel_sea_type == 'sea' or _east_pixel_sea_type == 'sea':
            _coast_points_collection.append(_check_pixel)
    return _coast_points_collection


def calculate_joint_POG(all_RGB_and_Area_list, rgb_area_main_part_index):
    joint_POG = all_RGB_and_Area_list[rgb_area_main_part_index][2]
    jointX = 0
    jointY = 0
    jointAmount = 0
    for i in range(len(all_RGB_and_Area_list)):
        if i == rgb_area_main_part_index:
            a = 1
        else:
            jointX = jointX + all_RGB_and_Area_list[i][3] * all_RGB_and_Area_list[i][1][0]
            jointY = jointY + all_RGB_and_Area_list[i][3] * all_RGB_and_Area_list[i][1][1]
            jointAmount = jointAmount + all_RGB_and_Area_list[i][3]
    jointX = jointX/jointAmount
    jointY = jointY/jointAmount
    joint_POG = [jointX, jointY]

    return joint_POG

def get_nearest_POGOfSmallPartOnMainBlock(RGBAreaPartRestJointPointOfGravity, rgb_area_p):
    #RGBAreaPartRestJointPointOfGravity[0] = RGBAreaPartRestJointPointOfGravity[0] -0.5
    #RGBAreaPartRestJointPointOfGravity[1] = RGBAreaPartRestJointPointOfGravity[1] -0.5
    distance = 100000
    index = 0
    for item in range(len(rgb_area_p)):
        distanceTemp = calculate_P2P_distance(RGBAreaPartRestJointPointOfGravity, rgb_area_p[item])
        if distanceTemp < distance:
            distance = distanceTemp
            index = item
    nearestPointOfGravityOfSmallPart = rgb_area_p[index]
    return nearestPointOfGravityOfSmallPart

def calculate_divide_province_amount(image_height, default_province_size, longitude_north2D, longitude_south2D, rgb_area_main_POG, RGBAreaFullSize, max_new_provinces_per_state):
    # according to altitude
    equatorPosition = round(longitude_north2D/(longitude_north2D + longitude_south2D) * image_height)
    longitude2DHeight = rgb_area_main_POG[1]
    longitudeInBall = (longitude_north2D + longitude_south2D)/image_height * longitude2DHeight - longitude_north2D
    longitudeInBallInRand = miller_cylinder_inverse_projection(abs(longitudeInBall))

    xMagnify = 1/(np.cos(longitudeInBallInRand))
    #longitudeInBallInRand = longitudeInBallInRand/np.pi * 180
    temp1 = abs(abs(miller_cylinder_forward_projection(abs(longitudeInBallInRand) + 0.05)) - abs(miller_cylinder_forward_projection(abs(longitudeInBallInRand) - 0.05)))
    temp2 = miller_cylinder_forward_projection(0.05)*2
    yMagnify = temp1/temp2 #area near equator, difference is not accurate
    if yMagnify < 1: 
        yMagnify = 1
    areaMagnify = xMagnify * yMagnify

    refileProvinceSize = default_province_size * areaMagnify
    
    amountProvince = int(round(RGBAreaFullSize/refileProvinceSize -0.5 ))
    # don't do too harsh, divide province into 1 - 10 pieces
    if amountProvince == 0:
        amountProvince = 1
    if amountProvince >= max_new_provinces_per_state:
        amountProvince = max_new_provinces_per_state

    return amountProvince

#TODO Define painting state conditions
def correct_new_province_max_amount(max_new_provinces_per_state, rgb_area_main_RGB, definition_info_dict, states_info_dict):

    index_in_definition = definition_info_dict['RGB'].index(rgb_area_main_RGB)
    state_info_continent = definition_info_dict['continent'][index_in_definition]
    state_info_terrain = definition_info_dict['terrain'][index_in_definition]
    state_info_coast = definition_info_dict['coast'][index_in_definition]
    index_in_state_file = states_info_dict['provinces'].index((' ' + str(index_in_definition) + ' ') )
    state_info_id = states_info_dict['id'][index_in_state_file]
    state_info_state_category = states_info_dict['state_category'][index_in_state_file]
    state_info_impassable = states_info_dict['impassable'][index_in_state_file]
    state_info_resources = states_info_dict['resources'][index_in_state_file]
    state_info_provinces = states_info_dict['provinces'][index_in_state_file]
    state_info_victory_points = states_info_dict['victory_points'][index_in_state_file]
    state_info_owner = states_info_dict['owner'][index_in_state_file]
    state_info_add_core_of = states_info_dict['add_core_of'][index_in_state_file]

    #terrain unknown ocean lakes forest hills mountain plains urban jungle marsh desert water_fjords water_shallow_sea water_deep_ocean
    terrain_okay_dict = {
        'terrain': ['forest', 'hills', 'mountain', 'plains', 'urban', 'jungle', 'marsh', 'desert'],
        'new_province_max_amount': [3,3,3,3,4,3,2,2]
    }
    #countrytag, continent ['DEN',1]
    owner_okay_list = [['POR',1], ['SPR',1], ['FRA',1], ['ITA',1], ['GER',1], ['CZE',1], ['POL',1], ['AUS',1], 
        ['HUN',1], ['ROM',1], ['BUL',1], ['YUG',1], ['GRE',1], ['ALB',1], ['LIT',1], ['LAT',1], ['EST',1],
        ['BEL',1], ['HOL',1], ['LUX',1], ['ENG',1],
        ['SOV',1], ['ETH',5]]


    add_core_of_list = ['LIB', 'CHI', 'PRC', 'KOR', 'LBA', 'EGY']
    new_province_max_amount = 1
    if len(state_info_impassable) > 0:
        return new_province_max_amount

    elif [state_info_owner[0], state_info_continent] in owner_okay_list:
        if state_info_terrain in terrain_okay_dict['terrain']:
            new_province_max_amount = terrain_okay_dict['new_province_max_amount'][(terrain_okay_dict['terrain'].index(state_info_terrain))]

    elif (str(state_info_add_core_of)[2:5] in add_core_of_list) or (str(state_info_add_core_of)[9:12] in add_core_of_list):
        if state_info_terrain in terrain_okay_dict['terrain']:
            new_province_max_amount = terrain_okay_dict['new_province_max_amount'][(terrain_okay_dict['terrain'].index(state_info_terrain))]
    
    return new_province_max_amount


def step_get_seeds_in_every_area():
    #all_RGB_and_Area_list

    all_RGB_and_Area_dict = read_dict('all_RGB_and_Area_dict')
    all_RGB_list = all_RGB_and_Area_dict['RGB']
    all_seed_info = all_RGB_and_Area_dict['Seeds Info']
    #Open definition.csv#
    #exp: 4;0;0;232;sea;true;ocean;0
    # index;R;G;B;land/sea/lake;coast?;terrain;continent
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = open_file_return_str(title, filetypes)
    all_text_list = split_str_into_list(all_text_str, ';')
    definition_color_address = split_info_definition_csv(all_text_list)

    states_info_dict = read_dict('states_info_dict')
    definition_info_dict = read_dict('definition_info_dict')

    #ask do I have generated RGB file
    #bol_have_RGB_file = msgbox_prepare_aviliable_RGB_file()
    #if not bol_have_RGB_file:   #goto step 1 baka
    #    step_save_all_color_into_file

    #read image
    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (provinces.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_width, image_height = im.size

    #area Size
    paintColorAreaFull = []
    paintColorArea = []
    all_cores_of_seed_list = []
    count = 0
    all_seeds_original_color_list = []
    
    for iRGBList in range(len(all_RGB_list)):
        print("Part 3：get painting seeds location for every color : Color = " + str(iRGBList) + ' / ' + str(len(all_RGB_list)))
        t = time()
        rgb_area_part_size = 0
        rgb_area_part_size_Max = 0
        rgb_area_main_part_index = 0
        RGBAreaFullSize = 0
        #[(0,0,0),[(0,0),(0,0),(0,0),0]]) #[RGB, [_startPoint, PointOfGravity, NearestPointOfGravity, Count]]
        for iRGBContent in range(len(all_seed_info[iRGBList])):
            rgb_area_part_size = all_seed_info[iRGBList][iRGBContent][3]
            if rgb_area_part_size > rgb_area_part_size_Max:
                rgb_area_part_size_Max = rgb_area_part_size
                rgb_area_main_part_index = iRGBContent
                rgb_area_main_start_point = all_seed_info[iRGBList][iRGBContent][0]
                rgb_area_main_POG = all_seed_info[iRGBList][iRGBContent][1]
                rgb_area_main_POG_in_area = all_seed_info[iRGBList][iRGBContent][2]
                rgb_area_part_size_MaxSize = all_seed_info[iRGBList][iRGBContent][3]
            RGBAreaFullSize = max(RGBAreaFullSize , rgb_area_part_size)
            rgb_area_main_RGB = all_RGB_list[iRGBList]


        #if color is land
        #definition_color_address
        original_color = all_RGB_list[iRGBList]
        bolIsProvinceLand = is_province_land(original_color, definition_color_address['RGB'], definition_color_address['land_sea_lake'])
        bolIsProvinceCoast = is_province_coast(original_color, definition_color_address['RGB'], definition_color_address['coast'])

        if bolIsProvinceLand:
            new_max_new_provinces_per_state = correct_new_province_max_amount(max_new_provinces_per_state, rgb_area_main_RGB, definition_info_dict, states_info_dict)
            new_province_max_amount = calculate_divide_province_amount(image_height, default_province_size, longitude_north2D, longitude_south2D, rgb_area_main_POG, RGBAreaFullSize, new_max_new_provinces_per_state)
        else:
            new_province_max_amount = 1
        
        if new_province_max_amount > 1:
            #all_cores_of_seed_list.append([])
            all_seeds_original_color_list.append(all_RGB_list[iRGBList])
            
            rgb_area_p = []
            rgb_area_p, pixels = floodfill(pixels, rgb_area_main_RGB, (0,0,0), image_width, image_height, rgb_area_main_start_point[0], rgb_area_main_start_point[1])
            #create seed
            coreOfSeed = []
            #bolFixTheFirstSeedPosition = False
            
            if bolIsProvinceCoast:
                coast_points_collection = get_coast_points_collection(rgb_area_main_RGB, all_seed_info[iRGBList][0][4], pixels, definition_color_address['RGB'], definition_color_address['land_sea_lake'])

                if len(all_seed_info[iRGBList]) > 1: # >2 #area has one or more small parts 
                    RGBAreaPartRestJointPointOfGravity = calculate_joint_POG(all_seed_info[iRGBList], rgb_area_main_part_index)
                    nearestPointOfGravityOfSmallPart = get_nearest_POGOfSmallPartOnMainBlock(RGBAreaPartRestJointPointOfGravity, coast_points_collection)
                    coreOfSeed.append(nearestPointOfGravityOfSmallPart)
                    #smallPartWaitChangeAmount = RGBAreaFullSize - rgb_area_part_size_MaxSize
                    for item in range(1, new_province_max_amount):
                        coreOfSeed.append(rgb_area_main_POG_in_area)
                    coreOfNewSeed = []
                    startItem = 1
                    coreOfNewSeed = no_iteration_get_seed(iterate_amount, startItem, coreOfSeed, rgb_area_p)

                else:
                    coreOfSeed.append(coast_points_collection[0]) #TODO
                    for item in range(1, new_province_max_amount):
                        coreOfSeed.append(rgb_area_main_POG_in_area)
                        coreOfNewSeed = []
                        startItem = 1 #TODO move POG
                        coreOfNewSeed = no_iteration_get_seed(iterate_amount, startItem, coreOfSeed, rgb_area_p)

            else:
                if len(all_seed_info[iRGBList]) > 1: # >2 #area has one or more small parts 
                    RGBAreaPartRestJointPointOfGravity = calculate_joint_POG(all_seed_info[iRGBList], rgb_area_main_part_index)
                    nearestPointOfGravityOfSmallPart = get_nearest_POGOfSmallPartOnMainBlock(RGBAreaPartRestJointPointOfGravity, rgb_area_p)
                    coreOfSeed.append(nearestPointOfGravityOfSmallPart)
                    #smallPartWaitChangeAmount = RGBAreaFullSize - rgb_area_part_size_MaxSize
                    for item in range(1, new_province_max_amount):
                        coreOfSeed.append(rgb_area_main_POG_in_area)
                    coreOfNewSeed = []
                    startItem = 1
                    coreOfNewSeed = no_iteration_get_seed(iterate_amount, startItem, coreOfSeed, rgb_area_p)

                else:
                    for item in range(0, new_province_max_amount):
                        coreOfSeed.append(rgb_area_main_POG_in_area)
                    coreOfNewSeed = []
                    startItem = 0 #TODO move POG
                    coreOfNewSeed = no_iteration_get_seed(iterate_amount, startItem, coreOfSeed, rgb_area_p)
                
            #all_cores_of_seed_list[count].append(coreOfNewSeed)
            all_cores_of_seed_list.append(coreOfNewSeed)
            #count = count + 1
            print(time() - t)

    #all_seeds_original_color_list
    #all_cores_of_seed_list

    all_new_seeds_dict = {
        'Original Color': all_seeds_original_color_list,
        'Seeds Position': all_cores_of_seed_list
    }


    save_dict(all_new_seeds_dict, 'all_new_seeds_dict')
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #if not os.path.exists(temp_folder_location):
    #    os.makedirs(temp_folder_location)
    #full_file_name = temp_folder_location + "\\all_new_seeds_dict.txt"
    #joblib.dump(all_new_seeds_dict, full_file_name)
    #fp = open(full_file_name, 'wb')
    #pickle.dump(all_new_seeds_dict, fp)
    #fp.close()
    print('Part 3 finished')
    #return all_new_seeds_dict

## PART 4 ##

## PART 4 ##

def create_seed_color_dict(original_color, coreOfSeed, all_aviliable_RGB, all_used_RGB, count_create_seed_color_dict):
    choosed_color = []
    choosed_color.append(original_color)
    for i in range(1, len(coreOfSeed)):
        for j in range(count_create_seed_color_dict, len(all_aviliable_RGB)):
            if not(all_aviliable_RGB[j] in all_used_RGB):
                count_create_seed_color_dict =  j
                choosed_color.append(all_aviliable_RGB[j])
                all_used_RGB.append(all_aviliable_RGB[j])
                break

    seed_color_dict = {
        'Seed Position': coreOfSeed,
        'Color': choosed_color
    }

    return seed_color_dict, all_used_RGB, count_create_seed_color_dict

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
                        distance = calculate_P2P_distance(painting_area_for_loop[item], seeds_position_list[i])
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

def get_seeds_painting_area_v2(all_used_RGB, all_used_RGB_info, seeds_position_list, seeds_color_list):
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
    
    seeds_stack_list = []
    for i in range(len(seeds_position_list)):
        #seeds_stack_list.append([])
        x = seeds_position_list[i][0]
        y = seeds_position_list[i][1]
        seeds_stack_list.append([[x, y]])
        #seeds_stack_list[0].append((1,1))

    distance_points2seeds = []
    for i in range(len(seeds_position_list)):
        distance_points2seeds.append([])
        for j in range(len(painting_area_for_loop)):
            #p2s_distance = calculate_P2P_distance(painting_area_for_loop[j], seeds_position_list[i]) + random.uniform(-0.1,0.1)
            p2s_distance = calculate_P2P_distance(painting_area_for_loop[j], seeds_position_list[i])
            distance_points2seeds[i].append((painting_area_for_loop[j],p2s_distance))

    distance_group_point2seed = []
    for i in range(len(seeds_position_list)):
        #distance_group_point2seed.append(random.uniform(-0.1,0.1))
        distance_group_point2seed.append(0)
    distance_group_point2seed[0] = -1

    while sum(is_seeds_expand_end) < len(is_seeds_expand_end):
        min_index = distance_group_point2seed.index(min(distance_group_point2seed))
        if len(seeds_stack_list[min_index]) == 0:
            is_seeds_expand_end[min_index] = True
            distance_group_point2seed[min_index] = 999999999999
        else:
            pixel_position = seeds_stack_list[min_index].pop()
            x = pixel_position[0]
            y = pixel_position[1]
            if pixel_position in painting_area_for_loop:
                pixel_position_index = painting_area_for_loop.index(pixel_position)
                pixel_position_color = painting_area_is_painted[pixel_position_index]
                if pixel_position_color == False:
                    painting_area_is_painted[pixel_position_index] = seeds_color_list[min_index]

                    list_for_sorted = []
                    list_for_sorted = seeds_stack_list[min_index].copy()
                    list_for_sorted.reverse()
                    north_pixel = [x, y+1]
                    south_pixel = [x, y-1]
                    west_pixel = [x-1, y]
                    east_pixel = [x+1, y]
                    if north_pixel in painting_area_for_loop:
                        list_for_sorted.append(north_pixel)
                    if south_pixel in painting_area_for_loop:
                        list_for_sorted.append(south_pixel)
                    if west_pixel in painting_area_for_loop:
                        list_for_sorted.append(west_pixel)
                    if east_pixel in painting_area_for_loop:
                        list_for_sorted.append(east_pixel)

                    #list_for_sorted.append([x, y+1])
                    #list_for_sorted.append([x, y-1])
                    #list_for_sorted.append([x-1, y])
                    #list_for_sorted.append([x+1, y])
                    if len(list_for_sorted) ==0:
                        is_seeds_expand_end[min_index] = True
                        distance_group_point2seed[min_index] = 999999999999
                    else:
                        index2 = painting_area_for_loop.index(list_for_sorted[0])
                        p2s_distance = distance_points2seeds[min_index][index2][1]
                        distance_group_point2seed[min_index] = p2s_distance

                    list_for_sorted.reverse()
                    #seeds_stack_list[min_index] = []
                    seeds_stack_list[min_index] = list_for_sorted.copy()

                    #list_for_sorted = []
                    #p2s_distance_group = []
                    #for j in range(len(seeds_stack_list[min_index])):
                    #    if seeds_stack_list[min_index][j] in painting_area_for_loop:
                    #        pixel_position_index = painting_area_for_loop.index(seeds_stack_list[min_index][j])
                    #        pixel_position_color = painting_area_is_painted[pixel_position_index]
                    #        if pixel_position_color == False:
                    #            index2 = painting_area_for_loop.index(seeds_stack_list[min_index][j])
                    #            p2s_distance = distance_points2seeds[min_index][index2][1]
                    #            list_for_sorted.append((seeds_stack_list[min_index][j], p2s_distance))
                    #            p2s_distance_group.append(p2s_distance)
                    #            distance_group_point2seed[min_index] = min(p2s_distance_group)
                    #new_list_for_sorted = sorted(list_for_sorted, key=lambda s: s[1], reverse = True)
                    #seeds_stack_list[min_index] = []
                    #if len(new_list_for_sorted) != 0:
                    #    for j in range(len(new_list_for_sorted)):
                    #        seeds_stack_list[min_index].append(new_list_for_sorted[j][0])




    for i in range(len(painting_area_is_painted)):
        if painting_area_is_painted[i] == (0,0,0):
            painting_area_is_painted[i] = original_color


    return original_color, painting_area, painting_area_is_painted



def step_get_seeds_painting_area():
    #all_RGB_and_Area_list
    #used_RGB_list
    print('Part 4')
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #full_file_name = temp_folder_location + "\\all_RGB_and_Area_dict.txt"
    #with open(full_file_name, 'wb') as fp:
    #all_RGB_and_Area_dict = joblib.load(full_file_name)
    #full_file_name = temp_folder_location + "\\all_new_seeds_dict.txt"
    #with open(full_file_name, 'wb') as fp:
    #all_new_seeds_dict = joblib.load(full_file_name)
    all_RGB_and_Area_dict = read_dict('all_RGB_and_Area_dict')
    all_new_seeds_dict = read_dict('all_new_seeds_dict')
    
    all_used_RGB = all_RGB_and_Area_dict['RGB']
    all_used_RGB_info = all_RGB_and_Area_dict['Seeds Info']
    all_new_seeds_original_RGB = all_new_seeds_dict['Original Color']
    all_new_seeds_position = all_new_seeds_dict['Seeds Position']

    #import avaliable RGB file
    title = "Open avaliable RGB file(all_RGB_list.txt)"
    filetypes = {("avaliable RGB file", ".txt")}
    all_text_str = open_file_return_str(title, filetypes)
    all_text_str = split_str_into_list(all_text_str, ';')
    all_aviliable_RGB = __splitRGBOutOfLst2(all_text_str)

    all_painting_area_position = []
    all_painting_area_color = []
    all_painting_area_original_color = []
    all_painting_area_new_color = []
    count_create_seed_color_dict =  0
    for i in range(len(all_new_seeds_original_RGB)):
        t = time()
        print("Part 4：get painting area for every seeds : Color = " + str(i) + ' / ' + str(len(all_new_seeds_original_RGB)))
        
        seed_color_dict, all_used_RGB, count_create_seed_color_dict = create_seed_color_dict(all_new_seeds_original_RGB[i], all_new_seeds_position[i], all_aviliable_RGB, all_used_RGB, count_create_seed_color_dict)

        seeds_position_list = seed_color_dict['Seed Position']
        seeds_color_list = seed_color_dict['Color']

        #OMG cost too much cpu time flood fill
        #original_color, painting_area_position, painting_area_color = get_seeds_painting_area(all_used_RGB, all_used_RGB_info, seeds_position_list, seeds_color_list)
        original_color, painting_area_position, painting_area_color = get_seeds_painting_area_v2(all_used_RGB, all_used_RGB_info, seeds_position_list, seeds_color_list)

        all_painting_area_original_color.append(original_color)
        all_painting_area_position.append(painting_area_position)
        all_painting_area_color.append(painting_area_color)
        temp = seeds_color_list.copy()
        temp.remove((0,0,0))
        all_painting_area_new_color.append(temp)

        print(time() - t)

    all_painting_area_dict = {
        'Painting area original color': all_painting_area_original_color,
        'Painting area position': all_painting_area_position,
        'Painting area color': all_painting_area_color,
        'Painting area new color': all_painting_area_new_color
    }

    all_painting_area_dict_small = {
        'Painting area original color': all_painting_area_original_color,
        'Painting area new color': all_painting_area_new_color
    }
    all_painting_area_dict_small = []
    for i in range(len(all_painting_area_original_color)):
        temp = []
        temp.append(all_painting_area_original_color[i])
        for j in range(len(all_painting_area_new_color[i])):
            temp.append(all_painting_area_new_color[i][j])
        all_painting_area_dict_small.append(temp)

    save_dict(all_painting_area_dict, 'all_painting_area_dict')
    save_dict(all_painting_area_dict_small, 'all_painting_area_dict_small')
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #if not os.path.exists(temp_folder_location):
    #    os.makedirs(temp_folder_location)
    #full_file_name = temp_folder_location + "\\all_painting_area_dict.txt"
    #joblib.dump(all_painting_area_dict, full_file_name)
    #full_file_name = temp_folder_location + "\\all_painting_area_dict_small.txt"
    #joblib.dump(all_painting_area_dict_small, full_file_name)
    #with open(temp_folder_location + "\\all_painting_area_dict.txt", "wb") as fp1:   #Pickling
    print('Part 4 finished')
    #return all_painting_area_dict, all_painting_area_dict_small

def painting_pixels():
    print('Part 5')
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
    print('Part 5 finished')

## PART 6 ##

## PART 6 ##
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
    print('Part 6')

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

    print('Part 6 finished')

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
    
