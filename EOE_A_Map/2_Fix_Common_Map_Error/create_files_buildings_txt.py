from tkinter import filedialog
import tkinter as tk 
from PIL import Image

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

def create_buildings_files():
    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (province.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_x = im.size[0]
    image_y = im.size[1]


    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = open_file_return_str(title, filetypes)
    all_text_list = split_str_into_list(all_text_str, ';')
    definition_color_address = split_info_definition_csv(all_text_list)
    used_RGB = definition_color_address['RGB']
    used_land_sea_lake = definition_color_address['land_sea_lake']
    used_terrain = definition_color_address['terrain']
    used_coast = definition_color_address['coast']

    building_export_list = []
    building_mark_list = []

    for y in range(0, image_y):
        print('calculating line ' + str(y) + ' / ' + str(image_y))
        for x in range(0, image_x):
            pixel_color = list(pixels[x,y])
            if pixel_color not in building_mark_list:
                building_mark_list.append(pixel_color)
                state_id = used_RGB.index(pixel_color)
                state_land_sea_lake = used_land_sea_lake[state_id]
                if state_land_sea_lake == 'land':
                    state_terrain = used_terrain[state_id]
                    if state_terrain != 'ocean':
                        building_export_list.append([str(state_id) + '.00;arms_factory;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;arms_factory;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;arms_factory;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;arms_factory;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;arms_factory;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;arms_factory;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;industrial_complex;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;industrial_complex;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;industrial_complex;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;industrial_complex;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;industrial_complex;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;industrial_complex;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;air_base;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])                        
                        building_export_list.append([str(state_id) + '.00;supply_node;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        #naval_base
                        building_export_list.append([str(state_id) + '.00;bunker;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        state_coast = used_coast[state_id]
                        if state_coast == 'true':
                            building_export_list.append([str(state_id) + '.00;coastal_bunker;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                            building_export_list.append([str(state_id) + '.00;dockyard;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;anti_air_building;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;anti_air_building;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;anti_air_building;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;synthetic_refinery;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;fuel_silo;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;radar_station;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;rocket_site;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        building_export_list.append([str(state_id) + '.00;nuclear_reactor;' + str(x) + ';0.00;' + str(y) + '.00;0.00;0'])
                        #floating_harbor

    a = 1

    MyFile = open('buildings_new.txt','w')
    for element in building_export_list:
        MyFile.write(element[0])
        MyFile.write('\n')
    MyFile.close()




def main():
    create_buildings_files()

if __name__ == "__main__":
    main()
