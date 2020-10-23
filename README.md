# Modding tools for game Heart of Iron 4 in python




# 1. Preparation
## 1.1 Basic python coding knowledge
* Basic Python knowledge. (how to run file, python PIP)
* I'm using Visual Studio Code (A python writing/debugging tool, or anything you need to run python) 

## 1.2 recommend tools
* Everything (A universal file search tool on windows, sometimes i forget where the created files are saved)
* Listary  (free version is enough)
* Photoshop or windows paint(modify map file) 
* Notepad++
* FileLocator Pro

## 1.3 enable debug mode
* first of first, set HOI4 add laucher option -debug, if you don't know, google it.

## 1.4 Create your mod file.
* create your mod file under X:/[YOUR NAME]/Documents/Paradox Interative/Hearts of Iron IV/mod by using HOI4 own mod tools(start panel => Mods => MOD TOOLS => Create a mod)
* or do it yourself (see below)

create a .mod file under X:/[YOUR NAME]/Documents/Paradox Interative/Hearts of Iron IV/mod


>name="test01" <br>
version="1.3" <br>
tags={ <br>
	"Map" <br>
	"Utilities" <br>
}<br>
picture="title.png"<br>
supported_version="1.9.*"<br>
path="E:/Users/EOE/Documents/Paradox Interactive/Hearts of Iron IV/Mymod/test01"<br>
remote_file_id="1818951012"<br>

