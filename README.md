# Modding tools for game Heart of Iron 4 in python

Youtube Channel for Modder [The Iron Workshop](https://www.youtube.com/channel/UCYGO3GSISuiwAl4XchNvlTg)

## STEP 1: Create a new map

use this mod as basic: https://steamcommunity.com/sharedfiles/filedetails/?id=804347118

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

### **Fix supply line (TODO)**

launch the game, some railway are not well connected, modify railways.txt or province.bmp, you choose one.
>Task: how to generate the map from GIS without changing the topology of provinces?

temp fix: use this mod, it modifies the railway.txt manually
: https://steamcommunity.com/sharedfiles/filedetails/?id=2718546428 

>Solution: redraw the province.bmp

## **STEP 2: Every province a state**

### **Modify /State files**

run: 3_Every_Province_a_State/main1_create_states.py

GOOD CODING

### **RUN Debug Tool**

>"Validate all State" DON'T WORK.

> Nudge => Buildings => Find Error(F) => Validate In State(V), if error, open building.txt add code manually => leave Nudge, enter Nedge to refresh map.

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
| `add_core_of = GER`, reported by user | Germany.txt error |
| Trying to set invalid state building "dockyard" to state #59. | manually |
| `Spain Civil war, too many unit created` | DELETE create_unit event `Anarchist Militia` |

### **Modify impassable area and more**

impassable = yes in history/state file

adjacencies.csv

adjacency_rules.txt

Caspian Sea/ volkhov


### **Add name for all new states**

https://steamcommunity.com/sharedfiles/filedetails/?id=2352204526

| Common Errors | Fix |
| :- | :- |
| `nothing changed` | change line code is \n  |
| `nothing changed` | Encode in UTF8-BOM  |
| `The game has loc key collisions. Check logs/text.log for more details` | Check logs/text.log  |

>4_More_Provinces/main.py => STEP3 

## **STEP 3: More Province**

>EOE_A_Other_Map_Modification/main.py

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
| `STEP8` | Supply note |
| Modify states | add bunkers for Maginot line |


STEP1 to STEP 8 

