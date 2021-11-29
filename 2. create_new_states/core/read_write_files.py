import tkinter as Tkinter
from tkinter import filedialog
import os
import shutil
import re


def copy_original_files_to_export_folder():
    
    _export_folder_location = os.getcwd() + "/export"
    if not os.path.exists(_export_folder_location):
        os.makedirs(_export_folder_location)
    _states_definition_file_location = filedialog.askopenfilename(title = "Select Vanilla Game's State Definition file (definition.csv)", filetypes={("HOI Map file", ".csv"),("All files", "*.*")})

    #read all supplyarea files
    #1.11.* update no more supplyareas
    if not os.path.exists(_export_folder_location + "/map/supplyareas"):
        os.makedirs(_export_folder_location + "/map/supplyareas")
    _supplyareas_folder_location = filedialog.askdirectory(title = "Select Vanilla Game's Supply Folder")
    src_files = os.listdir(_supplyareas_folder_location)
    for file_name in src_files:
        full_file_name = os.path.join(_supplyareas_folder_location, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, _export_folder_location + "/map/supplyareas")
    
    #read all state files
    if not os.path.exists(_export_folder_location + "/history/states"):
        os.makedirs(_export_folder_location + "/history/states")
    _states_folder_location = filedialog.askdirectory(title = "Select Vanilla Game's State Folder")
    src_files = os.listdir(_states_folder_location)
    for file_name in src_files:
        full_file_name = os.path.join(_states_folder_location, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, _export_folder_location + "/history/states")

    return _export_folder_location, _states_definition_file_location


def str_initialize(_all_text_in_lst):
    # remove comment
    for i in range(len(_all_text_in_lst)):
        if "#" in _all_text_in_lst[i]:
            _all_text_in_lst[i] = _all_text_in_lst[i].split("#",1)[0]
            _all_text_in_lst[i] = _all_text_in_lst[i] + "\n"
    all_text_in_str_initialized = "".join(_all_text_in_lst)
    return all_text_in_str_initialized    


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





def get_bracket_part_index(all_text_in_str_initialized, find_text, start_mark, end_mark):
    find_text_position = [m.start() for m in re.finditer(find_text,all_text_in_str_initialized)]
    #start_mark_position = [m.start() for m in re.finditer(start_mark,all_text_in_str_initialized)]
    #end_mark_position = [m.start() for m in re.finditer(end_mark,all_text_in_str_initialized)]
    i = find_text_position[0]
    stack = 0
    result = []
    result = ["",""]
    while i < (len(all_text_in_str_initialized)):
        if all_text_in_str_initialized[i]==start_mark:
            stack+=1
            if stack==1 and result[0] == "": 
                result[0] = i+1
        if all_text_in_str_initialized[i]==end_mark:
            stack-=1
            if stack==0 and result[1] == "": 
                result[1] = i
        i+=1
    find_text_info = result
    return find_text_info



def write_info(fileID, line_begin, original_info, index1, index2, line_end):
    if original_info != []:
        if index2 == "":
            fileID.write((line_begin + "%s" + line_end) %(original_info[index1]))
        else:
            if original_info[index1][index2] !="":
                fileID.write((line_begin + "%s" + line_end) %(original_info[index1][index2]))





def get_original_provinces_definition(modify_provinces_ID,states_definition_file_location):
    definition_file = open(states_definition_file_location)
    definition_file_lst_content = definition_file.readlines()
    definition_file.close()
    newlist = []
    for i in modify_provinces_ID:
        r = re.compile(i + ";" + ".*")
        newlist.append(list(filter(r.match, definition_file_lst_content)))
    new_item = []
    for i in newlist:
        item = i[0].split(";")
        new_item.append([item[0], item[4], item[5], item[6], item[7]])
    return new_item


def create_new_state_name(original_state_name, modify_provinces_ID):
    modify_state_name = []
    for i in range(len(modify_provinces_ID)):
        temp = "STATE_" + str(modify_provinces_ID[i])
        modify_state_name.append([str(modify_provinces_ID[i]), temp])

    modify_state_name[0] = [modify_provinces_ID[0] ,original_state_name[0]]
    return modify_state_name


