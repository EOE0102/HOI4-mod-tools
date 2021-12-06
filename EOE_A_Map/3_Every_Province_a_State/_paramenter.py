## parameter inistialation
#weight
manpower_weight = [["unknown",0.00000001],["ocean",0.00000001],["lakes",0.00000001],
                    ["forest",40],["hills",40],["mountain",20],
                    ["plains",60],["urban",100],["jungle",20],
                    ["marsh",10],["desert",1],
                    ["water_fjords",0.00000001],["water_shallow_sea",0.00000001],["water_deep_ocean",0.00000001],
                    ["ice_sheet",0.00000001]]
manpower_victory_points_weight = 0.20
manpower_provinces_buildings_weight = 1
manpower_coast_weight = 1.5

state_category_weight = [["unknown",-10],["ocean",-10],["lakes",-10],
                    ["forest",-1],["hills",-1],["mountain",-2],
                    ["plains",0],["urban",0],["jungle",-2],
                    ["marsh",-3],["desert",-3],
                    ["water_fjords",-10],["water_shallow_sea",-10],["water_deep_ocean",-10],
                    ["ice_sheet",-10]]
state_category_type_lst  = ["rural","town","large_town","city","large_city","metropolis","megalopolis"]
state_category_type_nochange_lst = ["enclave","small_island","tiny_island","wasteland","pastoral"]
state_category_victory_points_weight = 5
state_category_provinces_buildings_weight = 1

state_infrastructure_weight = [["unknown",-10],["ocean",-10],["lakes",-10],
                    ["forest",-1],["hills",-1],["mountain",-2],
                    ["plains",0],["urban",0],["jungle",-2],
                    ["marsh",-3],["desert",-3],
                    ["water_fjords",-10],["water_shallow_sea",-10],["water_deep_ocean",-10],
                    ["ice_sheet",-10]]
infrastructure_victory_points_weight = 5
infrastructure_provinces_buildings_weight = 1


state_local_supplies_weight = [["unknown",0],["ocean",0],["lakes",0],
                    ["forest",10],["hills",10],["mountain",5],
                    ["plains",20],["urban",100],["jungle",10],
                    ["marsh",0],["desert",0],
                    ["water_fjords",-100],["water_shallow_sea",-100],["water_deep_ocean",-100],
                    ["ice_sheet",-100]]
local_supplies_victory_points_weight = 5
local_supplies_buildings_weight = 20


max_victory_point_weight = 10 # goto change_victory_points
