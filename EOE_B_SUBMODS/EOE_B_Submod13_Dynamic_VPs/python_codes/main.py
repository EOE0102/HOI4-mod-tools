
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

        if states_info_dict['victory_points'][index] != []:
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

        write_inhalt.append('##########################################')
        write_inhalt.append('#EOE_B_Dynamic_VPs')
        write_inhalt.append('##########################################')
        write_inhalt.append('#cant use EOE_B_Dynamic_VPs.1.arms_factory should use EOE_B_Dynamic_VPs.1')        
        write_inhalt.append('add_namespace = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4))
        write_inhalt.append('\t')
        #[12:10:41][namespacemanager.h:210]: Reverse id lookup: id -2141883649 = EOE_B_Dynamic_VPs.999991_0205

        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.10')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.10.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.10.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.11')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.11.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.11.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.12')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.12.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.12.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.20')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.20.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.20.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.21')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.21.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.21.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.22')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.22.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.22.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.30')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.30.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.30.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.31')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.31.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.31.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.32')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.32.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.32.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@air_base > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 2')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')


        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.40')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.40.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.40.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.41')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.41.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.41.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.42')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.42.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.42.desc')
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
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.50')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.50.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.50.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@rocket_site > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 10')
        write_inhalt.append('\t\t}')
        write_inhalt.append('\t}')
        write_inhalt.append('}')


        write_inhalt.append('country_event = {')
        write_inhalt.append('\tid = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.60')
        write_inhalt.append('\ttitle = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.60.title')
        write_inhalt.append('\tdesc = EOE_B_Dynamic_VPs.' + check_state_id[0].zfill(4) + '.60.desc')
        write_inhalt.append('\tfire_only_once = yes')
        write_inhalt.append('\ttrigger = {')
        write_inhalt.append('\t\t' + check_state_id[0] + ' = { check_variable = { building_level@nuclear_reactor > 0 }}')
        write_inhalt.append('\t}')
        write_inhalt.append('\toption = {')
        write_inhalt.append('\t\tadd_victory_points = {')
        write_inhalt.append('\t\t\tprovince = ' + chosen_VP_province)
        write_inhalt.append('\t\t\tvalue = 20')
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
    