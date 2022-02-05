from tkinter import filedialog
from PIL import Image #pip install Pillow
from core import read_write_files
from core import step2_genetate_rgb_area


def read_supply_lines():
    print('Part 8')

    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = read_write_files.open_file_return_str(title, filetypes)
    all_text_list = read_write_files.split_str_into_list(all_text_str, ';')
    definition_color_address = read_write_files.split_info_definition_csv(all_text_list)
    

    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (provinces.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_width, image_height = im.size

    connected_provinces = []
    for j in range(2, image_height - 1):
        print('checking line ', j, ' of ', image_height )
        last_right_pair = []
        last_under_pair = []
        for i in range(2, image_width - 1):
            color_center = list(pixels[i,j])
            center_province_ID = definition_color_address['RGB'].index(color_center)
            if definition_color_address['land_sea_lake'][center_province_ID] == 'land':

                color_right = list(pixels[i+1,j])
                right_province_ID = definition_color_address['RGB'].index(color_right)
                if definition_color_address['land_sea_lake'][right_province_ID] == 'land':
                    if center_province_ID != right_province_ID:
                        if [center_province_ID, right_province_ID] not in connected_provinces:
                            connected_provinces.append([center_province_ID, right_province_ID])

                color_under = list(pixels[i,j+1])
                under_province_ID = definition_color_address['RGB'].index(color_under)
                if definition_color_address['land_sea_lake'][under_province_ID] == 'land':
                    if center_province_ID != under_province_ID:
                        if [center_province_ID, under_province_ID] not in connected_provinces:
                            connected_provinces.append([center_province_ID, under_province_ID])

    connected_provinces.sort()
    read_write_files.save_dict(connected_provinces, 'connected_provinces')


def find_connect_railway_between_two_points_v1(start_point, end_point, connected_provinces):
    
    connected_provinces_start_province = []
    connected_provinces_end_province = []
    for count, value in enumerate(connected_provinces):
        connected_provinces_start_province.append(value[0])
        connected_provinces_end_province.append(value[1])

    start_point_location = [i for i, x in enumerate(connected_provinces_start_province) if x == int(start_point)]

    for item in start_point_location:
        mid_point1 = connected_provinces_end_province[item]
        if mid_point1 == int(end_point):
            start_point = str(start_point)
            return start_point # level 1 succeed

    for item in start_point_location:
        mid_point1 = connected_provinces_end_province[item]
        mid_point1_location = [i for i, x in enumerate(connected_provinces_start_province) if x == int(mid_point1)]
        for item in mid_point1_location:
            mid_point2 = connected_provinces_end_province[item]
            if mid_point2 == int(end_point):
                start_point = str(start_point) + ' ' + str(mid_point1)
                return start_point # level 2 succeed


    for item in start_point_location:
        mid_point1 = connected_provinces_end_province[item]
        mid_point1_location = [i for i, x in enumerate(connected_provinces_start_province) if x == int(mid_point1)]
        for item in mid_point1_location:
            mid_point2 = connected_provinces_end_province[item]
            mid_point2_location = [i for i, x in enumerate(connected_provinces_start_province) if x == int(mid_point2)]
            for item in mid_point2_location:
                mid_point3 = connected_provinces_end_province[item]
                if mid_point3 == int(end_point):
                    start_point = str(start_point) + ' ' + str(mid_point1) + ' ' + str(mid_point2)
                    return start_point # level 3 succeed


    for item in start_point_location:
        mid_point1 = connected_provinces_end_province[item]
        mid_point1_location = [i for i, x in enumerate(connected_provinces_start_province) if x == int(mid_point1)]
        for item in mid_point1_location:
            mid_point2 = connected_provinces_end_province[item]
            mid_point2_location = [i for i, x in enumerate(connected_provinces_start_province) if x == int(mid_point2)]
            for item in mid_point2_location:
                mid_point3 = connected_provinces_end_province[item]
                mid_point3_location = [i for i, x in enumerate(connected_provinces_start_province) if x == int(mid_point3)]
                for item in mid_point3_location:
                    mid_point4 = connected_provinces_end_province[item]
                    if mid_point4 == int(end_point):
                        start_point = str(start_point) + ' ' + str(mid_point1) + ' ' + str(mid_point2) + ' ' + str(mid_point3)
                        return start_point # level 4 succeed



    return start_point




def find_connect_railway_between_two_points_v2(start_point_province_ID, end_point_province_ID, definition_color_address, all_RGB_list, all_seed_info, pixels):
    start_point_province_RGB = definition_color_address['RGB'][int(start_point_province_ID)]
    temp = all_RGB_list.index(start_point_province_RGB)
    start_point_POG = all_seed_info[temp][0][2]
    end_point_province_RGB = definition_color_address['RGB'][int(end_point_province_ID)]
    temp = all_RGB_list.index(end_point_province_RGB)
    end_point_POG = all_seed_info[temp][0][2]

    passing_points = []
    x_rate = 10
    step_x = 1
    if start_point_POG[0] > end_point_POG[0]:
        step_x = -1
    else:
        step_x = 1
    step_y = 1
    if start_point_POG[1] > end_point_POG[1]:
        step_y = -1
    else:
        step_y = 1
    for x_10 in range(x_rate*(start_point_POG[0]), x_rate*(end_point_POG[0]), step_x):
        if start_point_POG[0] == end_point_POG[0]:
            for j in (start_point_POG[1], end_point_POG[1], step_y):
                passing_points.append(start_point_POG[0], j)
        else:
            y = round(start_point_POG[1] + (end_point_POG[1] - start_point_POG[1])/(end_point_POG[0] - start_point_POG[0]) * (x_10/x_rate - start_point_POG[0]))
            x = round(x_10/10)
            passing_points.append([x, y])

    passing_points_no_duplicate = []
    for item in passing_points:
        if item not in passing_points_no_duplicate:
            passing_points_no_duplicate.append(item)

    passing_point_province_ID_list = []
    for item in passing_points_no_duplicate:
        passing_point_RGB = pixels[item[0], item[1]]
        passing_point_province_ID = definition_color_address['RGB'].index(list(passing_point_RGB))
        if passing_point_province_ID != int(start_point_province_ID) and passing_point_province_ID != int(end_point_province_ID):
            passing_point_province_ID_list.append(str(passing_point_province_ID))

    passing_point_province_ID_list_no_duplicate = []
    for item in passing_point_province_ID_list:
        if item not in passing_point_province_ID_list_no_duplicate:
            passing_point_province_ID_list_no_duplicate.append(item)

    return passing_point_province_ID_list_no_duplicate





def calculate_topology_between_provinces():
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = read_write_files.open_file_return_str(title, filetypes)
    all_text_list = read_write_files.split_str_into_list(all_text_str, ';')
    definition_color_address = read_write_files.split_info_definition_csv(all_text_list)

    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (provinces.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_width, image_height = im.size

    province_topology = []
    for check_Y in range(0, image_height-1):
        print('Checking Line '+ str(check_Y) + ' of ' + str(image_height))
        for check_X in range(0, image_width-1):
            check_point_color = list(pixels[check_X,check_Y])
            check_point_color_right = list(pixels[check_X + 1,check_Y])
            check_point_color_under = list(pixels[check_X ,check_Y + 1])
            check_point_province_ID = definition_color_address['province ID'][definition_color_address['RGB'].index(check_point_color)]
            check_point_type =  definition_color_address['land_sea_lake'][definition_color_address['RGB'].index(check_point_color)]

            if check_point_type == 'land':

                if check_point_color != check_point_color_right:
                    check_point_province_ID_right = definition_color_address['province ID'][definition_color_address['RGB'].index(check_point_color_right)]
                    check_point_type_right =  definition_color_address['land_sea_lake'][definition_color_address['RGB'].index(check_point_color_right)]
                    if check_point_type_right == 'land':
                        two_province_topology = [check_point_province_ID, check_point_province_ID_right]
                        two_province_topology.sort()
                        if two_province_topology not in province_topology:
                            province_topology.append(two_province_topology)

                if check_point_color != check_point_color_under:
                    check_point_province_ID_under = definition_color_address['province ID'][definition_color_address['RGB'].index(check_point_color_under)]
                    check_point_type_under =  definition_color_address['land_sea_lake'][definition_color_address['RGB'].index(check_point_color_under)]
                    if check_point_type_under == 'land':
                        two_province_topology = [check_point_province_ID, check_point_province_ID_under]
                        two_province_topology.sort()
                        if two_province_topology not in province_topology:
                            province_topology.append(two_province_topology)


    read_write_files.save_dict(province_topology, 'province_topology')


def railway_recursion(temp_list, recursion_depth, route, one_railways_list, province_topology, start_point_province_ID, end_point_province_ID):
    connected_province = [start_point_province_ID, end_point_province_ID]
    connected_province.sort()
    recursion_depth = recursion_depth + 1
    possible_targets = []
    if connected_province in province_topology:
        temp_list = temp_list[::-1]
        temp_list.append(start_point_province_ID)
        temp_list = temp_list[::-1]
        return temp_list
    else:
        for item1, value1 in enumerate(province_topology):
            if int(start_point_province_ID) in value1:
                possible_targets.append(value1)
        for item2, value2 in enumerate(possible_targets):
            if possible_targets[item2][0] == int(start_point_province_ID):
                check_new_railway_point = possible_targets[item2][1]
            else:
                check_new_railway_point = possible_targets[item2][0]
            temp_list = temp_list[::-1]
            temp_list.append(railway_recursion(temp_list, recursion_depth, route, one_railways_list, province_topology, check_new_railway_point, end_point_province_ID))
            temp_list = temp_list[::-1]
            return temp_list


def get_new_railway_points(province_topology, start_point_province_ID, one_railways_list):
    possible_targets = []
    new_railway_points = []
    for item1, value1 in enumerate(province_topology):
        if int(start_point_province_ID) in value1:
            possible_targets.append(value1)
    for item2, value2 in enumerate(possible_targets):
        if possible_targets[item2][0] == int(start_point_province_ID):
            check_new_railway_point = possible_targets[item2][1]
        else:
            check_new_railway_point = possible_targets[item2][0]
        if str(check_new_railway_point) in one_railways_list:
            a = 1
        else:
            new_railway_points.append(check_new_railway_point)
    return new_railway_points

def modify_supply_lines_V2():
    province_topology = read_write_files.read_dict('province_topology')
    province_topology.sort()
    title = "Open railways file(railways.txt)"
    filetypes = {("railways file", ".txt")}
    railways_str = read_write_files.open_file_return_str(title, filetypes)
    railways_list = read_write_files.split_str_into_list(railways_str, ' ')
    new_railways_string = ''

    for i in range(len(railways_list)):
        print('Calculate ' + str(i) + ' of ' + str(len(railways_list)))
        railways_points_len = len(railways_list[i])
        railways_points_level = railways_list[i][0]
        one_railways_list = railways_list[i][2:railways_points_len - 1]
        real_end_point_province_ID = railways_list[i][railways_points_len - 2]

        new_connect_provinces = []
        new_connect_provinces.append(railways_list[i][2])

        new_connect_provinces_list = []

        for j in range(2, railways_points_len - 2): #(2,6) = 2 3 4 5
            start_point_province_ID = int(railways_list[i][j])
            end_point_province_ID = int(railways_list[i][j+1])
            connected_province = [start_point_province_ID, end_point_province_ID]
            connected_province.sort()
            if connected_province in province_topology:
                a = 1 #next
                new_connect_provinces.append(end_point_province_ID)
            else:
                possible_targets1 = get_new_railway_points(province_topology, start_point_province_ID, one_railways_list)
                for item, value1 in enumerate(possible_targets1):
                    connected_province = [value1, end_point_province_ID]
                    connected_province.sort()
                    if connected_province in province_topology:
                        new_connect_provinces_list.append([value1])
                    else:
                        possible_targets2 = get_new_railway_points(province_topology, value1, one_railways_list)
                        for item, value2 in enumerate(possible_targets2):
                            connected_province = [value2, end_point_province_ID]
                            connected_province.sort()
                            if connected_province in province_topology:
                                new_connect_provinces_list.append([value1, value2])
                            else:
                                possible_targets3 = get_new_railway_points(province_topology, value2, one_railways_list)
                                for item, value3 in enumerate(possible_targets3):
                                    connected_province = [value3, end_point_province_ID]
                                    connected_province.sort()
                                    if connected_province in province_topology:
                                        new_connect_provinces_list.append([value1, value2, value3])
                                    else:
                                        possible_targets4 = get_new_railway_points(province_topology, value3, one_railways_list)
                                        for item, value4 in enumerate(possible_targets3):
                                            connected_province = [value4, end_point_province_ID]
                                            connected_province.sort()
                                            if connected_province in province_topology:
                                                new_connect_provinces_list.append([value1, value2, value3, value4])
                                            #else:
                                                #new_connect_provinces_list.append('NOT FOUND')

                chosen_railway = []
                if new_connect_provinces_list == []: #still not found
                    new_connect_provinces.append('TODO')
                    new_connect_provinces.append(end_point_province_ID)
                else:
                    item_min = len(new_connect_provinces_list[0])
                    chosen_railway = new_connect_provinces_list[0]
                    for item, value in enumerate(new_connect_provinces_list):
                        if len(value) < item_min:
                            item_min = len(value)
                            chosen_railway = value
                    for item, value in enumerate(chosen_railway):
                        new_connect_provinces.append(value)
                    new_connect_provinces.append(end_point_province_ID)

        new_railways_string = new_railways_string + str(railways_points_level) + ' ' + str(len(new_connect_provinces)) + ' ' 
        for item, value in enumerate(new_connect_provinces):
            new_railways_string = new_railways_string + str(value) + ' '
        if len(set(new_connect_provinces)) < len(new_connect_provinces):
            new_railways_string = new_railways_string + 'TODO '
        new_railways_string = new_railways_string + '\r\n'
        a = 1
    a = 1

    save_file = filedialog.asksaveasfilename(title = "save railways.txt")
    with open(save_file, 'w') as filehandle:
        filehandle.write(new_railways_string)
    filehandle.close()
    print('Part 8 finished')







def modify_supply_lines():
    title = "Open railways file(railways.txt)"
    filetypes = {("railways file", ".txt")}
    railways_str = read_write_files.open_file_return_str(title, filetypes)
    railways_list = read_write_files.split_str_into_list(railways_str, ' ')
    #connected_provinces = read_write_files.read_dict('connected_provinces')
    
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = read_write_files.open_file_return_str(title, filetypes)
    all_text_list = read_write_files.split_str_into_list(all_text_str, ';')
    definition_color_address = read_write_files.split_info_definition_csv(all_text_list)

    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (provinces.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_width, image_height = im.size

    # do it before
    # step2_genetate_rgb_area.step_get_RGB_area_for_every_color()
    all_RGB_and_Area_dict = read_write_files.read_dict('all_RGB_and_Area_dict')
    all_RGB_list = all_RGB_and_Area_dict['RGB']
    all_seed_info = all_RGB_and_Area_dict['Seeds Info']


    for i in range(len(railways_list)):
        print('Calculate ' + str(i) + ' of ' + str(len(railways_list)))
        railways_points_len = len(railways_list[i])
        railways_points_level = railways_list[i][0]
        railways_points_amount = railways_list[i][1]
        real_end_point_province_ID = railways_list[i][railways_points_len - 2]

        for j in range(2, railways_points_len - 2): #(2,6) = 2 3 4 5
            start_point_province_ID = railways_list[i][j]
            end_point_province_ID = railways_list[i][j+1]

            #debug
            if start_point_province_ID == '3522':
                a = 1

            passing_point_province_ID_list = find_connect_railway_between_two_points_v2(start_point_province_ID, end_point_province_ID, definition_color_address, all_RGB_list, all_seed_info, pixels)

            new_railway = str(start_point_province_ID) + ' '
            for item in passing_point_province_ID_list:
                if item == []:
                    new_railway = new_railway + str(item) + ' '
                else:
                    check_passing_point_province_ID_list = find_connect_railway_between_two_points_v2(item, real_end_point_province_ID, definition_color_address, all_RGB_list, all_seed_info, pixels)
                    if check_passing_point_province_ID_list == []:
                        new_railway = new_railway = new_railway + str(item) + ' ' + str(real_end_point_province_ID)+ ' '
                    else:
                        new_railway = new_railway + str(item) + ' '

            railways_list[i][j] = new_railway
        #remove space at end
        for j in range(len(railways_list[i])):
            if railways_list[i][j][-1] == ' ':
                railways_list[i][j] = railways_list[i][j][:-1]

        new_railway_string = ' '.join(str(v) for v in railways_list[i])
        #new_railway_string = ' '.join(railways_list[i])
        new_railway_sorted_list = []
        new_railway_full_list = new_railway_string.split(' ')
        new_railway_sorted_list.append(new_railway_full_list[0])
        new_railway_sorted_list.append(new_railway_full_list[1])
        railway_count = 0
        no_more = 0
        for j in range(2, len(new_railway_full_list)):
            if no_more == 0:
                if new_railway_full_list[j] != end_point_province_ID:
                    new_railway_sorted_list.append(new_railway_full_list[j])
                    railway_count = railway_count + 1
                else:
                    no_more = 1
                    new_railway_sorted_list.append(end_point_province_ID)
                    railway_count = railway_count + 1

        new_railway_sorted_list2 = []
        new_railway_sorted_list2.append(new_railway_sorted_list[0])
        new_railway_sorted_list2.append(new_railway_sorted_list[1])
        for j in range(2, len(new_railway_sorted_list)):
            if definition_color_address['land_sea_lake'][int(new_railway_sorted_list[j])] == 'land':
                new_railway_sorted_list2.append(new_railway_sorted_list[j])
            else:
                railway_count = railway_count - 1
            
        railways_list[i] = new_railway_sorted_list2


        railways_list[i][1] = str(railway_count)
        if railways_list[i][-1] != '\n':
            railways_list[i].append('\n')



    new_railways_string = ''
    for item in railways_list:
        new_railways_string = new_railways_string + ' '.join(str(v) for v in item)

    save_file = filedialog.asksaveasfilename(title = "save railways.txt")
    with open(save_file, 'w') as filehandle:
        filehandle.write(new_railways_string)
    filehandle.close()
    print('Part 8 finished')

