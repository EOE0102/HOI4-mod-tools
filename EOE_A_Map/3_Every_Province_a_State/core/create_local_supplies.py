

def change_local_supplies(original_local_supplies, original_provinces_definition, state_local_supplies_weight, 
            modify_victory_points, local_supplies_victory_points_weight, modify_provinces_buildings, local_supplies_buildings_weight):

    _modify_local_supplies = []
    modify_local_supplies_matrix = []

    for i in range(len(original_provinces_definition)):
        for j in state_local_supplies_weight:
            if original_provinces_definition[i][3] in j:
                temp = j[1]
                modify_local_supplies_matrix.append([original_provinces_definition[i][0], temp])

    #VP 
    for i in range(len(modify_victory_points)):
        if modify_victory_points[i][1] != "":
            temp = modify_victory_points[i][1].split()
            temp = float(temp[1]) * local_supplies_victory_points_weight

            
            for j in range(len(modify_local_supplies_matrix)):
                if modify_victory_points[i][0] in modify_local_supplies_matrix[j][0]:#TODO: 123 in 1234? maybe happend
                    modify_local_supplies_matrix[j][1] = modify_local_supplies_matrix[j][1] + temp



    #buildings
    for i in range(len(modify_provinces_buildings)):
        if i == 0:
            if modify_provinces_buildings[0][1] != "":
                modify_local_supplies_matrix[0][1] = modify_local_supplies_matrix[0][1] + local_supplies_buildings_weight
        else:
            temp_id1 = modify_provinces_buildings[i][0]
            for j in range(len(modify_local_supplies_matrix)):
                temp_id2 = modify_local_supplies_matrix[j][0]
                if temp_id1 == temp_id2:
                    if modify_provinces_buildings[i][1] != "":
                        modify_local_supplies_matrix[j][1] = modify_local_supplies_matrix[j][1] + local_supplies_buildings_weight


    # divide
    for i in range(len(modify_local_supplies_matrix)):
        if modify_local_supplies_matrix[i][1] < 0:
                modify_local_supplies_matrix[i][1] = 0

    local_supplies_sum = 0
    for i in range(len(modify_local_supplies_matrix)):
        local_supplies_sum = local_supplies_sum + modify_local_supplies_matrix[i][1]


    for i in range(len(modify_local_supplies_matrix)):
        if local_supplies_sum == 0:
            temp4 = 0.0
        elif original_local_supplies == []: #yes developteam forget to add local suppolies, LOL
            temp4 = 0.0
        else:
            temp4 = modify_local_supplies_matrix[i][1] / local_supplies_sum * float(original_local_supplies[0])
        temp4 = round(temp4,1)
        _modify_local_supplies.append([modify_local_supplies_matrix[i][0], temp4])
        
    return _modify_local_supplies
