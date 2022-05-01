import tkinter as Tkinter
from tkinter import filedialog
import os
import re
import copy

def reminder_initialize(new_state_remider_original_lst):
    new_state_remider_lst = []
    for i in new_state_remider_original_lst:
        temp = i.split(":")
        temp[1] = temp[1].replace("\n", "")
        temp[1] = temp[1].strip()
        temp[0] = temp[0].replace(" ","")
        new_state_remider_lst.append([temp[0], temp[1]]) 
    return new_state_remider_lst


def str_initialize(all_text_in_lst):
    for i in range(len(all_text_in_lst)):
        if "#" in all_text_in_lst[i]:
            all_text_in_lst[i] = all_text_in_lst[i].split("#",1)[0]
            all_text_in_lst[i] = all_text_in_lst[i] + "\n"
        
        all_text_in_str_initialized = "".join(all_text_in_lst)
    return all_text_in_str_initialized

def __folder_files_prepearation():
    root = Tkinter.Tk()
    import_file_folder_location = filedialog.askdirectory(title = "Select Event(or any relative files) Location")


    #export_folder_location = filedialog.askdirectory(title = "Select Export Folder Location")
    export_folder_location = os.getcwd() + "/export/"
    if not os.path.exists(export_folder_location):
        os.makedirs(export_folder_location)

    new_state_reminder_definition_file_location = filedialog.askopenfilename(title = "Select new_state_reminder_ file(new_state_reminder_.txt)", filetypes={("HOI Map file", ".txt"),("All files", "*.*")})
    return import_file_folder_location, export_folder_location, new_state_reminder_definition_file_location

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


def find_first_enter_letter_after_kw(_kw_position_int, _list):
    for i in _list:
        if i > _kw_position_int:
            return i
    return -1


def find_last_letter_before_kw(_kw_position_int, _list):
    for i in range(len(_list)):
        if _list[i] > _kw_position_int:
            return _list[i-1]
    return -1


def find_first_bracket_after_kw(_kw_position, _open_bracket_lst, _close_bracket_lst):
    _first_open_bracket_position = find_first_enter_letter_after_kw(_kw_position, _open_bracket_lst)
    a = 1
    _next_bracket_position = _first_open_bracket_position

    while a != 0:
        _next_open_bracket_position = find_first_enter_letter_after_kw(_next_bracket_position, _open_bracket_lst)
        if _next_open_bracket_position < 0: #bug last open bracket
            _next_open_bracket_position = 99999999
        _next_close_bracket_position = find_first_enter_letter_after_kw(_next_bracket_position, _close_bracket_lst)
        _next_bracket_position = min(_next_open_bracket_position, _next_close_bracket_position)
        

        if _next_close_bracket_position < _next_open_bracket_position: #good
            a = a - 1
        else:
            a = a + 1

        if a == 0:
            return _next_bracket_position




def add_provinces_after_kw(_new_import_file_str, _find_str, _start_mark, _end_mark, _new_state_remider_lst):

    kw_position = [m.start() for m in re.finditer(r"\s" + _find_str + r"\s+" + "=" + r"\s+" + _start_mark, _new_import_file_str)]
    #temp = re.findall(r"\s+" + find_str + r"\s+" + "=" + r"\s+" + "{", _new_import_file_str)

    if kw_position != []:
        for i in range(len(kw_position)):
            new_combined_state_str = ""
            kw_position = [m.start() for m in re.finditer(r"\s" + _find_str + r"\s+" + "=" + r"\s+" + _start_mark, _new_import_file_str)]
            open_bracket_position_lst = [m.start() for m in re.finditer(_start_mark, _new_import_file_str)]
            close_bracket_position_lst = [m.start() for m in re.finditer(_end_mark, _new_import_file_str)]

            open_bracket_position = find_first_enter_letter_after_kw(kw_position[i], open_bracket_position_lst)
            close_bracket_position = find_first_bracket_after_kw(kw_position[i], open_bracket_position_lst, close_bracket_position_lst)

            _inhalt_states_id_str = _new_import_file_str[open_bracket_position+1:close_bracket_position]
            _inhalt_states_id_str = _inhalt_states_id_str.strip()
            _inhalt_states_id_lst = _inhalt_states_id_str.split(" ")



            for j in range(len(_inhalt_states_id_lst)):
                for k in _new_state_remider_lst:
                    if _inhalt_states_id_lst[j] == k[0]:
                        _found_new_states = k[1]
                        new_combined_state_str = new_combined_state_str + " " + _found_new_states
            _new_import_file_str = _new_import_file_str[:close_bracket_position] + new_combined_state_str + _new_import_file_str[close_bracket_position:]

    return _new_import_file_str


