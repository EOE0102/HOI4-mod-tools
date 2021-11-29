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