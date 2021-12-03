from tkinter import filedialog
import tkinter as tk 

import json #finally find one


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

    

def read_dict(variable_str):
    ftypes = [('txt', '.txt'),('All files', '*')]
    path = filedialog.askopenfilename(title = ("load Variable " + str(variable_str)), filetypes = ftypes)
    print('Be patient, reading: ' + str(variable_str))
    with open(path) as f:
        some_variable = json.load(f)
    return some_variable

    
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


def save_dict(some_variable, variable_str):
    ftypes = [('txt', '.txt'),('All files', '*')]
    path = filedialog.asksaveasfilename(title = ("save Variable " + str(variable_str)), filetypes = ftypes)
    print('Be patient, saving: ' + str(variable_str))
    with open(path, 'w') as f:
        json.dump(some_variable, f)