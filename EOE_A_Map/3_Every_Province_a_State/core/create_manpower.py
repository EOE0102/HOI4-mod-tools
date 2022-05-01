
def change_manpower(original_state_manpower, original_provinces_definition, manpower_weight, coast_weight, 
        modify_victory_points, manpower_victory_points_weight, max_victory_point_weight, modify_provinces_buildings, manpower_provinces_buildings_weight):
    modify_manpower = []
    modify_manpower_matrix = []
    base_weight = 0
    total_manpower = float(original_state_manpower[0])


    for i in original_provinces_definition:
        for j in manpower_weight:
            if i[3] in j:
                modify_manpower_matrix.append([i[0], j[1]])

    #add manpower according to coast
    for i in range(len(original_provinces_definition)):
        if original_provinces_definition[i][2] == "true":
            modify_manpower_matrix[i][1] = modify_manpower_matrix[i][1] * coast_weight

    #add manpower according to VP
    for i in range(len(modify_victory_points)):
        if modify_victory_points[i][1] != "":
            temp = modify_victory_points[i][1].split()
            temp = float(temp[1])
            if temp > max_victory_point_weight:
                temp = max_victory_point_weight
                for j in range(len(modify_manpower_matrix)):
                    if modify_victory_points[i][0] in modify_manpower_matrix[j][0]:#TODO: 123 in 1234? maybe happend
                        modify_manpower_matrix[j][1] = modify_manpower_matrix[j][1] * (1 + temp*manpower_victory_points_weight)


    # and lakes always located in the 0 position.
    #add manpower according to buildings
    for i in range(len(modify_provinces_buildings)):
        if i == 0:
            if modify_provinces_buildings[0][1] != "":
                modify_manpower_matrix[0][1] = modify_manpower_matrix[0][1] * (1 + 1*manpower_provinces_buildings_weight)
        else:
            temp_id1 = modify_provinces_buildings[i][0]
            for j in range(len(modify_manpower_matrix)):
                temp_id2 = modify_manpower_matrix[j][0]
                if temp_id1 == temp_id2:
                    if modify_provinces_buildings[i][1] != "":
                        modify_manpower_matrix[j][1] = modify_manpower_matrix[j][1] * (1 + 1*manpower_provinces_buildings_weight)

                

    #cal. base weight
    for i in modify_manpower_matrix:
        base_weight = base_weight + i[1]
    
    #cal.
    for i in range(len(modify_manpower_matrix)):
        temp = int(total_manpower * modify_manpower_matrix[i][1] / base_weight)
        if temp <= 0:
            temp = 1
        modify_manpower.append([modify_manpower_matrix[i][0], temp])
    
    return modify_manpower