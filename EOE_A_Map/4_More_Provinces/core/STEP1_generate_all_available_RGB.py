from tkinter import filedialog
from core import read_write_files


## PART 1 ##
def step_save_all_color_into_file():
    all_color = list_all_RGB()
    save_color_into_file(all_color)
    print('Part 1 finished')

def list_all_RGB():
    #R range 0-10 42-52, 84-94, 126-136, 168-178 + 210-220
    #G range 0-210
    #B range 0,5,10,15,20 ...225
    all_color_R = []
    all_color_G = []
    all_color_B = []
    all_color = []
    for i in range(20):
        all_color_R.append((10*i))

    for i in range(25):
        all_color_G.append(8*i)

    #for i in range(46):
    for i in range(20):
        all_color_B.append(10*i)

    for i in all_color_R:
        for j in all_color_G:
            for k in all_color_B:
                all_color.append([i,j,k])
                
    all_color.remove([0,0,0])
    return all_color

def save_color_into_file(all_color):
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = read_write_files.open_file_return_str(title, filetypes)
    all_text_list = read_write_files.split_str_into_list(all_text_str, ';')
    definition_color_address = read_write_files.split_info_definition_csv(all_text_list)
    used_RGB = definition_color_address['RGB']


    save_file = filedialog.asksaveasfilename(title = "save all_RGB_list.txt")
    with open(save_file, 'w') as filehandle:
        for i in range(len(all_color)):
            R = str(all_color[i][0])
            G = str(all_color[i][1])
            B = str(all_color[i][2])
            #filehandle.write(R + ','+ G+',' + B +'\n')
            #if i % 5 == 4:

            if not([int(R),int(G),int(B)] in used_RGB):
                filehandle.write("%s;%s;%s\n" % (R,G,B))
    filehandle.close()