def add_item_after_kw(_new_import_file_str, _find_str,_start_mark, _end_mark, _new_state_remider_lst):
    _kw_position = [m.start() for m in re.finditer(r"\s" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)]
    i = 0
    if _kw_position != []:
        while i < len(_kw_position):
            _new_combined_state_str = ""
            _kw_position = [m.start() for m in re.finditer(r"\s+" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)]
            _kw = re.findall(r"\s+" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)
            _space_position = [m.start() for m in re.finditer(r"\s" , _new_import_file_str)]
            _end_state_position = find_first_enter_letter_after_kw(_kw_position[i] + len(_kw[i]), _space_position)
            _state_id = _new_import_file_str[_kw_position[i] + len(_kw[i]) : _end_state_position]
            
            i = i + 1
            for j in _new_state_remider_lst:
                
                if _state_id == j[0]:
                    
                    _found_new_states = j[1]
                    _found_new_states_lst = _found_new_states.split()
                    for k in _found_new_states_lst:
                        _new_combined_state_str = _new_combined_state_str + " \n\t\t" + _find_str + " = " + k
                        i = i + 1	

            _new_import_file_str = _new_import_file_str[:_end_state_position] + _new_combined_state_str + _new_import_file_str[_end_state_position:]
            _kw_position = [m.start() for m in re.finditer(r"\s" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)]
    return _new_import_file_str



def add_item_before_kw(_new_import_file_str, _find_str, _start_mark, _end_mark, _start_mark2, _end_mark2, _new_state_remider_lst):
    _kw_position = [m.start() for m in re.finditer(r"\s" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)]
    i = 0
    if _kw_position != []:
        #because I modify the file 
        while i < len(_kw_position):
            _kw_position = [m.start() for m in re.finditer(r"\s" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)]
            _new_combined_state_str = ""
            #_kw = re.findall(r"\s+" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)
            #_space_position = [m.start() for m in re.finditer(r"\s" , _new_import_file_str)]
            #_end_state_position = find_first_enter_letter_after_kw(_kw_position[i] + len(_kw[i]), _space_position)
            #_info = _new_import_file_str[_kw_position[i] + len(_kw[i]) : _end_state_position] # yes /no /AUS ...
            _state_id_position = [m.start() for m in re.finditer(r"\s+\d+\s+" + _start_mark + r"\s+", _new_import_file_str)]
            _state_id = re.findall(r"\s+\d+\s+" + _start_mark + r"\s+", _new_import_file_str)
            temp1 = find_last_letter_before_kw(_kw_position[i], _state_id_position)

            if temp1 < 0: #no id not found
                i = i + 1
            elif _kw_position[i] - temp1 > 20: # bug like this:537 = /r/r {add_core_of = FROM} 
		                #153 = {if = {limit = { is_owned_by = AUS }add_core_of = GER}}
                i = i + 1
            else:
                for temp2 in range(len(_state_id_position)):
                    if temp1 == _state_id_position[temp2]:
                        _old_state_info = _new_import_file_str[temp1 : temp1 + len(_state_id[temp2])]
                _old_state = re.findall(r"\d+", _old_state_info)[0]

                open_bracket_position_lst = [m.start() for m in re.finditer(_start_mark2, _new_import_file_str)]
                close_bracket_position_lst = [m.start() for m in re.finditer(_end_mark2, _new_import_file_str)]
                _first_open_bracket_position = find_first_enter_letter_after_kw(temp1, open_bracket_position_lst)
                _last_close_bracket_position = find_first_bracket_after_kw(temp1, open_bracket_position_lst, close_bracket_position_lst)

                _inhalt_within_bracket = _new_import_file_str[_first_open_bracket_position: _last_close_bracket_position + 1]

                for j in _new_state_remider_lst:
                    if _old_state == j[0]:
                        i = i + 1
                        _found_new_states = j[1]
                        _found_new_states_lst = _found_new_states.split()
                        for k in _found_new_states_lst:
                            _new_combined_state_str = _new_combined_state_str + " \n\t\t" + k + " = " +  _inhalt_within_bracket 
                            i = i + 1

                    
                _new_import_file_str = _new_import_file_str[:_last_close_bracket_position+1] + _new_combined_state_str + _new_import_file_str[_last_close_bracket_position+1:]
                _kw_position = [m.start() for m in re.finditer(r"\s" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)]


    return _new_import_file_str




