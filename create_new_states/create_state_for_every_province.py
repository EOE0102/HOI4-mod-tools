import tkinter as Tkinter
from tkinter import filedialog
import os
import shutil
import re

## parameter inistialation
#weight
manpower_weight = [["unknown",0.00000001],["ocean",0.00000001],["lakes",0.00000001],
                    ["forest",40],["hills",40],["mountain",20],
                    ["plains",60],["urban",100],["jungle",20],
                    ["marsh",10],["desert",1],
                    ["water_fjords",0.00000001],["water_shallow_sea",0.00000001],["water_deep_ocean",0.00000001],
                    ["ice_sheet",0.00000001]]
manpower_victory_points_weight = 0.20
manpower_provinces_buildings_weight = 1
manpower_coast_weight = 1.5

state_category_weight = [["unknown",-10],["ocean",-10],["lakes",-10],
                    ["forest",-2],["hills",-2],["mountain",-3],
                    ["plains",-1],["urban",0],["jungle",-3],
                    ["marsh",-4],["desert",-4],
                    ["water_fjords",-10],["water_shallow_sea",-10],["water_deep_ocean",-10],
                    ["ice_sheet",-10]]
state_category_type_lst  = ["rural","town","large_town","city","large_city","metropolis","megalopolis"]
state_category_type_nochange_lst = ["enclave","small_island","tiny_island","wasteland","pastoral"]
state_category_victory_points_weight = 10
state_category_provinces_buildings_weight = 1

state_infrastructure_weight = [["unknown",-10],["ocean",-10],["lakes",-10],
                    ["forest",-2],["hills",-2],["mountain",-3],
                    ["plains",-1],["urban",0],["jungle",-3],
                    ["marsh",-4],["desert",-4],
                    ["water_fjords",-10],["water_shallow_sea",-10],["water_deep_ocean",-10],
                    ["ice_sheet",-10]]
infrastructure_victory_points_weight = 10
infrastructure_provinces_buildings_weight = 1



def __folder_files_prepearation():
    root = Tkinter.Tk()
    _states_folder_location = filedialog.askdirectory(title = "Select State Folder Location")
    _supplyareas_folder_location = filedialog.askdirectory(title = "Select Supply Folder Location")
    _export_folder_location = filedialog.askdirectory(title = "Select Export Folder Location")
    _states_definition_file_location = filedialog.askopenfilename(title = "Select State Definition file(definition.csv)", filetypes={("HOI Map file", ".csv"),("All files", "*.*")})
    
    #prepare for export
    if not os.path.exists(_export_folder_location + "/states"):
        os.makedirs(_export_folder_location + "/states")
    if not os.path.exists(_export_folder_location + "/supplyareas"):
        os.makedirs(_export_folder_location + "/supplyareas")

    #create supply file for modify
    src_files = os.listdir(_states_folder_location)
    for file_name in src_files:
        full_file_name = os.path.join(_states_folder_location, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, _export_folder_location + "/states")

    src_files = os.listdir(_supplyareas_folder_location)
    for file_name in src_files:
        full_file_name = os.path.join(_supplyareas_folder_location, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, _export_folder_location + "/supplyareas")
    return _export_folder_location, _states_folder_location, _supplyareas_folder_location, _states_definition_file_location

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


def get_remain_province_ID(original_victory_points, original_provinces_ID):
    no_modify_provinces_ID = original_provinces_ID.split()
    no_modify_victory_points = []

    for i in no_modify_provinces_ID:
        no_modify_victory_points.append([i,""])

    for i in range(len(no_modify_provinces_ID)):
        for j in original_victory_points:
            temp = re.findall(r"\D+" + no_modify_provinces_ID[i] +r"\s+\d",j)
            temp2 = ""
            if temp != []:
                j = j.replace(temp[0][:-1], "")
                j = j.replace("#", "")
                temp2 = str(int(float(j)))
                no_modify_victory_points[i][1] = temp2
    
    max_vp = 0
    for i in no_modify_victory_points:
        if i[1] != "" :
            if int(i[1]) > int(max_vp):
                max_vp = i[1]
                max_vp_id = i[0]

    if max_vp == 0:
        base_state_remain_province_ID = no_modify_provinces_ID[0]
    else:
        base_state_remain_province_ID = max_vp_id
    
    return base_state_remain_province_ID


