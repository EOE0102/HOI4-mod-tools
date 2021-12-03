
import numpy as np #pip install numpy
import re


def miller_cylinder_forward_projection(theta_in_rand):
    longitude_in_what = 1.25 * np.log(np.tan(np.pi / 4 + 0.4 * theta_in_rand))
    return longitude_in_what

def miller_cylinder_inverse_projection(longitude_in_what):
    theta_in_rand = 2.5 * (np.arctan(np.exp(0.8 * longitude_in_what)) - np.pi / 4)
    return theta_in_rand

#im.save("pixel_grid.bmp")
iterate_amount = 2
#equatorialPosition = 1350
longitude_north = 72
longitude_south = 57
longitude_north_in_rand = longitude_north/ 180 * np.pi
longitude_south_in_rand = longitude_south/ 180 * np.pi
longitude_north2D = miller_cylinder_forward_projection(longitude_north_in_rand)
longitude_south2D = miller_cylinder_forward_projection(longitude_south_in_rand)

default_province_size = 20 #pixel on equator
max_new_provinces_per_state = 5



#TODO Define painting state conditions
def correct_new_province_max_amount(max_new_provinces_per_state, rgb_area_main_RGB, definition_info_dict, states_info_dict):

    index_in_definition = definition_info_dict['RGB'].index(rgb_area_main_RGB)
    state_info_continent = definition_info_dict['continent'][index_in_definition]
    state_info_terrain = definition_info_dict['terrain'][index_in_definition]
    state_info_coast = definition_info_dict['coast'][index_in_definition]
    #because of lake STATE! province 13165 13180 are lake province' 1426 ' => ' 1426 13165 13180 '

    index_in_state_file = [idx for idx, elem in enumerate(states_info_dict['provinces']) if (' ' + str(index_in_definition) + ' ') in elem][0]

    #index_in_state_file = states_info_dict['provinces'].index((' ' + str(index_in_definition) + ' '))


    state_info_id = states_info_dict['id'][index_in_state_file]
    state_info_state_category = states_info_dict['state_category'][index_in_state_file]
    state_info_impassable = states_info_dict['impassable'][index_in_state_file]
    state_info_resources = states_info_dict['resources'][index_in_state_file]
    state_info_provinces = states_info_dict['provinces'][index_in_state_file]
    state_info_victory_points = states_info_dict['victory_points'][index_in_state_file]
    state_info_owner = states_info_dict['owner'][index_in_state_file]
    state_info_add_core_of = states_info_dict['add_core_of'][index_in_state_file]

    #terrain unknown ocean lakes forest hills mountain plains urban jungle marsh desert water_fjords water_shallow_sea water_deep_ocean
    terrain_okay_dict = {
        'terrain': ['forest', 'hills', 'mountain', 'plains', 'urban', 'jungle', 'marsh', 'desert'],
        'new_province_max_amount': [3,3,3,2,4,3,2,2]
    }
    #countrytag, continent ['DEN',1]
    owner_okay_list = [['SPR',1], ['FRA',1], ['ITA',1], ['GER',1], ['CZE',1], ['POL',1], ['AUS',1], 
        ['HUN',1], ['ROM',1], ['BUL',1], ['YUG',1], ['GRE',1], ['LIT',1], ['LAT',1], ['EST',1],
        ['BEL',1], ['HOL',1], ['LUX',1], ['ENG',1],
        ['SOV',1], ['ETH',5]]


    add_core_of_list = ['LIB', 'CHI', 'PRC', 'KOR', 'LBA', 'EGY']
    new_province_max_amount = 1
    if len(state_info_impassable) > 0:
        return new_province_max_amount

    elif [state_info_owner[0], state_info_continent] in owner_okay_list:
        if state_info_terrain in terrain_okay_dict['terrain']:
            new_province_max_amount = terrain_okay_dict['new_province_max_amount'][(terrain_okay_dict['terrain'].index(state_info_terrain))]

    elif (str(state_info_add_core_of)[2:5] in add_core_of_list) or (str(state_info_add_core_of)[9:12] in add_core_of_list):
        if state_info_terrain in terrain_okay_dict['terrain']:
            new_province_max_amount = terrain_okay_dict['new_province_max_amount'][(terrain_okay_dict['terrain'].index(state_info_terrain))]
    
    return new_province_max_amount
