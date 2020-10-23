# Modding tools for game Heart of Iron 4 in python

# 1. Preparation
## 1.1 Basic python coding knowledge
* Basic Python knowledge. (how to run file, python PIP)
* I'm using Visual Studio Code (A python writing/debugging tool, or anything you need to run python) 

## 1.2 recommend tools
* Everything (A universal file search tool on windows, sometimes i forget where the creted files are saved)
* Listary  (free version is enough)
* Photoshop or windows paint(modify map file) 

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

and finally don't forget create a empty folder under the PATH.
</p>
Now you have .mod file and a empty folder for modding. You can choose your mod from HOI4 start panel, but nothing changed, since your mod file is empty. 

## 1.5 initial the test mod

**Subscribe [Standard World Map Mod
](https://steamcommunity.com/sharedfiles/filedetails/?id=804347118).** </p>
We are using this mod as our basic map mod. All of the modifications of map are based on the wunderbar mod. 

copy content under 

* [where your steam installed]/steamapps/workshop/content/394360/804347118

into your created mod folder. 

Run you game with your mod again, and you can find the changes.

# 2. Debug MAP and relative files.

if you have set the debug mode, run HOI4 with only your test mod, choose any country you want to test, then that beaver in lower right shows the error penal. 

This log file is also saved under 
* X:/[YOUR NAME]/Documents/Paradox Interative/Hearts of Iron IV/logs/error.log. 

Remember this, you will check it frequently. 
</p>
Let's look into this log file. <br>
one of typical error infos is: 

>[12:00:56][pdxmapborders.cpp:189]: One-pixel province color found at 1757, 2289.

One-pixel province, usually they are not harmful, but annoying. The original modder generates the map from GIS system, we will debug this.


## 2.1 debug One-pixel province problem.
One-pixel province, that mean there is a pixel surrounding by 8(or 5) other pixels, which have different colors. I don't want to check every situation, but choose to remove this one pixel, and paint it with random nearby color.

- TOOLS: remove_one_pixel_province.py
- Import: provinces.bmp 
- Export: pixel_grid.bmp

do it 2 or 3 times and remove all One-pixel provinces. Or you can DIY(photoshop), since there are a few left after 3 tries. 

## 2.2 debug Map invalid X crossing
you might noticed there is a new type of error pop up after debugging. 
>[13:45:49][map.cpp:1747]: Map invalid X crossing. Please fix pixels at coords: 1660,2093

the upper left pixel will be painted the same color which upper right has.

- **Tools**: DIY or run **fix_pixel_crossing.py**
- **Import**: provinces.bmp error.log
- **Export**: save your bmp file.

## 2.3 TOO LARGE BOX
ignore it, no harm.

## 2.4 map building location is not over the land and so on.
HOI4 has provided a great debug tools. Enable debug mod and you can see the **"NUDGE!"** there.<br>
This error sentence is about the building. Because we remove some pixels of a province, some buildings and 3D units are no more located in the right place, i.e over other province. It can cause CTD if we don't fix it. 

And there is a hidden CTD, called "province is a coastal province, but not marked as 'coastal' in definition.csv file, so the ship can not dock there"

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


# 3.





