def create_new_states_string(fileStart, amount_of_file):
    i = 0
    new_states_file_ID_name = ""
    while i < amount_of_file:
        new_states_file_ID_name = new_states_file_ID_name + str(fileStart+i) + " "
        i+=1
    return new_states_file_ID_name
    

def add_new_state_name_to_supplyarea(export_folder, supplyareas_file_lst, base_state_file_ID, new_states_file_ID_name):

    for supplyareas_file_name in supplyareas_file_lst:
        supplyareas_file = open(export_folder + "/supplyareas/" + supplyareas_file_name)
        supplyareas_file_content = supplyareas_file.read()
        #supplyareas_file.close()
        
        temp = re.findall(r"\s" + base_state_file_ID + r"\s",supplyareas_file_content) 
        if len(temp) == 1: #find index
            index1 = get_bracket_part_index(supplyareas_file_content, "states", "{", "}")
            #enter_position = [m.start() for m in re.finditer("\n" ,suppluareas_file_content)]
            temp2 = index1[1]
            supplyareas_file_content = supplyareas_file_content[:temp2] + "\t" + new_states_file_ID_name + "\n\t" + supplyareas_file_content[temp2:]
            supplyareas_file.close() 
            supplyareas_file = open(export_folder + "/supplyareas/" + supplyareas_file_name, "w+")
            supplyareas_file.write(supplyareas_file_content)
            #supplyareas_file.close()
            return supplyareas_file_content
        supplyareas_file.close()


def write_new_state_reminder_file(_export_folder, _base_state_file_ID, _new_states_file_ID_name):
    f = open(_export_folder + "/" + "new_state_reminder.txt", "a+")
    f.write(_base_state_file_ID + " : " + _new_states_file_ID_name + "\n")
    f.close()


def change_state_id(base_state_remain_province_ID, original_provinces_ID):
    temp2 = []
    temp2 = original_provinces_ID.split()
    temp2.remove(base_state_remain_province_ID)
    temp2.insert(0, base_state_remain_province_ID)
    return temp2


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


def change_manpower(original_state_manpower, original_provinces_definition, manpower_weight, coast_weight, 
        modify_victory_points, manpower_victory_points_weight, modify_provinces_buildings, manpower_provinces_buildings_weight):
    modify_manpower = []
    modify_manpower_matrix = []
    base_weight = 0
    total_manpower = float(original_state_manpower[0])


    for i in original_provinces_definition:
        for j in manpower_weight:
            if i[3] in j:
                modify_manpower_matrix.append([i[0], j[1]])

    #add manpower according to coast
    for i in range(len(original_provinces_definition)):
        if original_provinces_definition[i][2] == "true":
            modify_manpower_matrix[i][1] = modify_manpower_matrix[i][1] * coast_weight

    #add manpower according to VP
    for i in range(len(modify_victory_points)):
        if modify_victory_points[i][1] != "":
            temp = modify_victory_points[i][1].split()
            temp = float(temp[1])

            if temp > 10:
                temp = 10

            modify_manpower_matrix[i][1] = modify_manpower_matrix[i][1] * (1 + temp*manpower_victory_points_weight)

    #add manpower according to buildings
    for i in range(len(modify_provinces_buildings)):
        if modify_provinces_buildings[i][1] != "":
            modify_manpower_matrix[i][1] = modify_manpower_matrix[i][1] * (1 + 1*manpower_provinces_buildings_weight)

    #cal. base weight
    for i in modify_manpower_matrix:
        base_weight = base_weight + i[1]
    
    #cal.
    for i in range(len(modify_manpower_matrix)):
        temp = int(total_manpower * modify_manpower_matrix[i][1] / base_weight)
        if temp <= 0:
            temp = 1
        modify_manpower.append([modify_manpower_matrix[i][0], temp])
    
    return modify_manpower


