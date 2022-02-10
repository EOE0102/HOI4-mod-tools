import enum
from tkinter import filedialog
import tkinter as Tkinter
from core import read_write_files
import os
import re
import pandas as pd


from PIL import Image
#PictInst.exe for tga image

#from svglib.svglib import svg2rlg
#from reportlab.graphics import renderPDF, renderPM




def read_definition_info():
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = read_write_files.open_file_return_str(title, filetypes)
    all_text_list = read_write_files.split_str_into_list(all_text_str, ';')
    definition_color_address = read_write_files.split_info_definition_csv(all_text_list)
    return definition_color_address




def main():
    definition_color_address = read_definition_info()
    # do step3_step_get_states_info states_info_dict = read_states_info()
    provinces_bmp_file_location = filedialog.askopenfile(title = "Select provinces.bmp Location")
    provinces_bmp_image = Image.open(provinces_bmp_file_location.name).load()

    states_info_dict = read_write_files.read_dict('states_info_dict')
    used_RGB = definition_color_address['RGB']



    province_to_states_list = []
    for i_state, item_state in enumerate(states_info_dict['id']):
        provinces_ids = states_info_dict['provinces'][i_state]
        provinces_id_list = provinces_ids.split(' ')
        provinces_id_list = [ele for ele in provinces_id_list if ele.strip()]
        for i_province, item_province in enumerate(provinces_id_list):
            province_to_state = [item_province, item_state[0]]
            if province_to_state not in province_to_states_list:
                province_to_states_list.append(province_to_state)


    country_flag_folder_location = filedialog.askdirectory(title = "Select Country flag Location")
    country_flag_file_lst = []
    for flag_file in os.listdir(country_flag_folder_location):
        country_flag_file_lst.append([flag_file[0:3], (country_flag_folder_location + '/' + flag_file)])

    country_map_folder_location = filedialog.askdirectory(title = "Select Country Map Location")
    country_map_file_lst = []
    for map_file in os.listdir(country_map_folder_location):
        if map_file.endswith(".bmp"):
            country_map_file_lst.append([map_file[0:3], (country_map_folder_location + '/' + map_file)])

    excel_file_location = filedialog.askopenfile(title = "Select Excel File Location")
    xl_file = pd.read_excel(excel_file_location.name, header = 1)


    export_folder_location = filedialog.askdirectory(title = "Select Export Folder Location")
    if not os.path.exists(export_folder_location + "/common/countries"):
        os.makedirs(export_folder_location + "/common/countries")
    if not os.path.exists(export_folder_location + "/common/country_tags"):
        os.makedirs(export_folder_location + "/common/country_tags")
    if not os.path.exists(export_folder_location + "/gfx/flags"):
        os.makedirs(export_folder_location + "/gfx/flags")
    if not os.path.exists(export_folder_location + "/gfx/flags/medium"):
        os.makedirs(export_folder_location + "/gfx/flags/medium")
    if not os.path.exists(export_folder_location + "/gfx/flags/small"):
        os.makedirs(export_folder_location + "/gfx/flags/small")
    if not os.path.exists(export_folder_location + "/history/countries"):
        os.makedirs(export_folder_location + "/history/countries")
    if not os.path.exists(export_folder_location + "/localisation/english"):
        os.makedirs(export_folder_location + "/localisation/english")
    if not os.path.exists(export_folder_location + "/events"):
        os.makedirs(export_folder_location + "/events")


    common_country_tags = []
    localisation_list = []
    event_add_core_of = []
    for excel_vanilla_id, excel_vanilla_item in enumerate(xl_file['Vanilla']):
        if excel_vanilla_item != "YES":
            new_country_tag = xl_file['TAG'][excel_vanilla_id]
            #create flag
            for country_flag_id, country_flag_item in enumerate(country_flag_file_lst):
                if new_country_tag == country_flag_item[0]:
                    full_filename = country_flag_item[1]
                    #image_filetype = full_filename.split(".")
                    #use format factory convert all to png file
                    #if image_filetype[-1] == 'svg':
                    #    drawing = svg2rlg(full_filename)
                    #    renderPM.drawToFile(drawing, 'temp.png', fmt="PNG")
                    #    im = Image.open('temp.png')
                    #else:
                    country_flag_image = Image.open(full_filename)
                    resized_image = country_flag_image.resize((82, 52))
                    # Error loading flag for country E01 : Ideology democratic : Path gfx/flags/ : Warning slow to read format - Consider using 32D instead of 24bpp
                    resized_image.convert("RGBA").save(export_folder_location + '/gfx/flags/' + new_country_tag + '.tga') 
                    resized_image = country_flag_image.resize((41, 26))
                    resized_image.convert("RGBA").save(export_folder_location + '/gfx/flags/medium/' + new_country_tag + '.tga') 
                    resized_image = country_flag_image.resize((10, 7))
                    resized_image.convert("RGBA").save(export_folder_location + '/gfx/flags/small/' + new_country_tag + '.tga') 
                    
                    # #common\countries\color.txt




            # create common\countries
            common_countries_file_inhalt = []
            common_countries_file_inhalt.append('graphical_culture = '+ xl_file['graphical_culture'][excel_vanilla_id] + '\n')
            common_countries_file_inhalt.append('graphical_culture_2d = '+ xl_file['graphical_culture_2d'][excel_vanilla_id] + '\n')
            common_countries_file_inhalt.append('color = { '+ str(xl_file['color_R'][excel_vanilla_id]) + ' ' + str(xl_file['color_G'][excel_vanilla_id]) + ' ' + str(xl_file['color_B'][excel_vanilla_id]) + ' }\n')
            common_countries_file_name =  str(xl_file['TAG'][excel_vanilla_id]) + ' - ' + str(xl_file['country'][excel_vanilla_id])
            textfile = open(export_folder_location + "/common/countries/" + common_countries_file_name + '.txt', "w")
            for element in common_countries_file_inhalt:
                textfile.write(element)
            textfile.close()

            # create common\country_tags
            common_country_tags.append(xl_file['TAG'][excel_vanilla_id] + ' = "countries/' + common_countries_file_name + '.txt"\n')

            # create localisation
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_fascism:0 "' + str(xl_file['country'][excel_vanilla_id]) + ' Reich"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_fascism_DEF:0 "the ' + str(xl_file['country'][excel_vanilla_id]) + ' Reich"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_democratic:0 "' + str(xl_file['country'][excel_vanilla_id]) + ' Republic"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_democratic:0 "the ' + str(xl_file['country'][excel_vanilla_id]) + ' Republic"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_neutrality:1 "' + str(xl_file['country'][excel_vanilla_id]) + ' Empire"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_neutrality_DEF:1 "the ' + str(xl_file['country'][excel_vanilla_id]) + ' Empire"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_communism:0 "Socialist Republic of ' + str(xl_file['country'][excel_vanilla_id]) + '"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_communism_DEF:0 "the Socialist Republic of ' + str(xl_file['country'][excel_vanilla_id]) + '"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_fascism_ADJ:0 "' + str(xl_file['country'][excel_vanilla_id]) + '"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_democratic_ADJ:0 "' + str(xl_file['country'][excel_vanilla_id]) + '"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_neutrality_ADJ:0 "' + str(xl_file['country'][excel_vanilla_id]) + '"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_communism_ADJ:0 "' + str(xl_file['country'][excel_vanilla_id]) + '"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + ':0 "' + str(xl_file['country'][excel_vanilla_id]) + '"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_DEF:0 "' + str(xl_file['country'][excel_vanilla_id]) + '"\n')
            localisation_list.append(' ' + xl_file['TAG'][excel_vanilla_id] + '_ADJ:0 "' + str(xl_file['country'][excel_vanilla_id]) + '"\n')





            # create history\countries
            history_countries_file_inhalt = []
            found_capital_state_list = []
            found_province_state_list = []
            for country_map_id, country_map_item in enumerate(country_map_file_lst):
                if new_country_tag == country_map_item[0]:
                    full_filename = country_map_item[1]
                    country_map_image = Image.open(full_filename).load()

                    country_map_image_width, country_map_image_height= Image.open(full_filename).size
                    for y in range(0, country_map_image_height):
                        print('finding country TAG ' + str(new_country_tag) + ' ' + str(xl_file['country'][excel_vanilla_id]) + "'s pixels in line " + str(y) + ' of ' + str(country_map_image_height))
                        for x in range(0, country_map_image_width):
                            if country_map_image[x, y] == (255,255,255):
                                found_capital_color = provinces_bmp_image[x, y]
                                found_capital_province = used_RGB.index(list(found_capital_color))
                                for id, item in enumerate(province_to_states_list):
                                    if str(found_capital_province) == str(item[0]):
                                        if item[1] not in found_capital_state_list:
                                            found_capital_state_list.append(item[1])
                            if country_map_image[x, y] == (255,0,1):
                                found_province_color = provinces_bmp_image[x, y]
                                found_state_province = used_RGB.index(list(found_province_color))
                                for id, item in enumerate(province_to_states_list):
                                    if str(found_state_province) == str(item[0]):
                                        if item[1] not in found_province_state_list:
                                            found_province_state_list.append(item[1])


                    history_countries_file_inhalt.append('capital = '+ str(found_capital_state_list[0]) +'\n')
                    history_countries_file_inhalt.append('oob = "USA_states_1936"\n')
                    history_countries_file_inhalt.append('set_technology = {\n')
                    history_countries_file_inhalt.append('    infantry_weapons = 1\n')
                    history_countries_file_inhalt.append('}\n')
                    history_countries_file_inhalt.append('set_popularities = {\n')
                    history_countries_file_inhalt.append('    fascism = 10\n')
                    history_countries_file_inhalt.append('    communism = 30\n')
                    history_countries_file_inhalt.append('    neutrality = 30\n')
                    history_countries_file_inhalt.append('    democratic = 30\n')
                    history_countries_file_inhalt.append('}\n')
                    history_countries_file_inhalt.append('set_politics = {\n')
                    history_countries_file_inhalt.append('    ruling_party = democratic\n')
                    history_countries_file_inhalt.append('    last_election = "1936.1.1"\n')
                    history_countries_file_inhalt.append('    election_frequency = 48\n')
                    history_countries_file_inhalt.append('    elections_allowed = yes\n')
                    history_countries_file_inhalt.append('}\n')

                    textfile = open(export_folder_location + "/history/countries/" + common_countries_file_name + ".txt", "w")
                    for element in history_countries_file_inhalt:
                        textfile.write(element)
                    textfile.close()


                    #event add_core_of
                    event_add_core_of.append('##' +  str(xl_file['TAG'][excel_vanilla_id]) + ' - ' + str(xl_file['country'][excel_vanilla_id]) + '\n')
                    for i, new_state_id in enumerate(found_province_state_list):
                        event_add_core_of.append('\t\t' + str(new_state_id) + ' = { add_core_of = ' + str(xl_file['TAG'][excel_vanilla_id])  + ' }\n')


    #country_tags/export_countries
    textfile = open(export_folder_location + "/common/country_tags/export_countries.txt", "w")
    for element in common_country_tags:
        textfile.write(element)
    textfile.close()

    #localisation/english 
    textfile = open(export_folder_location + "/localisation/english/new_countries_names.txt", "w")
    for element in localisation_list:
        textfile.write(element)
    textfile.close()

    #add_core_of 
    textfile = open(export_folder_location + "/events/new_events.txt", "w")
    for element in event_add_core_of:
        textfile.write(element)
    textfile.close()

    #common\countries\colors.txt


    a = 1

if __name__ == '__main__':
    main()