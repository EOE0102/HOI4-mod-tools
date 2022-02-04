# Modding tools for game Heart of Iron 4 in python

Youtube Channel for Modder [The Iron Workshop](https://www.youtube.com/channel/UCYGO3GSISuiwAl4XchNvlTg)

## STEP 1: Create a new map

use this mod as basic: https://steamcommunity.com/sharedfiles/filedetails/?id=804347118

### **Fix provinces.bmp**

using paint.net, save as 24 bit BMP

| Common Errors | Fix |
| :- | :- |
| `Province 8944 has TOO LARGE BOX. Perhaps pixels are spread around the world in provinces.bmp` | No harm |
| `Map invalid X crossing. Please fix pixels at coords: [X],[Y]` | **fix_pixel_crossing.py**  |
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

### **modify impassable area and more**

impassable = yes in history/state file

adjacencies.csv

adjacency_rules.txt

## **STEP 3: More Province**


