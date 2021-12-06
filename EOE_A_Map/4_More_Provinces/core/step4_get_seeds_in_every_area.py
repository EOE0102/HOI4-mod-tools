from core import read_write_files
from tkinter import filedialog
from core import parameter
from itertools import product


from time import time
from PIL import Image #pip install Pillow
from core import step2_genetate_rgb_area
## PART 4 ##


def step_get_seeds_in_every_area():
    #all_RGB_and_Area_list

    all_RGB_and_Area_dict = read_write_files.read_dict('all_RGB_and_Area_dict')
    all_RGB_list = all_RGB_and_Area_dict['RGB']
    all_seed_info = all_RGB_and_Area_dict['Seeds Info']
    #Open definition.csv#
    #exp: 4;0;0;232;sea;true;ocean;0
    # index;R;G;B;land/sea/lake;coast?;terrain;continent
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = read_write_files.open_file_return_str(title, filetypes)
    all_text_list = read_write_files.split_str_into_list(all_text_str, ';')
    definition_color_address = read_write_files.split_info_definition_csv(all_text_list)

    states_info_dict = read_write_files.read_dict('states_info_dict')
    definition_info_dict = read_write_files.read_dict('definition_info_dict')

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
    all_cores_of_seed_list = []
    all_seeds_original_color_list = []
    
    for iRGBList in range(len(all_RGB_list)):


        #debug
        if iRGBList == 182:
            a = 1


        print("Part 4：get painting seeds location for every color : Color = " + str(iRGBList + 1) + ' / ' + str(len(all_RGB_list)))
        #t = time()
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
            new_max_new_provinces_per_state, new_state_info_terrain = parameter.correct_new_province_max_amount(parameter.max_new_provinces_per_state, rgb_area_main_RGB, definition_info_dict, states_info_dict)
            new_province_max_amount = parameter.calculate_divide_province_amount(image_height, parameter.default_province_size, parameter.longitude_north2D, parameter.longitude_south2D, rgb_area_main_POG, RGBAreaFullSize, new_max_new_provinces_per_state, new_state_info_terrain)

        else:
            new_province_max_amount = 1
        
        if new_province_max_amount > 1:
            #all_cores_of_seed_list.append([])
            all_seeds_original_color_list.append(all_RGB_list[iRGBList])
            
            rgb_area_p = []
            rgb_area_p, pixels = step2_genetate_rgb_area.floodfill(pixels, rgb_area_main_RGB, (0,0,0), image_width, image_height, rgb_area_main_start_point[0], rgb_area_main_start_point[1])
            #create seed
            coreOfSeed = []
            #bolFixTheFirstSeedPosition = False
            
            if len(all_seed_info[iRGBList]) > 1: # >2 #area has one or more small parts 
                RGBAreaPartRestJointPointOfGravity = calculate_joint_POG(all_seed_info[iRGBList], rgb_area_main_part_index)
                nearestPointOfGravityOfSmallPart = get_nearest_POGOfSmallPartOnMainBlock(RGBAreaPartRestJointPointOfGravity, rgb_area_p)
                coreOfSeed.append(nearestPointOfGravityOfSmallPart)
                #smallPartWaitChangeAmount = RGBAreaFullSize - rgb_area_part_size_MaxSize
                for item in range(1, new_province_max_amount):
                    coreOfSeed.append(rgb_area_main_POG_in_area)
                coreOfNewSeed = []
                startItem = 1
                if bolIsProvinceCoast: 
                    coreOfNewSeed = no_iteration_get_seed(parameter.iterate_amount, startItem, coreOfSeed, rgb_area_p)
                else:
                    coreOfNewSeed = no_iteration_get_seed(parameter.iterate_amount, startItem, coreOfSeed, rgb_area_p)

            else:
                for item in range(0, new_province_max_amount):
                    coreOfSeed.append(rgb_area_main_POG_in_area)
                coreOfNewSeed = []
                startItem = 0 #TODO move POG
                if bolIsProvinceCoast: 
                    startItem = 1
                    border_pixels = find_border_pixels(rgb_area_p)
                    coast_pixels = find_coast_pixels(border_pixels, pixels, definition_color_address)
                    coast_pixels.sort()
                    coast_seed = coast_pixels[round(len(coast_pixels)/2)]
                    coreOfSeed[0] = coast_seed
                    coreOfNewSeed = no_iteration_get_seed(parameter.iterate_amount, startItem, coreOfSeed, rgb_area_p)
                else:
                    coreOfNewSeed = no_iteration_get_seed(parameter.iterate_amount, startItem, coreOfSeed, rgb_area_p)
                
            #all_cores_of_seed_list[count].append(coreOfNewSeed)
            all_cores_of_seed_list.append(coreOfNewSeed)
            #count = count + 1
            #print(time() - t)

    #all_seeds_original_color_list
    #all_cores_of_seed_list

    all_new_seeds_dict = {
        'Original Color': all_seeds_original_color_list,
        'Seeds Position': all_cores_of_seed_list
    }


    read_write_files.save_dict(all_new_seeds_dict, 'all_new_seeds_dict')
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #if not os.path.exists(temp_folder_location):
    #    os.makedirs(temp_folder_location)
    #full_file_name = temp_folder_location + "\\all_new_seeds_dict.txt"
    #joblib.dump(all_new_seeds_dict, full_file_name)
    #fp = open(full_file_name, 'wb')
    #pickle.dump(all_new_seeds_dict, fp)
    #fp.close()
    print('Part 4 finished')
    #return all_new_seeds_dict




