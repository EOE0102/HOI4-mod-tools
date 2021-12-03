from tkinter import filedialog
import os


def main():
    _export_folder_location = os.getcwd() + "/export/"
    if not os.path.exists(_export_folder_location):
        os.makedirs(_export_folder_location)
    
    prospect_for_resources_definition_file_location = filedialog.askopenfilename(title = "Select prospect_for_resources's State Definition file (definition.csv)", filetypes={("HOI Map file", ".csv"),("All files", "*.*")})
    definition_file = open(prospect_for_resources_definition_file_location)
    definition_file_lst_content = definition_file.readlines()
    definition_file.close()
    prospect_for_resources_lst = []
    for i in definition_file_lst_content:
        item = i.split(",")
        prospect_for_resources_lst.append(item)

    new_resource_decisions_file = _export_folder_location + 'EOE_B_Resource_decisions.txt'
    file_id = open(new_resource_decisions_file, "w")
    file_id.write("EOE_B_Resource_decisions = {\n")

    new_resource_decisions_l_file = _export_folder_location + 'EOE_B_Resource_decisions_l_english.yml'
    file_id2 = open(new_resource_decisions_l_file, "w")
    file_id2.write("l_english:\n")

    for i in prospect_for_resources_lst:
        vanilla_state_id = i[0]
        object_province_id = i[1]
        state_name = i[2]
        own_country_tag = i[3]
        resource_type = i[4]
        resource_amount = i[5]
        prospect_serier = i[6]
        excavation_tech = i[7]
        another_tech_name = i[8]
        num_of_civilian_factories_available_for_projects = i[11]
        available_date = i[12]
        fire_only_once = i[13]
        cost_PP = i[14]
        days_remove = i[15]
        civilian_factory_use = i[16]
        ai_will_do = i[17]
        decision_name = i[18]
        has_state_flag = i[19]
        a = 1

        file_id.write('\t' + decision_name + " = { #" + vanilla_state_id + '\n')
        file_id.write('\t\ticon = ' + resource_type + '\n')
        file_id.write('\t\tallowed = { }\n')
        file_id.write('\t\thighlight_states = {\n')
        file_id.write('\t\t\thighlight_state_targets = {\n')
        file_id.write('\t\t\t\tstate = ' + vanilla_state_id + '\n')
        file_id.write('\t\t\t}\n')
        file_id.write('\t\t}\n')
        file_id.write('\t\tavailable = {\n')
        file_id.write('\t\t\thas_tech = excavation'+ excavation_tech + '\n')
        file_id.write('\t\t\tnum_of_civilian_factories_available_for_projects > '+ num_of_civilian_factories_available_for_projects + '\n')
        file_id.write('\t\t\towns_state = ' + vanilla_state_id + '\n')
        file_id.write('\t\t\tcontrols_state = ' + vanilla_state_id + '\n')
        file_id.write('\t\t}\n')
        file_id.write('\n')
        file_id.write('\t\tvisible = {\n')
        file_id.write('\t\t\towns_state = ' + vanilla_state_id + '\n')
        file_id.write('\t\t\tcontrols_state = ' + vanilla_state_id + '\n')
        file_id.write('\t\t\t' + vanilla_state_id + ' = {\n')
        file_id.write('\t\t\tNOT = { has_state_flag = ' + has_state_flag + ' }\n')
        file_id.write('\t\t\t}\n')
        file_id.write('\t\t}\n')
        file_id.write('\n')
        file_id.write('\t\tfire_only_once = ' + fire_only_once + '\n')
        file_id.write('\t\tcost = ' + cost_PP + '\n')
        file_id.write('\t\tdays_remove = ' + days_remove + '\n')
        file_id.write('\t\tmodifier = {\n')
        file_id.write('\t\t\tcivilian_factory_use = ' + civilian_factory_use + '\n')
        file_id.write('\t\t}\n')
        file_id.write('\t\tai_will_do = { factor = ' + ai_will_do + ' }\n')
        file_id.write('\t\tremove_effect = {\n')
        file_id.write('\t\t\t' + vanilla_state_id + ' = { set_state_flag = ' + has_state_flag + ' }\n')
        file_id.write('\t\t\t' + vanilla_state_id + ' = {\n')
        file_id.write('\t\t\t\tadd_resource = {\n')
        file_id.write('\t\t\t\t\ttype = ' + resource_type + '\n')
        file_id.write('\t\t\t\t\tamount = ' + resource_amount + '\n')
        file_id.write('\t\t\t\t}\n')
        file_id.write('\t\t\t}\n')
        file_id.write('\t\t}\n')
        file_id.write('\t}\n')
        file_id.write('\n')

        file_id2.write(' ' + decision_name + ':0 "Develop ' + state_name + ' Bauxite Deposits."\n')

    file_id.write("}")
    file_id.close()
    file_id2.close()

#    _states_definition_file_location = filedialog.askopenfilename(title = "Select Vanilla Game's State Definition file (definition.csv)", filetypes={("HOI Map file", ".csv"),("All files", "*.*")})
#    for file in os.listdir(_states_definition_file_location):
#        if file.endswith(".txt"):
#            _states_definition_file_location.append(file)



if __name__ == '__main__':
    main()
