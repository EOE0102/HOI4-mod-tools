
import re

def create_victory_points(modify_provinces_ID, original_victory_points):
    modify_victory_points = []
    
    for i in modify_provinces_ID:
        modify_victory_points.append([i,""])

    for i in range(len(modify_provinces_ID)):
        for j in original_victory_points:
            temp = re.findall(r"\D+" + modify_provinces_ID[i] +r"\s+\d",j)
            temp2 = ""
            if temp != []:
                j = j.replace(temp[0][:-1], "")
                j = j.replace("#", "")
                victory_point = int(float(j))
                changed_victory_point = change_victory_points(victory_point)
                temp2 = str(changed_victory_point)
                modify_victory_points[i][1] = str(modify_provinces_ID[i])+ " "+ temp2

    return modify_victory_points

def change_victory_points(original_victory_points_of_province):

    changed_victory_point = original_victory_points_of_province

    if original_victory_points_of_province <= 3:
        changed_victory_point = original_victory_points_of_province * 5
    elif 3 < original_victory_points_of_province <= 10:
        changed_victory_point = (original_victory_points_of_province - 3) * 4 + 15
    elif 10 < original_victory_points_of_province <= 20:
        changed_victory_point = (original_victory_points_of_province - 10) * 3 + 40
    elif 20 < original_victory_points_of_province <= 30:
        changed_victory_point = (original_victory_points_of_province - 20) * 2 + 70
    elif 30 < original_victory_points_of_province <= 40:
        changed_victory_point = (original_victory_points_of_province - 30) * 2 + 90
    elif 40 < original_victory_points_of_province:
        changed_victory_point = (original_victory_points_of_province - 40) * 1 + 110
    changed_victory_point = int(round(float(changed_victory_point)/5) * 5)

    return changed_victory_point
