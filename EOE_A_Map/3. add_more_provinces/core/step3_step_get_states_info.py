import re
import os
from tkinter import filedialog
from core import read_files

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
    for i in range(len(find_text_position)):
        for j in reversed(open_bracket_position):
            if j > find_text_position[i]:
                temp1 = j
                for k in reversed(close_bracket_position):
                    if k > temp1:
                        temp2 = k
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
    original_local_supplies = find_inhalt_in_bracket_fcn(all_text_in_str_initialized, "local_supplies", "=", "\n")
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
        'local_supplies': original_local_supplies,
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
    states_info_dict['local_supplies'].append(state_info_dict['local_supplies'])
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
        'local_supplies': [],
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
    all_text_str = read_files.open_file_return_str(title, filetypes)
    all_text_list = read_files.split_str_into_list(all_text_str, ';')
    definition_color_address = read_files.split_info_definition_csv(all_text_list)
    return definition_color_address

def step_get_states_info():
    states_info_dict = read_states_info()
    read_files.save_dict(states_info_dict, 'states_info_dict')
    definition_info_dict = read_definition_info()
    read_files.save_dict(definition_info_dict, 'definition_info_dict')

    print('PART 2.5 finished')