def change_state_category(original_state_category, original_provinces_definition, state_category_weight, state_category_type_lst, state_category_type_nochange_lst, 
        modify_victory_points, state_category_victory_points_weight, modify_provinces_buildings, state_category_provinces_buildings_weight):
    modify_state_category = []
    modify_state_category_matrix = []
    base_weight = -10
    for i in original_provinces_definition:
        for j in state_category_weight:
            if i[3] in j:
                base_weight = max(base_weight, j[1])

    for i in range(len(original_provinces_definition)):
        for j in state_category_weight:
            if original_provinces_definition[i][3] in j:
                temp = j[1] - base_weight
                modify_state_category_matrix.append([original_provinces_definition[i][0], temp])

    #VP
    for i in range(len(modify_victory_points)):
        if modify_victory_points[i][1] != "":
            temp = modify_victory_points[i][1].split()
            temp = float(temp[1])
            temp2 = int(temp/state_category_victory_points_weight) + 1
            modify_state_category_matrix[i][1] = modify_state_category_matrix[i][1] + temp2

    #building
    for i in range(len(modify_provinces_buildings)):
        if modify_provinces_buildings[i][1] != "":
            modify_state_category_matrix[i][1] = modify_state_category_matrix[i][1] + 1

    #
    for i in range(len(modify_state_category_matrix)):
        if modify_state_category_matrix[i][1] > 0:
                modify_state_category_matrix[i][1] = 0

    #
    if original_state_category[0] in state_category_type_nochange_lst:
        for i in range(len(modify_state_category_matrix)):
            modify_state_category.append([modify_state_category_matrix[i][0] ,original_state_category[0]])
    else:
        p = state_category_type_lst.index(original_state_category[0])
        for i in range(len(modify_state_category_matrix)):
            if modify_state_category_matrix[i][1] < (0-p):
                modify_state_category_matrix[i][1] = 0-p
            modify_state_category.append([modify_state_category_matrix[i][0], state_category_type_lst[p + modify_state_category_matrix[i][1]]] ) 

    return modify_state_category


def change_infrastructure_level(original_infrastructure, original_provinces_definition, state_infrastructure_weight, 
        modify_victory_points, infrastructure_victory_points_weight, modify_provinces_buildings, infrastructure_provinces_buildings_weight):
    _modify_infrastructure_level = []
    modify_infrastructure_level_matrix = []
    base_weight = -10
    for i in original_provinces_definition:
        for j in state_infrastructure_weight:
            if i[3] in j:
                base_weight = max(base_weight, j[1])

    for i in range(len(original_provinces_definition)):
        for j in state_category_weight:
            if original_provinces_definition[i][3] in j:
                temp = j[1] - base_weight
                modify_infrastructure_level_matrix.append([original_provinces_definition[i][0], temp])

    #VP
    for i in range(len(modify_victory_points)):
        if modify_victory_points[i][1] != "":
            temp = modify_victory_points[i][1].split()
            temp = float(temp[1])
            temp2 = int(temp/state_category_victory_points_weight) + 1
            modify_infrastructure_level_matrix[i][1] = modify_infrastructure_level_matrix[i][1] + temp2

    #buildings
    for i in range(len(modify_provinces_buildings)):
        if modify_provinces_buildings[i][1] != "":
            modify_infrastructure_level_matrix[i][1] = modify_infrastructure_level_matrix[i][1] + 1

    for i in range(len(modify_infrastructure_level_matrix)):
        if modify_infrastructure_level_matrix[i][1] > 0:
                modify_infrastructure_level_matrix[i][1] = 0

    #
    for i in range(len(modify_infrastructure_level_matrix)):
        temp4 = modify_infrastructure_level_matrix[i][1] + int(original_infrastructure[0])
        if temp4 < 1:
            temp4  = 1
            if int(original_infrastructure[0]) == 0:
                temp4  = 0
        _modify_infrastructure_level.append([modify_infrastructure_level_matrix[i][0], temp4])
        
    return _modify_infrastructure_level


