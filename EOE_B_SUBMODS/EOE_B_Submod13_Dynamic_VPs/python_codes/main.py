
from core import *


def main():
    states_info_dict = read_states_info()
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = open_file_return_str(title, filetypes)
    all_text_list = split_str_into_list(all_text_str, ';')
    definition_color_address = split_info_definition_csv(all_text_list)
    used_province_ID = definition_color_address['province ID']
    used_land_sea_lake = definition_color_address['land_sea_lake']
    used_coast = definition_color_address['coast']
    used_terrain = definition_color_address['terrain']
    
    write_inhalt = []
    for check_state_id in states_info_dict['id']:
        index = states_info_dict['id'].index(check_state_id)
        countain_provinces = states_info_dict['provinces'][index]

        if states_info_dict['victory_points'][index][0] != '':
            a = 1
            chosen_VP_province = states_info_dict['victory_points'][index][0].split(' ')[0]

        else:
            
            check_countain_province_list = list(filter(None, countain_provinces.split(' ')))
            chosen_VP_provinces_value_list = []
            chosen_VP_province = '3838'
            for check_province_id in check_countain_province_list:
                check_province_value = 0
                index2 = used_province_ID.index(int(check_province_id))

                if used_land_sea_lake[index2] == 'land':
                    check_province_value = check_province_value + 1
                if used_coast[index2] == 'true':
                    check_province_value = check_province_value + 20
                if used_terrain[index2] == 'ocean':
                    check_province_value = check_province_value - 100
                if used_terrain[index2] == 'lakes':
                    check_province_value = check_province_value - 100
                if used_terrain[index2] == 'forest':
                    check_province_value = check_province_value + 10
                if used_terrain[index2] == 'hills':
                    check_province_value = check_province_value + 10
                if used_terrain[index2] == 'mountain':
                    check_province_value = check_province_value + 5
                if used_terrain[index2] == 'plains':
                    check_province_value = check_province_value + 50
                if used_terrain[index2] == 'urban':
                    check_province_value = check_province_value + 100
                if used_terrain[index2] == 'jungle':
                    check_province_value = check_province_value + 5
                if used_terrain[index2] == 'marsh':
                    check_province_value = check_province_value + 1
                if used_terrain[index2] == 'desert':
                    check_province_value = check_province_value + 1
                chosen_VP_provinces_value_list.append(check_province_value)
            temp2 = chosen_VP_provinces_value_list.index(max(chosen_VP_provinces_value_list))
            chosen_VP_province = check_countain_province_list[temp2]

        #create file inhalt

        write_inhalt.append('##########################################')
        write_inhalt.append('#EOE_B_Dynamic_VPs_' + check_state_id[0])
        write_inhalt.append('##########################################')
        write_inhalt.append('#cant use EOE_B_Dynamic_VPs_1.arms_factory should use EOE_B_Dynamic_VPs.1')
        write_inhalt.append('#cant use EOE_B_Dynamic_VPs_1.arms_factory should use EOE_B_Dynamic_VPs.1')
        # 1:infrastructure
        # 2:arms_factory
        # 3:industrial_complex
        # 4:air_base
        # 5:supply_node
        # 6:rail_way
        # 7:naval_base
        # 8:bunker
        # 9:coastal_bunker
        # 10:dockyard
        # 11:anti_air_building
        # 12:synthetic_refinery
        # 13:fuel_silo
        # 14:radar_station
        # 15:rocket_site
        # 16:nuclear_reactor


        write_inhalt.append('add_namespace = EOE_B_Dynamic_VPs_' + check_state_id[0])
        write_inhalt.append('\t')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0201')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0201.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0201.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@arms_factory > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 1')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0205')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0205.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0205.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@arms_factory > 4 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0210')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0210.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0210.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@arms_factory > 9 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')


        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0301')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0301.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0301.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@industrial_complex > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 1')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0305')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0305.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0305.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@industrial_complex > 4 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0310')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0310.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0310.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@industrial_complex > 9 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')


        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0401')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0401.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0401.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@air_base > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 1')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0405')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0405.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0405.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@air_base > 4 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0410')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0410.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0410.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@air_base > 9 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')


        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0501')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0501.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0501.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@supply_node > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 5')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0701')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0701.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0701.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@naval_base > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 1')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0705')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0705.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0705.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@naval_base > 4 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0710')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0710.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.0710.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@naval_base > 9 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1001')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1001.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1001.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@dockyard > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 1')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1005')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1005.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1005.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@dockyard > 4 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1010')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1010.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1010.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@dockyard > 9 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1601')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1601.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs_' + check_state_id[0] + '.1601.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@nuclear_reactor > 9 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 10')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')








    textfile = open( 'EOE_B_Submod13_Dynamic_VPs_events.txt', "w")
    
    for element in write_inhalt:
        textfile.write(element)
        textfile.write('\n')
    textfile.close()


if __name__ == "__main__":
    main()
    