>**name**: the display name on HOI4 start panel<br>
**version**: you mod version, choose the number you like<br>
**tags**: the tags displayed on steam mod site, you can check other mod and choose the proper ones.<br>
**picture**: thumbnail, don's matter if empty.<br>
**path**: the mod folder you or mod tools create. here is a trick, you can place the mod folder under other path just like I do.<br>
**remote_file_id**: the mod id shown after steam url(https://steamcommunity.com/sharedfiles/filedetails/?id=1818951012 ). If you have upload a mod, you will get one.<br>

and finally don't forget to create a empty folder under the PATH.
</p>
Now you have .mod file and a empty folder for modding. You can choose your mod from HOI4 start panel, but nothing changed, since your mod file is empty. 

## 1.5 initial the test mod

**Subscribe [Standard World Map Mod
](https://steamcommunity.com/sharedfiles/filedetails/?id=804347118).** </p>
We are using this mod as our basic map mod. All of the modifications of map are based on the wunderbar mod. 

copy content under 

* [where your steam installed]/steamapps/workshop/content/394360/804347118

into your created mod folder. 

Run you game with your mod again, and you can see the changes.

# 2. Debug MAP(provinces.bmp) and relative files.

if you have set the debug mode, run HOI4 only with your test mod, choose any country you want to play, then that beaver in lower right shows the error penal. 

This log file is also saved under 
* X:/[YOUR NAME]/Documents/Paradox Interative/Hearts of Iron IV/logs/error.log. 

Remember this, you will check it frequently. 


## 2.1 debug One-pixel province problem.
</p>
Let's look into this log file. <br>
one of typical error infos is like: 

>[12:00:56][pdxmapborders.cpp:189]: One-pixel province color found at 1757, 2289.

One-pixel province, usually they are not harmful, but annoying. The original modder generates the map from GIS system, we will debug this.

One-pixel province, that mean there is a pixel surrounding by 8(or 5) other pixels, which have different colors. I don't want to check every situation, but choose to remove this one pixel, and paint it with random nearby color.

- TOOLS: remove_one_pixel_province.py
- Import: provinces.bmp 
- Export: pixel_grid.bmp

do it 2 or 3 times and remove all One-pixel provinces. Or you can DIY(photoshop), since there are a few left after 3 tries. 

## 2.2 debug Map invalid X crossing
you might noticed there is a new type of error pop up after debugging. 
>[13:45:49][map.cpp:1747]: Map invalid X crossing. Please fix pixels at coords: 1660,2093

the upper left pixel will be painted the same color which upper right has.

- **Tools**: DIY or **fix_pixel_crossing.py**
- **Import**: provinces.bmp error.log
- **Export**: save your bmp file.

## 2.3 TOO LARGE BOX
ignore it, no harm.

## 2.4 map building location is not over the land and so on.
HOI4 has provided a great debug tools. Enable debug mod and you can see the **"NUDGE!"** there.<br>
This error sentence is about the building. Because we remove some pixels of a province, some buildings and 3D units are no more located in the right place, i.e over other province. It can cause CTD if we don't fix it. 

And there is a hidden CTD, called "province is a coastal, but not marked as 'coastal' in the definition.csv file, so ships can not dock there. opps, CTD!"

This tool modifies the important definition files under /map folder
>airports.txt<br>
>ambient_object.txt<br>
>buildings.txt<br>
>definition.csv<br>
>unitstacks.txt<br>
>weatherpositions.txt (no need for modify)


in short:

* Database => Coastal => Generate => save
* building => Random All States => (wait) => save
* Units => Auto in All => save

new files are saved under path 
* [YOUR NAME]Documents\Paradox Interactive\Hearts of Iron IV\map

## 2.5 prov X stack Y Ship in port moving is too far away from center
TODO, not too serious


# 3. Create new states (one province, one state)
this time, we will do something big, creating new states for every province. \
Those changes will impact many files, but I will teach you step by step.

## 3.1 Create new definition files (/history/state and /map/supplyareas)
- **Tools**: create_state_for_every_province.py

1. Select State Folder Location 
>[YOUR MOD]\history\states (if you have)\
>OR\
>[Where Steam installed]\steamapps\common\Hearts of Iron IV\history\states

2. Select Supply Folder Location
>[YOUR MOD]\map\supplyareas (if you have)\
>OR\
>[Where Steam installed]\steamapps\common\Hearts of Iron IV\map\supplyareas

3. Select State Definition file(definition.csv)
>**[YOUR MOD]**\map\definition.csv
4. Select Export Folder Location
>Whatever, better on SSD, because of 10K+ small files.
5. Waiting for export, you can locate to your export folder

6. Export files are:
>**states folder**, with 10K+ definition files
>**supplyareas**, with 300+ supply area definition files.
>**new_state_reminder.txt**, recording the new state IDs

7. cut and paste those to where they should be in your mod folder.

## 3.2 Create new event files 
we know that some events like annex or add_core are relative to map file.
Hopefully I have covered all the events.

- **Tools**: debug_states_in_events.py

1. Select Event(or any relative files) Location
ATTENTION, you should check every folder under HOI4 install folder, because you don't know which file modifies the map information. 
- here are some Folder you should choose: 
>\common\decisions\
>\common\national_focus\
>\common\on_actions\
>\common\operations\ (because of new DLC)
>\events

2. Select Export Folder Location
>better on a SSD

3. Select new_state_reminder_ file(new_state_reminder_.txt)
>new_state_reminder_.txt

4. usually game crash during first testing, but don't worry, check error.log first.
>... Error: "Unexpected token: ﻬ near line: 9" in file: "common/national_focus/germany.txt" near line: 9
open the file with Notepad++, (View=> Show Symbol => Show All Characters), and you can see the first character is not **NULL**. Delete it.
>do the same with \event folder

# 4. test and fix
**Check error.log.** \
Do Capital 2.4 again, because we have just create plenty of states, all of them need 3D Models and so on.\
**Game now is playable, play as Liberia and do some small fix** 

## 4.1 fix Trying to set invalid state building "dockyard" 
if you forget which file should be modified, look up new_state_reminder_.txt 

And do Capital 4.2 again.

## 4.2 fix has_dlc for new DLC
some code like ... has_dlc ... are not added to the new state file, DIY please, not too many of them.
Search has_dlc by using FileLocator.
if you forget which file should be modified, look up new_state_reminder_.txt 
>if = {\
			limit = { has_dlc = "Battle for the Bosporus"}\
			set_demilitarized_zone = yes\
		}\
		1936.11.9 = {\
			set_demilitarized_zone = no\
		}

# 5. More provinces (option and hard) TODO debugging...
run add_more_provinces.py follow the step...\
you need a good place(SSD) to save temperate files\
be patient...

1. STEP1: Generate all available RGB, and write into a file

2. STEP2: get the painting area for every color in map

3. STEP2.5: get states info 
>emmmmm, debugging...