def create_victory_points(modify_provinces_ID, original_victory_points):
    modify_victory_points = []
    
    for i in modify_provinces_ID:
        modify_victory_points.append([i,""])

    for i in range(len(modify_provinces_ID)):
        for j in original_victory_points:
            temp = re.findall(r"\D+" + modify_provinces_ID[i] +r"\s+\d",j)
            temp2 = ""
            if temp != []:
                j = j.replace(temp[0][:-1], "")
                j = j.replace("#", "")
                temp2 = str(int(float(j)))
                modify_victory_points[i][1] = str(modify_provinces_ID[i])+ " "+ temp2

    return modify_victory_points


def create_original_provinces_buildings(modify_provinces_ID, original_province_buildings):
    modify_provinces_buildings = []
    for i in range(len(modify_provinces_ID)):
        modify_provinces_buildings.append([modify_provinces_ID[i] ,""])

    for i in range(len(modify_provinces_ID)):
        for j in original_province_buildings:
            if modify_provinces_ID[i] == j[0]:
                modify_provinces_buildings[i][1] = j[1]
    
    return modify_provinces_buildings


def write_info(fileID, line_begin, original_info, index1, index2, line_end):
    if original_info != []:
        if index2 == "":
            fileID.write((line_begin + "%s" + line_end) %(original_info[index1]))
        else:
            if original_info[index1][index2] !="":
                fileID.write((line_begin + "%s" + line_end) %(original_info[index1][index2]))


