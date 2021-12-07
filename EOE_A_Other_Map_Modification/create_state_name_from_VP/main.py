
from tkinter import filedialog
import re

import json #finally find one



def read_dict(variable_str):
    ftypes = [('txt', '.txt'),('All files', '*')]
    path = filedialog.askopenfilename(title = ("load Variable " + str(variable_str)), filetypes = ftypes)
    print('Be patient, reading: ' + str(variable_str))
    with open(path) as f:
        some_variable = json.load(f)
    return some_variable


def main():
    states_info_dict = read_dict('states_info_dict')
    a = 1

    ftypes = [('yml', '.yml'),('All files', '*')]
    path = filedialog.askopenfilename(title = ("load Variable " + str("victory_points_l_english")), filetypes = ftypes)
    with open(path, encoding='utf-8') as f:
        victory_points_info_line = [victory_points_info_line.rstrip() for victory_points_info_line in f]

    new_state_file = []
    RE_VP = re.compile('VICTORY_POINTS_([0-9]+)')

    for item in victory_points_info_line:
        reee = RE_VP.search(item)
        if reee is not None:
            province_ID = ' ' + reee.group(1) + ' '
            province_name = re.search('"(.*)"', item).group(1)
            found_state_ID = ''
            for i in range(len(states_info_dict['provinces'])):
                if province_ID in states_info_dict['provinces'][i]:
                    found_state_ID = states_info_dict['id'][i][0]
                    new_state_file.append(' STATE_'+ found_state_ID + ':0 "' + province_name + '"\n') 


#not/r/n is /r
    new_state_file.sort()
    path = filedialog.askopenfilename(title = ("save language file"))
    textfile = open(path, 'w' ,encoding='utf-8')
    for element in new_state_file:
        textfile.write(element)
    textfile.close()











if __name__ == "__main__":
    main()
    
