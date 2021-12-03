from core import read_files
import step2_genetate_rgb_area
from time import time

def step_get_seeds_painting_area():
    #all_RGB_and_Area_list
    #used_RGB_list
    print('Part 5')
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #full_file_name = temp_folder_location + "\\all_RGB_and_Area_dict.txt"
    #with open(full_file_name, 'wb') as fp:
    #all_RGB_and_Area_dict = joblib.load(full_file_name)
    #full_file_name = temp_folder_location + "\\all_new_seeds_dict.txt"
    #with open(full_file_name, 'wb') as fp:
    #all_new_seeds_dict = joblib.load(full_file_name)
    all_RGB_and_Area_dict = read_files.read_dict('all_RGB_and_Area_dict')
    all_new_seeds_dict = read_files.read_dict('all_new_seeds_dict')
    
    all_used_RGB = all_RGB_and_Area_dict['RGB']
    all_used_RGB_info = all_RGB_and_Area_dict['Seeds Info']
    all_new_seeds_original_RGB = all_new_seeds_dict['Original Color']
    all_new_seeds_position = all_new_seeds_dict['Seeds Position']

    #import avaliable RGB file
    title = "Open avaliable RGB file(all_RGB_list.txt)"
    filetypes = {("avaliable RGB file", ".txt")}
    all_text_str = read_files.open_file_return_str(title, filetypes)
    all_text_str = read_files.split_str_into_list(all_text_str, ';')
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

    read_files.save_dict(all_painting_area_dict, 'all_painting_area_dict')
    read_files.save_dict(all_painting_area_dict_small, 'all_painting_area_dict_small')
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #if not os.path.exists(temp_folder_location):
    #    os.makedirs(temp_folder_location)
    #full_file_name = temp_folder_location + "\\all_painting_area_dict.txt"
    #joblib.dump(all_painting_area_dict, full_file_name)
    #full_file_name = temp_folder_location + "\\all_painting_area_dict_small.txt"
    #joblib.dump(all_painting_area_dict_small, full_file_name)
    #with open(temp_folder_location + "\\all_painting_area_dict.txt", "wb") as fp1:   #Pickling
    print('Part 5 finished')
    #return all_painting_area_dict, all_painting_area_dict_small



def __splitRGBOutOfLst2(all_text_list):
    allRGBInLst = []
    for i in range(len(all_text_list)):
        R = int(all_text_list[i][0])
        G = int(all_text_list[i][1])
        B = int(all_text_list[i][2])
        allRGBInLst.append((R,G,B))
    return allRGBInLst

    
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
            #p2s_distance = step2_genetate_rgb_area.calculate_P2P_distance(painting_area_for_loop[j], seeds_position_list[i]) + random.uniform(-0.1,0.1)
            p2s_distance = step2_genetate_rgb_area.calculate_P2P_distance(painting_area_for_loop[j], seeds_position_list[i])
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



