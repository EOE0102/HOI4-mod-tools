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


def find_connect_railway_between_two_points(start_point, end_point, connected_provinces):
    
    connected_provinces_start_province = []
    connected_provinces_end_province = []
    for count, value in enumerate(connected_provinces):
        connected_provinces_start_province.append(value[0])
        connected_provinces_end_province.append(value[1])

    start_point_location = [i for i, x in enumerate(connected_provinces_start_province) if x == int(start_point)]
    end_point_location = [i for i, x in enumerate(connected_provinces_end_province) if x == int(end_point)]



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

    pass_points = []
    for x_10 in range(10*(start_point_POG[0]), 10*(end_point_POG[0])):
        if start_point_POG[0] == end_point_POG[0]:
            for j in (start_point_POG[1] + 1, end_point_POG[2]):
                pass_points.append(start_point_POG[0], j)
        else:
            y = round(start_point_POG[1] + (end_point_POG[1] - start_point_POG[1])/(end_point_POG[0] - start_point_POG[0]) * (x_10/10 - start_point_POG[0]))
            x = round(x_10/10)
            pass_points.append([x, y])

    pass_points2 = []
    for item in pass_points:
        if item not in pass_points2:
            pass_points2.append(item)

    temp = []
    for item in pass_points2:
        passing_point_RGB = pixels[item[0], item[1]]
        passing_point_province_ID = definition_color_address['RGB'].index(list(passing_point_RGB))
        if passing_point_province_ID != int(start_point_province_ID) and passing_point_province_ID != int(end_point_province_ID):
            temp.append(str(passing_point_province_ID))
    
    passing_point_province_ID_list = []
    for item in temp:
        if item not in passing_point_province_ID_list:
            passing_point_province_ID_list.append(item)

    passing_point_province_ID_string = ''
    for item in passing_point_province_ID_list:
        passing_point_province_ID_string = passing_point_province_ID_string + item + ' '
    passing_point_province_ID_string = str(start_point_province_ID) + ' ' + passing_point_province_ID_string
    passing_point_province_ID_string = passing_point_province_ID_string [:-1]

    return passing_point_province_ID_string

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
        for j in range(2, railways_points_len - 2): #(2,6) = 2 3 4 5
            start_point_province_ID = railways_list[i][j]
            end_point_province_ID = railways_list[i][j+1]

            new_railway = find_connect_railway_between_two_points_v2(start_point_province_ID, end_point_province_ID, definition_color_address, all_RGB_list, all_seed_info, pixels)


            #new_railway = find_connect_railway_between_two_points(start_point, end_point, connected_provinces)

            railways_list[i][j] = new_railway
            new_railway_string = ' '.join(str(v) for v in railways_list[i])
            #new_railway_string = ' '.join(railways_list[i])
            new_railway_string = new_railway_string.split(' ')
            railways_list[i][1] = len(new_railway_string) - 3


    new_railways_string = ''
    for item in railways_list:
        new_railways_string = new_railways_string + ' '.join(str(v) for v in item)

    save_file = filedialog.asksaveasfilename(title = "save railways.txt")
    with open(save_file, 'w') as filehandle:
        filehandle.write(new_railways_string)
    filehandle.close()
    print('Part 8 finished')

