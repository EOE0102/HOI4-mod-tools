# Modding tools for game Heart of Iron 4 in python

Youtube Channel for Modder [The Iron Workshop](https://www.youtube.com/channel/UCYGO3GSISuiwAl4XchNvlTg)

## STEP 1: Create a new map

use this mod as basic: <https://steamcommunity.com/sharedfiles/filedetails/?id=804347118>

### **Fix provinces.bmp**

using paint.net, save as 24 bit BMP

| Common Errors | Fix |
| :- | :- |
| `Province 8944 has TOO LARGE BOX. Perhaps pixels are spread around the world in provinces.bmp` | No harm |
| `Map invalid X crossing. Please fix pixels at coords: [X],[Y]` | **fix_pixel_crossing.py** |
| `Bitmap and province definition disagree on whether or not province [X] is coastal. Bitmap adjacency result will be prefered` | NEDGE! -> Database => Coastal **first click show color, otherwise nedge will CTD, no idea why** |
| `Error in map/adjacencies.csv: Adj between 1399 and 1515 is not adjacent with THROUGH = 220` | No harm, manual |
| `One-pixel province color found at [X],[Y]` | No harm yet **remove_one_pixel_province.py** |
| `port building has invalid sea zone for province 12920` | No harm yet |
| `prov 7855 stack 19 Ship in port is too far away from center (dist 160 55 prov -1)` | TODO |
| `Province 5918 has no pixels in provinces` | might happened after editing, manual |
| `map/buildings.txt port building has invalid sea zone for province 11070` | Cause NEDGE CTD: might happened after editing, manual:140;naval_base;2997.00;9.60;1966.00;-1.17;2455 end with Province ID 2455 not 0, Found this bug on Sri Lanka|

### **Fix heightmap.bmp**

im_heightmap2.convert('L')

### **world_normal.bmp**

Normal maps can be created with Nvidia's texture tools from the heightmap.bmp, or by using Filter > 3D > Generate Normal Map in Photoshop CC. If you are using GIMP, download the Normal Map Plugin. Load the heightmap, change the image type to RGB and add the bump map filter by using Filter > Map > Normal. Remember to inverse the Y axis.

### **Fix supply line (TODO)**

launch the game, some railway are not well connected, modify railways.txt or province.bmp, you choose one.
>Task: how to generate the map from GIS without changing the topology of provinces?

temp fix: use this mod, it modifies the railway.txt manually
: <https://steamcommunity.com/sharedfiles/filedetails/?id=2718546428>

>Solution: redraw the province.bmp

## **STEP 2: More map features**

### **Create sailable caspian sea**

## **STEP 3: Every province a state**

### **Modify /State files**

run: 3_Every_Province_a_State/main1_create_states.py

GOOD CODING

### **RUN Debug Tool**

>"Validate all State" DON'T WORK.(8h+ not responding)

> Nudge => Buildings => Find Error(F) => Validate In State(V), if error, open building.txt add code manually (F**K debug 500+) => leave Nudge, enter Nedge to refresh map.
> 6430;(the most south state of )

THEN

>"Random All States".

| Common Errors | Fix |
| :- | :- |
| `Adj between 1135 and 13090 is not adjacent with THROUGH = 6471` | :- |
| `State Error: Trying to set invalid state building "dockyard" to state #7.` | :- |
| `set override garrison strength for state with invalid Data = 353` | :- |
| `set override garrison strength for state with invalid Data = 350` | :- |
| `prov 8944 stack 9 Attacking is too far away from center (dist 144 0 prov -1)` | :- |
| `Trying to move navy to land province with no port: 6332 (Ostseeflotte)` | :- |
| `6 -  Vlaanderen has too many buildings : -2` | :- |

### **Modify /events /common files**

run: 3_Every_Province_a_State/main2_debug_relative_events.py

| Common Errors | Fix |
| :- | :- |
| `CTD when loading events` | windows UTF-8 error. open nation_focus files with notepad++, delete the first letter 锘 |
| `4 = { if = { limit ={...} add_core_of = GER}}`, reported by user | event\Germany.txt error |
| Trying to set invalid state building "dockyard" to state #59. | manually |
| `Spain Civil war, too many unit created` | DELETE create_unit event `Anarchist Militia` , every_owned_state |

### **Modify impassable area and more**

impassable = yes in history/state file

adjacencies.csv

adjacency_rules.txt

Caspian Sea/ volkhov

### **Add name for all new states**

<https://steamcommunity.com/sharedfiles/filedetails/?id=2352204526>

| Common Errors | Fix |
| :- | :- |
| `nothing changed` | change line code is \n  |
| `nothing changed` | Encode in UTF8-BOM  |
| `The game has loc key collisions. Check logs/text.log for more details` | Check logs/text.log  |

>4_More_Provinces/main.py => STEP3

## **STEP 4: More Province**

>EOE_A_Other_Map_Modification/main.py

STEP1 to STEP 8

| Common Errors | Fix |
| :- | :- |
| `STEP1: create available RGB` | max color 255*255*255 - 10K vanilla color |
| `STEP2: get painting area` | NO |
| `STEP3: get states info` | read definition.txt |
| `STEP4: get painting seeds` | you can modify core/parameter.py |
| `STEP5: get painting area for every seeds` | core: floodfill |
| `STEP6: painting` | NO |
| `STEP7: modify states and strategicregions files` | strategicregions file is in vanilla game folder |
| `Province 17640 has only 7 pixels around (x=3312,y=868). Should have at least 8` | MANUALLY |
| `Map invalid X crossing. Please fix pixels at coords` | **fix_pixel_crossing.py** |
| `One-pixel province color found` | **remove_one_pixel_province.py** |
| `adjacencies.csv`| adjacencies.csv |
| `VP` | add new VP in 1-France.txt |
| `STEP8: create supply note` | 8-1 takes 90min, 8-2 takes 90min |
| `Railway level > NDefines::NSupply::MAX_RAILWAY_LEVEL (province 9371, neighbor index 5, level 6)` | fix all TODO create by 8-2 |
| Modify states | add bunkers for Maginot line |

## **STEP 5: More Features**

### **Increase Supply Range**

The supply range is +60%.

### **Add Resistance type**

Because the strength of Resistance is based on amount of states. Therefore we need a new type army to reduce the the cose fo manpower.

### **More Resource**

| Common Errors | Fix |
| :- | :- |
| `Duplicate decision. develop_524_oil_deposits is a duplicate.` | BETA |

### **State Buildings Slot limiter**

BETA

### **More releasable countries**

BETA
| Common Errors | Fix |
| :- | :- |
| `FLAG` | 32bit ,no compress |
