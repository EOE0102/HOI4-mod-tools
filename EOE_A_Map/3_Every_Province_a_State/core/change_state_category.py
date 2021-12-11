

def change_state_category(original_state_category, original_provinces_definition, state_category_weight, state_category_type_lst, state_category_type_nochange_lst, 
        modify_victory_points, state_category_victory_points_weight, max_victory_point_weight, modify_provinces_buildings, state_category_provinces_buildings_weight):
    modify_state_category = []
    modify_state_category_matrix = []
    base_weight = -10
    for i in original_provinces_definition:
        for j in state_category_weight:
            if i[3] in j:
                base_weight = max(base_weight, j[1])

    for i in range(len(original_provinces_definition)):
        for j in state_category_weight:
            if original_provinces_definition[i][3] in j:
                temp = j[1] - base_weight
                modify_state_category_matrix.append([original_provinces_definition[i][0], temp])

    #VP
    for i in range(len(modify_victory_points)):
        if modify_victory_points[i][1] != "":
            temp = modify_victory_points[i][1].split()
            temp = float(temp[1])
            temp2 = int(temp/state_category_victory_points_weight) + 1

            for j in range(len(modify_state_category_matrix)):
                if modify_victory_points[i][0] in modify_state_category_matrix[j][0]:#TODO: 123 in 1234? maybe happend
                    modify_state_category_matrix[j][1] = modify_state_category_matrix[j][1] + temp2

           

    #building
    for i in range(len(modify_provinces_buildings)):
        if modify_provinces_buildings[i][1] != "":
            modify_state_category_matrix[i][1] = modify_state_category_matrix[i][1] + 1

    #
    for i in range(len(modify_state_category_matrix)):
        if modify_state_category_matrix[i][1] > 0:
                modify_state_category_matrix[i][1] = 0

    #
    if original_state_category[0] in state_category_type_nochange_lst:
        for i in range(len(modify_state_category_matrix)):
            modify_state_category.append([modify_state_category_matrix[i][0] ,original_state_category[0]])
    else:
        p = state_category_type_lst.index(original_state_category[0])
        for i in range(len(modify_state_category_matrix)):
            if modify_state_category_matrix[i][1] < (0-p):
                modify_state_category_matrix[i][1] = 0-p
            modify_state_category.append([modify_state_category_matrix[i][0], state_category_type_lst[p + modify_state_category_matrix[i][1]]] ) 

    return modify_state_category