def change_state_id(base_state_remain_province_ID, original_provinces_ID):
    temp2 = []
    temp2 = original_provinces_ID.split()
    temp2.remove(base_state_remain_province_ID)
    temp2.insert(0, base_state_remain_province_ID)
    return temp2


def write_new_state_reminder_file(_export_folder, _base_state_file_ID, _new_states_file_ID_name):
    f = open(_export_folder + "/" + "new_state_reminder.txt", "a+")
    f.write(_base_state_file_ID + " : " + _new_states_file_ID_name + "\n")
    f.close()






def write_state_file(file_id, index, state_id, 
    m_manpower, m_state_category, m_max_level, 
    m_resources, m_provinces,
    m_owner, m_add_tag, m_VP, m_infrastructure, 
    original_impassable, original_set_demilitarized_zone, m_local_supplies,
    o_airbase, o_antiair, o_radar, 
    o_arms_factory, o_industrial, o_dockyard, o_synthetic, 
    o_fuelsilo, o_rocket, o_nuclear, 
    o_navalbase, o_bunker, o_coastalbunker,
    m_provinces_buildings):

    file_id.write("state= {\n")
    file_id.write("\tid=%s\n" %state_id)
    file_id.write("\tname=\x22STATE_%s\x22\n" %state_id)
    file_id.write("\tmanpower = %d\r\t\n" %m_manpower[index][1])
    file_id.write("\tstate_category = %s\n\t\n" %m_state_category[index][1])
    write_info(file_id, "\timpassable = ", original_impassable, 0, "", "\n")
    write_info(file_id, "\tbuildings_max_level_factor = ", m_max_level, 0, "", "\n")
    write_info(file_id, "\tlocal_supplies = ", m_local_supplies, index, 1, "\n")
    file_id.write("\tprovinces = { %s }\n\t\n" %m_provinces)

    if index == 0:
        if m_resources != []:
            file_id.write(("\n\t\n\tresources= { "+"%s"+"\t}\n\t\n") %(m_resources[index]))

    ##history
    file_id.write("\thistory = {\n")
    file_id.write("\t\towner = %s\n\t\n" %m_owner)
    #add core
    for i in range(len(m_add_tag)):
        write_info(file_id, "\t\tadd_core_of = ", m_add_tag, i, "", "\n")
    file_id.write("\t\n")
    
    #dont forget...
    write_info(file_id, "\t\tset_demilitarized_zone = ", original_set_demilitarized_zone, 0, "", "\n")


    #VPs
    write_info(file_id, "\t\tvictory_points = {", m_VP, index, 1,"}\n\t\t\n")
    ##buildings
    file_id.write("\t\tbuildings = {\n")
    write_info(file_id, "\t\t\tinfrastructure = ", m_infrastructure, index, 1, "\n")
    
    if index == 0:
        write_info(file_id, "\t\t\tair_base = ", o_airbase, 0, "", "\n")
        write_info(file_id, "\t\t\tanti_air_building = ", o_antiair, 0, "", "\n")
        write_info(file_id, "\t\t\tarms_factory = ", o_arms_factory, 0, "", "\n")
        write_info(file_id, "\t\t\tindustrial_complex = ", o_industrial, 0, "", "\n")
        write_info(file_id, "\t\t\tdockyard = ", o_dockyard, index, "", "\n")
        write_info(file_id, "\t\t\tsynthetic_refinery = ", o_synthetic, 0, "", "\n")
        write_info(file_id, "\t\t\tfuel_silo = ", o_fuelsilo, 0, "", "\n")
        write_info(file_id, "\t\t\trocket_site = ", o_rocket, 0, "", "\n")
        write_info(file_id, "\t\t\tnuclear_reactor = ", o_nuclear, 0, "", "\n")
        write_info(file_id, "\t\t\tnaval_base = ", o_navalbase, 0, "", "\n")
        write_info(file_id, "\t\t\tbunker = ", o_bunker, 0, "", "\n")
        write_info(file_id, "\t\t\tcoastal_bunker = ", o_coastalbunker, 0, "", "\n")
    file_id.write("\t\t\n")
    
    write_info(file_id, ("\t\t"+ m_provinces_buildings[index][0] + " = {"), 
                    m_provinces_buildings ,index ,1 ,"}\n")

    file_id.write("\t\t}\n")
    file_id.write("\t}\n")
    file_id.write("}")
