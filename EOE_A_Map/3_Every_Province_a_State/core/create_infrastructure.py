
def change_infrastructure_level(original_infrastructure, original_provinces_definition, state_infrastructure_weight, 
        modify_victory_points, infrastructure_victory_points_weight, max_victory_point_weight, modify_provinces_buildings, infrastructure_provinces_buildings_weight):
        
    _modify_infrastructure_level = []
    modify_infrastructure_level_matrix = []
    base_weight = -10
    for i in original_provinces_definition:
        for j in state_infrastructure_weight:
            if i[3] in j:
                base_weight = max(base_weight, j[1])

    for i in range(len(original_provinces_definition)):
        for j in state_infrastructure_weight:
            if original_provinces_definition[i][3] in j:
                temp = j[1] - base_weight
                modify_infrastructure_level_matrix.append([original_provinces_definition[i][0], temp])

    #VP 
    for i in range(len(modify_victory_points)):
        if modify_victory_points[i][1] != "":
            temp = modify_victory_points[i][1].split()
            temp = float(temp[1])
            temp2 = int(temp/infrastructure_victory_points_weight) + 0.51
            if temp2 > 1:
                temp2 = 1

                for j in range(len(modify_infrastructure_level_matrix)):
                    if modify_victory_points[i][0] in modify_infrastructure_level_matrix[j][0]:#TODO: 123 in 1234? maybe happend
                        modify_infrastructure_level_matrix[j][1] = modify_infrastructure_level_matrix[j][1] + temp2



    #buildings
    for i in range(len(modify_provinces_buildings)):
        if modify_provinces_buildings[i][1] != "":
            modify_infrastructure_level_matrix[i][1] = modify_infrastructure_level_matrix[i][1] + 0.51

    # max +1
    for i in range(len(modify_infrastructure_level_matrix)):
        temp4 = modify_infrastructure_level_matrix[i][1] + int(original_infrastructure[0])
        temp4 = int(round(temp4))
        if temp4 > 5:
            temp4 = 5
        if temp4 < 1:
            temp4  = 1
        if int(original_infrastructure[0]) == 0:
            temp4  = 0
        _modify_infrastructure_level.append([modify_infrastructure_level_matrix[i][0], temp4])
        
    return _modify_infrastructure_level
