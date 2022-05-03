
import numpy #pip install numpy



def miller_cylinder_forward_projection(theta_in_rand):
    longitude_in_what = 1.25 * numpy.log(numpy.tan(numpy.pi / 4 + 0.4 * theta_in_rand))
    return longitude_in_what

def miller_cylinder_inverse_projection(longitude_in_what):
    theta_in_rand = 2.5 * (numpy.arctan(numpy.exp(0.8 * longitude_in_what)) - numpy.pi / 4)
    return theta_in_rand


#im.save("pixel_grid.bmp")
iterate_amount = 2
#equatorialPosition = 1350
longitude_north = 72
longitude_south = 57
longitude_north_in_rand = longitude_north/ 180 * numpy.pi
longitude_south_in_rand = longitude_south/ 180 * numpy.pi
longitude_north2D = miller_cylinder_forward_projection(longitude_north_in_rand)
longitude_south2D = miller_cylinder_forward_projection(longitude_south_in_rand)

default_province_size = 20 #pixel on equator #20=> 18847 16=>20359 don't use 16 too harsh
max_new_provinces_per_state = 5 #max 5 block because range(1, new_province_max_amount):


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
        'new_province_max_amount': [3,3,4,2,4,3,3,2]
    }
    #countrytag, continent ['DEN',1]

#   continents = 
#	europe
#	north_america
#	south_america
#	australia
#	africa
#	asia
#	middle_east

    owner_okay_list = [['POR',1], ['SPR',1], ['FRA',1], ['ITA',1], ['GER',1], ['CZE',1], ['AUS',1],  #west europa
        ['POL',1], ['HUN',1], ['ROM',1], ['BUL',1], ['YUG',1], ['ALB',1], ['GRE',1],  #east europa
        ['LIT',1], ['LAT',1], ['EST',1], #little three
        ['BEL',1], ['HOL',1], ['LUX',1], #Netherlands
        ['ENG',1], ['IRE',1], #UK
        ['FIN',1], ['SWE',1], ['NOR',1], ['DEN',1],#north europa
        ['TUR',1], ['TUR',7], ['PER',7], #turkey in europa and middle east
        ['SOV',1], ['SOV',7], #sov in europa and middle east
        ['ETH',5]] #Africa


    add_core_of_list = ['LIB', #test country
    'ERI', 'DJI', 'SOM', #horn of africa
    'SUD', 'UGA', 'KEN', 'TZN', 'MZB', 'MLW', 'MAD',#east africa
    #'ZAM', 'BOT', 'SAF', 'ANG', 'COG', 'RCG', 'GAB', 'CMR', 'GHA','IVO','GNA', 'MLI', 'NGA','ELS','CHA','VOL',#middle Africa
    'CHI', 'PRC', #china
    'KOR', #japan?
    'VIN', 'LAO', 'CAM', 'SIA', 'BRM', #south east asia
    'EGY', 'LBA', 'TUN', 'ALG', 'MOR', #north africa
    'PAL', 'ISR', 'JOR', 'SYR', 'IRQ'] #middle east

    new_province_max_amount = 1
    if len(state_info_impassable) > 0:
        return new_province_max_amount, state_info_terrain

    elif [state_info_owner[0], state_info_continent] in owner_okay_list:
        if state_info_terrain in terrain_okay_dict['terrain']:
            new_province_max_amount = terrain_okay_dict['new_province_max_amount'][(terrain_okay_dict['terrain'].index(state_info_terrain))]

    elif (str(state_info_add_core_of)[2:5] in add_core_of_list) or (str(state_info_add_core_of)[9:12] in add_core_of_list):
        if state_info_terrain in terrain_okay_dict['terrain']:
            new_province_max_amount = terrain_okay_dict['new_province_max_amount'][(terrain_okay_dict['terrain'].index(state_info_terrain))]
    
    return new_province_max_amount,  state_info_terrain


def calculate_divide_province_amount(image_height, default_province_size, longitude_north2D, longitude_south2D, rgb_area_main_POG, RGBAreaFullSize, max_new_provinces_per_state, state_info_terrain):
    # according to altitude
    equatorPosition = round(longitude_north2D/(longitude_north2D + longitude_south2D) * image_height)
    longitude2DHeight = rgb_area_main_POG[1]
    longitudeInBall = (longitude_north2D + longitude_south2D)/image_height * longitude2DHeight - longitude_north2D
    longitudeInBallInRand = miller_cylinder_inverse_projection(abs(longitudeInBall))

    xMagnify = 1/(numpy.cos(longitudeInBallInRand))
    #longitudeInBallInRand = longitudeInBallInRand/np.pi * 180
    temp1 = abs(abs(miller_cylinder_forward_projection(abs(longitudeInBallInRand) + 0.05)) - abs(miller_cylinder_forward_projection(abs(longitudeInBallInRand) - 0.05)))
    temp2 = miller_cylinder_forward_projection(0.05)*2
    yMagnify = temp1/temp2 #area near equator, difference is not accurate
    if yMagnify < 1: 
        yMagnify = 1
    areaMagnify = xMagnify * yMagnify

    refileProvinceSize = default_province_size * areaMagnify
        
    amountProvince = int(round(RGBAreaFullSize/refileProvinceSize -0.5 ))
    if state_info_terrain == 'urban':
        amountProvince = max_new_provinces_per_state
        # don't do too harsh, divide province into 1 - 10 pieces
    if amountProvince == 0:
        amountProvince = 1
    if amountProvince >= max_new_provinces_per_state:
        amountProvince = max_new_provinces_per_state
            
    return amountProvince

    