def add_item_before_kw_V2(_new_import_file_str, _find_str, _start_mark, _end_mark, _start_mark2, _end_mark2, _new_state_remider_lst):
    _kw_position = [m.start() for m in re.finditer(r"\s" + _find_str + r"\s+" + _start_mark + r"\s+", _new_import_file_str)]
    all_possible_province_position_with_bracket =  [m.start() for m in re.finditer(r"\s" + r"\d+" + r"\s+" + "=" + r"\s+" + "{", _new_import_file_str)]
    all_possible_province_position =  [m.start() for m in re.finditer(r"\d+", _new_import_file_str)]
    all_equal_position =  [m.start() for m in re.finditer("=", _new_import_file_str)]

    all_left_bracket_position =  [m.start() for m in re.finditer("{", _new_import_file_str)]
    all_right_bracket_position =  [m.start() for m in re.finditer("}", _new_import_file_str)]
    all_bracket_position = []
    all_bracket_position.extend(all_left_bracket_position)
    all_bracket_position.extend(all_right_bracket_position)
    all_bracket_position.sort()
    all_bracket_position_plus_minus = []
    for element in all_bracket_position:
        if element in all_left_bracket_position: 
            all_bracket_position_plus_minus.append(1)
        else: #element in all_right_bracket_position
            all_bracket_position_plus_minus.append(-1)


    insert_position_text_list = []
    for possible_province_position in all_possible_province_position_with_bracket:
        first_left_bracket_position_index = next(x[0] for x in enumerate(all_bracket_position) if x[1] > possible_province_position)
        nearest_province_position_index = next(x[0] for x in enumerate(all_possible_province_position) if x[1] > possible_province_position)
        nearest_equal_position_index = next(x[0] for x in enumerate(all_equal_position) if x[1] > possible_province_position)

        nearest_province_position = all_possible_province_position[nearest_province_position_index]
        nearest_equal_position = all_equal_position[nearest_equal_position_index]
        nearest_province = str(int(_new_import_file_str[nearest_province_position:nearest_equal_position]))


        first_left_bracket_position = all_bracket_position[first_left_bracket_position_index]
        #next is {
        next_bracket_position_index = first_left_bracket_position_index
        bracket_balance = 1
        while bracket_balance != 0:
            next_bracket_position_index = next_bracket_position_index + 1
            bracket_balance = bracket_balance + all_bracket_position_plus_minus[next_bracket_position_index]
        
        last_right_bracket_position = all_bracket_position[next_bracket_position_index]
        inhalt_between_bracket = _new_import_file_str[first_left_bracket_position:last_right_bracket_position+1]

        if _find_str in inhalt_between_bracket:

            for item in _new_state_remider_lst:
                if nearest_province == item[0]:
                    if item[1] != '':
                        _found_new_states = item[1]
                        _found_new_states_lst = _found_new_states.split()
                        _new_insert_text_str = ''
                        for k in _found_new_states_lst:
                            _new_insert_text_str = _new_insert_text_str + " \n\t\t" + k + " = " + inhalt_between_bracket
                        _new_insert_text_str = _new_insert_text_str + '\n'
                        insert_position_text_list.append([last_right_bracket_position + 1, _new_insert_text_str])

    a = 1
    text_start_position = 0
    new_text_string = ''
    if len(insert_position_text_list) != 0:
        for item in insert_position_text_list:
            insert_position = item[0]
            insert_text = item[1]
            new_text_string = new_text_string + _new_import_file_str[text_start_position:insert_position] + insert_text
            text_start_position = insert_position + 1
        new_text_string = new_text_string + _new_import_file_str[insert_position_text_list[-1][0]+1:]
        return new_text_string
    else:
        return _new_import_file_str

    