def find_border_pixels(rgb_area_p):
    border_pixels = []
    for item in rgb_area_p:
        x = item[0]
        y = item[1]
        point_up = [x, y-1]
        point_right = [x+1, y]
        point_down = [x, y+1]
        point_left = [x-1, y]

        if (point_up not in rgb_area_p) or (point_right not in rgb_area_p) or (point_down not in rgb_area_p) or (point_left not in rgb_area_p):
            border_pixels.append(item)

    return border_pixels


def find_coast_pixels(border_pixels, pixels, definition_color_address):
    coast_pixels = []
    
    for item in border_pixels:
        x = item[0]
        y = item[1]
        if x != 0 and x!= 5632 and y != 0 and y != 2048:
            point_up_RGB = list(pixels[x, y-1])
            point_right_RGB = list(pixels[x+1, y])
            point_down_RGB = list(pixels[x, y+1])
            point_left_RGB = list(pixels[x-1, y])
            if definition_color_address['land_sea_lake'][definition_color_address['RGB'].index(point_up_RGB)] == 'sea'\
                or definition_color_address['land_sea_lake'][definition_color_address['RGB'].index(point_right_RGB)] == 'sea'\
                or definition_color_address['land_sea_lake'][definition_color_address['RGB'].index(point_down_RGB)] == 'sea'\
                or definition_color_address['land_sea_lake'][definition_color_address['RGB'].index(point_left_RGB)] == 'sea':
                coast_pixels.append(item)
    
    return coast_pixels


def is_province_land(original_color, voll_rgb_list, land_sea_lake_type):
    index = voll_rgb_list.index(list(original_color))
    landSeaLakeType = land_sea_lake_type[index]
    if landSeaLakeType == 'land':
        return True
    else:
        return False


def is_province_coast(original_color, voll_rgb_list, coast_type):
    index = voll_rgb_list.index(list(original_color))
    CoastType = coast_type[index]
    if CoastType == 'true':
        return True
    else:
        return False


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
        distanceTemp = step2_genetate_rgb_area.calculate_P2P_distance(RGBAreaPartRestJointPointOfGravity, rgb_area_p[item])
        if distanceTemp < distance:
            distance = distanceTemp
            index = item
    nearestPointOfGravityOfSmallPart = rgb_area_p[index]
    return nearestPointOfGravityOfSmallPart

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

def no_iteration_get_seed_coast(iterate_amount, startItem, coreOfSeed, rgb_area_p):


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


def calculate_sum_p2p_energy(coreOfNewSeed):
    sum_energy = 0
    for point1, point2 in product(coreOfNewSeed, coreOfNewSeed):
        sum_energy = sum_energy + step2_genetate_rgb_area.calculate_P2P_energy(point1, point2) / 2
    return sum_energy