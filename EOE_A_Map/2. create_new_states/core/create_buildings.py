

def create_original_provinces_buildings(modify_provinces_ID, original_province_buildings):
    modify_provinces_buildings = []
    for i in range(len(modify_provinces_ID)):
        modify_provinces_buildings.append([modify_provinces_ID[i] ,""])

    for i in range(len(modify_provinces_ID)):
        for j in original_province_buildings:
            if modify_provinces_ID[i] == j[0]:
                modify_provinces_buildings[i][1] = j[1]
    
    return modify_provinces_buildings