def write_file(_export_folder_location, _file_name, _file_str):
    f = open(_export_folder_location + "/" + _file_name, "w+", encoding='gb18030', errors='ignore')
    f.write(_file_str)
    f.close()


def main():
    import_file_folder_location, export_folder_location, new_state_reminder_definition_file_location = __folder_files_prepearation()
    
    new_state_remider_file = open(new_state_reminder_definition_file_location, "r")
    new_state_remider_original_lst = new_state_remider_file.readlines()
    new_state_remider_file.close()
    
    new_state_remider_lst = reminder_initialize(new_state_remider_original_lst)
    

    event_file_lst = []
    for file in os.listdir(import_file_folder_location):
        if file.endswith(".txt"):
            event_file_lst.append(file)


    for import_file_name in event_file_lst:
        #'gbk' codec can't decode byte 0xbf in position 2: illegal multibyte sequence
        import_file = open(str(import_file_folder_location) + "/" + str(import_file_name), encoding='gb18030', errors='ignore')
        original_import_file_lst = import_file.readlines()
        import_file.close()

        new_import_file_str = str_initialize(original_import_file_lst)
        f = copy.deepcopy(new_import_file_str)

        # states = {}
        find_str = "states"
        start_mark = "{"
        end_mark = "}"
        new_import_file_str = add_provinces_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        # add_state_claim
        start_mark = "="
        end_mark = r"\D"

        find_str = "add_state_claim"
        new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        find_str = "remove_state_claim"
        new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        find_str = "add_state_core"
        new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        find_str = "remove_state_core"
        new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        find_str = "transfer_state"
        new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        #find_str = "owns_state"
        #new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        #find_str = "controls_state"
        #new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        find_str = "set_state_controller"
        new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)

        find_str = "\tstate"
        new_import_file_str = add_item_after_kw(new_import_file_str, find_str, start_mark, end_mark, new_state_remider_lst)



        start_mark = "="
        end_mark = r"\W"
        start_mark2 = "{"
        end_mark2 = "}"
        find_str = "is_demilitarized_zone"
        new_import_file_str = add_item_before_kw_V2(new_import_file_str, find_str, start_mark, end_mark , start_mark2, end_mark2, new_state_remider_lst)

        find_str = "set_demilitarized_zone"
        new_import_file_str = add_item_before_kw_V2(new_import_file_str, find_str, start_mark, end_mark , start_mark2, end_mark2, new_state_remider_lst)

        find_str = "add_core_of"
        new_import_file_str = add_item_before_kw_V2(new_import_file_str, find_str, start_mark, end_mark , start_mark2, end_mark2, new_state_remider_lst)

        #TODO ai_strategy _economic

        if f != new_import_file_str:
            write_file(export_folder_location, import_file_name, new_import_file_str)



if __name__ == '__main__':
    main()