def write_state_file(file_id, index, state_id, 
    m_manpower, m_state_category, m_max_level, 
    m_resources, m_provinces,
    m_owner, m_add_tag, m_VP, m_infrastructure, 
    original_impassable, original_set_demilitarized_zone,
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
    if index == 0:
        if m_resources != []:
            file_id.write(("\n\t\n\tresources= { "+"%s"+"\t}\n\t\n") %(m_resources[index]))

    file_id.write("\tprovinces = { %s }\n\t\n" %m_provinces)
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










def main():
    export_folder_location, states_folder_location, supplyareas_folder_location, states_definition_file_location= __folder_files_prepearation()

    #get original file name
    states_file_lst = []
    for file in os.listdir(states_folder_location):
        if file.endswith(".txt"):
            states_file_lst.append(file)

    #modify for every state in folder
    for base_state_file_name in states_file_lst:
        #read original file
        temp = states_folder_location + "/" + base_state_file_name
        file_state_original = open(temp)
        all_text_in_lst = file_state_original.readlines()
        file_state_original.close()
        
        #remove comment
        all_text_in_str_initialized = str_initialize(all_text_in_lst)

        #state basic info 1
        text_in_level_1 = getbrace_only(all_text_in_str_initialized,1)
        text_in_level_1_nospace = text_in_level_1.replace(" ","")
        #original_state_id = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "id", "=", "\n")
        original_state_name = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "name", "=", "\n")
        original_state_manpower = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "manpower", "=", "\n")
        original_state_category = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "state_category", "=", "\n")
        original_state_category[0] = original_state_category[0].replace("\"", "")
        original_buildings_max_level_factor = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "buildings_max_level_factor", "=", "\n")
        original_impassable = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "impassable", "=", "\n")
        
        # resources & provinces ID & VPs
        original_resources = find_inhalt_in_bracket_fcn(all_text_in_str_initialized, "resources", "{", "}")
        original_provinces_ID = find_inhalt_in_bracket_fcn(all_text_in_str_initialized, "provinces", "{", "}")
        original_provinces_ID = original_provinces_ID[0].replace("\n","")
        original_provinces_ID = original_provinces_ID.replace("\t","")  
        original_victory_points = find_inhalt_in_bracket_fcn(all_text_in_str_initialized, "victory_points", "{", "}")

        #state basic info 2
        text_in_level_2 = getbrace_only(all_text_in_str_initialized,2)
        text_in_level_2_nospace = text_in_level_2.replace(" ","")
        original_state_owner = find_inhalt_in_bracket_fcn(text_in_level_2_nospace, "owner", "=", "\n")
        original_add_core_of_country_tag = find_inhalt_in_bracket_fcn(text_in_level_2_nospace, "add_core_of", "=", "\n")
        #dont forget
        original_set_demilitarized_zone = find_inhalt_in_bracket_fcn(text_in_level_2_nospace, "set_demilitarized_zone", "=", "\n")



        # state basic info 2 original building
        text_in_level_3 = getbrace_only(all_text_in_str_initialized,3)
        text_in_level_3_nospace = text_in_level_3.replace(" ","")
        original_infrastructure = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "infrastructure", "=", "\n")
        original_air_base = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "air_base", "=", "\n")  
        original_anti_air_building = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "anti_air_building", "=", "\n")  
        original_radar_station = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "radar_station", "=", "\n")  

        original_arms_factory = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "arms_factory", "=", "\n")
        original_industrial_complex = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "industrial_complex", "=", "\n")
        original_dockyard = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "dockyard", "=", "\n") 
        original_synthetic_refinery = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "synthetic_refinery", "=", "\n") 
        original_fuel_silo = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "fuel_silo", "=", "\n")  
        original_rocket_site = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "rocket_site", "=", "\n")  
        original_nuclear_reactor = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "nuclear_reactor", "=", "\n")  

        original_naval_base = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "naval_base", "=", "\n")   
        original_bunker = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "\tbunker", "=", "\n")    #TODO OPPS coastal_bunker will be seleted too
        original_coastal_bunker = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "coastal_bunker", "=", "\n")  

        #history part
        history_part_index = get_bracket_part_index(all_text_in_str_initialized, "history", "{", "}")
        #text_in_str_nohistorypart = all_text_in_str_initialized[:history_part_index[0]] + all_text_in_str_initialized[history_part_index[1]:]
        text_in_str_historypart = all_text_in_str_initialized[history_part_index[0]:history_part_index[1]]

        #building part
        #text_of_building_part = find_inhalt_in_bracket_fcn(text_in_str_historypart, "buildings", "{", "}")
        buildings_part_index = get_bracket_part_index(text_in_str_historypart, "buildings", "{", "}")
        text_in_str_historypart_nobuildingpart = text_in_str_historypart[:buildings_part_index[0]] + text_in_str_historypart[buildings_part_index[1]:] 
        text_in_str_historypart_buildingpart = text_in_str_historypart[buildings_part_index[0]:buildings_part_index[1]]

        # script info
        original_script_start_date = re.findall(r"\d\d\d\d\.\d+\.\d+",text_in_str_historypart_nobuildingpart)
        original_script = []
        for i in original_script_start_date:
            index = get_bracket_part_index(text_in_str_historypart_nobuildingpart, i, "{", "}")
            original_script.append(text_in_str_historypart_nobuildingpart[index[0]:index[1]])

        #provinces detial info

        temp = text_in_str_historypart_buildingpart.replace(" ","")
        original_province_buildings_id = re.findall(r"\d+\=\{",temp)
        original_province_buildings_id = [m.replace("={","") for m in original_province_buildings_id]
        original_province_buildings = []
        for i in original_province_buildings_id:
            index = get_bracket_part_index(text_in_str_historypart_buildingpart, i, "{", "}")
            temp = text_in_str_historypart_buildingpart[index[0]:index[1]]
            original_province_buildings.append([i ,temp])



        base_state_remain_province_ID = get_remain_province_ID(original_victory_points, original_provinces_ID)
        #MODIFY
        #state basic info 1
        base_state_file_ID = base_state_file_name.split("-")[0]
        modify_provinces_ID = change_state_id(base_state_remain_province_ID, original_provinces_ID) #state id state name
        original_provinces_definition = get_original_provinces_definition(modify_provinces_ID,states_definition_file_location)
        modify_state_name = create_new_state_name(original_state_name, modify_provinces_ID)
        
        # resources & provinces ID & VPs
        modify_victory_points = create_victory_points(modify_provinces_ID, original_victory_points)
        modify_provinces_buildings = create_original_provinces_buildings(modify_provinces_ID, original_province_buildings)

        modify_manpower = change_manpower(original_state_manpower, original_provinces_definition, manpower_weight, manpower_coast_weight,
            modify_victory_points, manpower_victory_points_weight, modify_provinces_buildings, manpower_provinces_buildings_weight)
        modify_state_category = change_state_category(original_state_category, original_provinces_definition, state_category_weight, state_category_type_lst, state_category_type_nochange_lst, 
            modify_victory_points, state_category_victory_points_weight, modify_provinces_buildings, state_category_provinces_buildings_weight)
        modify_infrastructure_level = change_infrastructure_level(original_infrastructure, original_provinces_definition, state_infrastructure_weight, 
            modify_victory_points, infrastructure_victory_points_weight, modify_provinces_buildings, infrastructure_provinces_buildings_weight)
        #state basic info 2
        modify_state_owner = original_state_owner[0]
        modify_add_core_of_country_tag = original_add_core_of_country_tag

        # state basic info 2 original building
    
        



        ## add new states to supplyareas
        #numberOfFiles = len([name for name in os.listdir(export_folder_location + "/supplyareas") if os.path.isfile(name)]) #get number of files in /states
        number_of_state_file = len(os.listdir(export_folder_location + "/states"))
        state_file_start = number_of_state_file + 1 #fileStart, txt file ID
        amount_of_new_state_file = len(modify_provinces_ID)
        new_states_file_ID_name = create_new_states_string(state_file_start, amount_of_new_state_file - 1)
        

        supplyareas_file_lst = os.listdir(export_folder_location + "/supplyareas")
        add_new_state_name_to_supplyarea(export_folder_location, supplyareas_file_lst, base_state_file_ID, new_states_file_ID_name)
        
        write_new_state_reminder_file(export_folder_location, base_state_file_ID, new_states_file_ID_name)
        

        ##modify base state file

        all_states_id_lst = new_states_file_ID_name.split()
        all_states_id_lst.insert(0, base_state_file_ID)

        for index in range(len(all_states_id_lst)):
            if index == 0:
                new_states_file_name = base_state_file_name.replace(".txt","")
            else:
                new_states_file_name = ("%s-STATE_%s" %(all_states_id_lst[index],all_states_id_lst[index]))
            new_states_full_file_name = export_folder_location + "/states/" + new_states_file_name + ".txt"
            new_states_file = open(new_states_full_file_name, "w")

            write_state_file(new_states_file, index, all_states_id_lst[index], 
                modify_manpower, modify_state_category, original_buildings_max_level_factor, 
                original_resources, modify_provinces_ID[index],
                modify_state_owner, modify_add_core_of_country_tag, modify_victory_points, modify_infrastructure_level, 
                original_impassable, original_set_demilitarized_zone,
                original_air_base, original_anti_air_building, original_radar_station, 
                original_arms_factory, original_industrial_complex, original_dockyard, original_synthetic_refinery, 
                original_fuel_silo, original_rocket_site, original_nuclear_reactor, 
                original_naval_base, original_bunker, original_coastal_bunker,
                modify_provinces_buildings)
            new_states_file.close()


if __name__ == '__main__':
    main()
