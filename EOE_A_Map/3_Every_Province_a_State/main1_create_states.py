import os
import re
#private function
from _paramenter import *
from core import *

def get_remain_province_ID(original_victory_points, original_provinces_ID):
    #the first province will ramain as the original state's province
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


def change_state_id(base_state_remain_province_ID, original_provinces_ID):
    temp2 = []
    temp2 = original_provinces_ID.split()
    temp2.remove(base_state_remain_province_ID)
    temp2.insert(0, base_state_remain_province_ID)
    return temp2


def create_new_states_string(fileStart, amount_of_file):
    i = 0
    new_states_file_ID_name = ""
    while i < amount_of_file:
        new_states_file_ID_name = new_states_file_ID_name + str(fileStart+i) + " "
        i+=1
    return new_states_file_ID_name


def get_a_clear_VP(original_victory_points):

    for item in original_victory_points:
        a = 1

    return original_victory_points

def main():
    export_folder_location, states_definition_file_location= copy_original_files_to_export_folder()

    export_states_folder_location = export_folder_location + "/history/states/"
    export_supplyareas_folder_location = export_folder_location + "/map/supplyareas/"

    #get original file name
    states_file_lst = []
    for file in os.listdir(export_states_folder_location):
        if file.endswith(".txt"):
            states_file_lst.append(file)

    #modify for every state in folder
    for base_state_file_name in states_file_lst:
        #read original file
        temp = export_states_folder_location  + base_state_file_name
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
        original_buildings_max_level_factor = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "buildings_max_level_factor", "=", "\n")
        original_state_category = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "state_category", "=", "\n")
        original_state_category[0] = original_state_category[0].replace("\"", "")
        original_impassable = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "impassable", "=", "\n")
        original_local_supplies = find_inhalt_in_bracket_fcn(text_in_level_1_nospace, "local_supplies", "=", "\n")
        
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
        original_bunker = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "\tbunker", "=", "\n")
        original_coastal_bunker = find_inhalt_in_bracket_fcn(text_in_level_3_nospace, "coastal_bunker", "=", "\n")  

        ##history part
        original_set_demilitarized_zone = find_inhalt_in_bracket_fcn(text_in_level_2_nospace, "set_demilitarized_zone", "=", "\n")
        history_part_index = get_bracket_part_index(all_text_in_str_initialized, "history", "{", "}")
        #text_in_str_nohistorypart = all_text_in_str_initialized[:history_part_index[0]] + all_text_in_str_initialized[history_part_index[1]:]
        text_in_str_historypart = all_text_in_str_initialized[history_part_index[0]:history_part_index[1]]


        ##building part
        #text_of_building_part = find_inhalt_in_bracket_fcn(text_in_str_historypart, "buildings", "{", "}")
        buildings_part_index = get_bracket_part_index(text_in_str_historypart, "buildings", "{", "}")
        text_in_str_historypart_nobuildingpart = text_in_str_historypart[:buildings_part_index[0]] + text_in_str_historypart[buildings_part_index[1]:] 
        text_in_str_historypart_buildingpart = text_in_str_historypart[buildings_part_index[0]:buildings_part_index[1]]

        # script info TODO: script??? for different script?
        original_script_start_date = re.findall(r"\d\d\d\d\.\d+\.\d+",text_in_str_historypart_nobuildingpart)
        original_script = []
        for i in original_script_start_date:
            index = get_bracket_part_index(text_in_str_historypart_nobuildingpart, i, "{", "}")
            original_script.append(text_in_str_historypart_nobuildingpart[index[0]:index[1]])

        #provinces detail info
        temp = text_in_str_historypart_buildingpart.replace(" ","")
        original_province_buildings_id = re.findall(r"\d+\=\{",temp)
        original_province_buildings_id = [m.replace("={","") for m in original_province_buildings_id]
        original_province_buildings = []
        for i in original_province_buildings_id:
            index = get_bracket_part_index(text_in_str_historypart_buildingpart, i, "{", "}")
            temp = text_in_str_historypart_buildingpart[index[0]:index[1]]
            original_province_buildings.append([i ,temp])


        original_victory_points = get_a_clear_VP(original_victory_points)
        base_state_remain_province_ID = get_remain_province_ID(original_victory_points, original_provinces_ID)
        #MODIFY
        #state basic info 1
        base_state_file_ID = base_state_file_name.split("-")[0]
        modify_provinces_ID = change_state_id(base_state_remain_province_ID, original_provinces_ID) #state id state name
        modify_provinces_ID_without_lake = remove_lake_from_provinces_ID(modify_provinces_ID, states_definition_file_location)
        #original_provinces_definition = get_original_provinces_definition(modify_provinces_ID,states_definition_file_location)
        #lake state
        original_provinces_definition = get_original_provinces_definition_without_lake(modify_provinces_ID,states_definition_file_location)

        #TODO
        modify_state_name = create_new_state_name(original_state_name, modify_provinces_ID)

        # resources & provinces ID & VPs
        modify_victory_points = create_victory_points(modify_provinces_ID, original_victory_points)
        modify_provinces_buildings = create_original_provinces_buildings(modify_provinces_ID, original_province_buildings)


        #debug
        if original_provinces_definition[0][0]  == '3379 3217':
            a = 1



        modify_manpower = change_manpower(original_state_manpower, original_provinces_definition, manpower_weight, manpower_coast_weight,
            modify_victory_points, manpower_victory_points_weight, max_victory_point_weight,modify_provinces_buildings, manpower_provinces_buildings_weight)
        modify_state_category = change_state_category(original_state_category, original_provinces_definition, state_category_weight, state_category_type_lst, state_category_type_nochange_lst, 
            modify_victory_points, state_category_victory_points_weight, max_victory_point_weight, modify_provinces_buildings, state_category_provinces_buildings_weight)
        modify_infrastructure_level = change_infrastructure_level(original_infrastructure, original_provinces_definition, state_infrastructure_weight, 
            modify_victory_points, infrastructure_victory_points_weight, max_victory_point_weight, modify_provinces_buildings, infrastructure_provinces_buildings_weight)
        modify_local_supplies = change_local_supplies(original_local_supplies, original_provinces_definition, state_local_supplies_weight, 
            modify_victory_points, local_supplies_victory_points_weight, modify_provinces_buildings, local_supplies_buildings_weight)

        #state basic info 2
        modify_state_owner = original_state_owner[0]
        modify_add_core_of_country_tag = original_add_core_of_country_tag

        # state basic info 2 original building
    
        



        ## add new states to supplyareas
        numberOfFiles = len([name for name in os.listdir(export_supplyareas_folder_location) if os.path.isfile(name)]) #get number of files in /states
        number_of_state_file = len(os.listdir(export_states_folder_location))
        state_file_start = number_of_state_file + 1 #fileStart, txt file ID
        amount_of_new_state_file = len(modify_provinces_ID_without_lake)
        new_states_file_ID_name = create_new_states_string(state_file_start, amount_of_new_state_file - 1)
        

        #supplyareas_file_lst = os.listdir(export_folder_location + "/supplyareas")
        #add_new_state_name_to_supplyarea(export_folder_location, supplyareas_file_lst, base_state_file_ID, new_states_file_ID_name)
        write_new_state_reminder_file(export_folder_location, base_state_file_ID, new_states_file_ID_name)
        

        ##modify base state file

        all_states_id_lst = new_states_file_ID_name.split()
        all_states_id_lst.insert(0, base_state_file_ID)

        for index in range(len(all_states_id_lst)):
            if index == 0:
                new_states_file_name = base_state_file_name.replace(".txt","")
            else:
                new_states_file_name = ("%s-STATE_%s" %(all_states_id_lst[index],all_states_id_lst[index]))
            new_states_full_file_name = export_states_folder_location + new_states_file_name + ".txt"
            new_states_file = open(new_states_full_file_name, "w")

            write_state_file(new_states_file, index, all_states_id_lst[index], 
                modify_manpower, modify_state_category, original_buildings_max_level_factor, 
                original_resources, modify_provinces_ID_without_lake[index],
                modify_state_owner, modify_add_core_of_country_tag, modify_victory_points, modify_infrastructure_level, 
                original_impassable, original_set_demilitarized_zone, modify_local_supplies,
                original_air_base, original_anti_air_building, original_radar_station, 
                original_arms_factory, original_industrial_complex, original_dockyard, original_synthetic_refinery, 
                original_fuel_silo, original_rocket_site, original_nuclear_reactor, 
                original_naval_base, original_bunker, original_coastal_bunker,
                modify_provinces_buildings)
            new_states_file.close()


if __name__ == '__main__':
    main()
