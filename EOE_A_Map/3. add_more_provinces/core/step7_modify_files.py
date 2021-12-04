
from core import read_write_files
import tkinter
from tkinter import filedialog
import os
import re

def modify_files():
    print('Part 7')

    all_painting_area_dict_small = read_write_files.read_dict('all_painting_area_dict_small')
    all_painting_area_dict = read_write_files.read_dict('all_painting_area_dict')

    exportFolderLocation = filedialog.askdirectory(title = "Select Export Folder Location")
    if not os.path.exists(exportFolderLocation + "/export/states"):
        os.makedirs(exportFolderLocation + "/export/states")
    if not os.path.exists(exportFolderLocation + "/export/strategicregions"):
        os.makedirs(exportFolderLocation + "/export/strategicregions")


    newProvincesListFull = write_definition_csv_file(exportFolderLocation, all_painting_area_dict_small, all_painting_area_dict)
    write_state_files(exportFolderLocation, newProvincesListFull, all_painting_area_dict_small)
    write_strategicregions_files(exportFolderLocation, newProvincesListFull, all_painting_area_dict_small)

    print('Part 7 finished')


def write_definition_csv_file(exportFolderLocation, all_painting_area_dict_small, all_painting_area_dict):
    title = "Open definition file(definition.csv)"
    filetypes = {("Map definition file", ".csv")}
    all_text_str = read_write_files.open_file_return_str(title, filetypes)
    all_text_list = read_write_files.split_str_into_list(all_text_str, ';')
    definition_color_address = read_write_files.split_info_definition_csv(all_text_list)

    allRGBInLst = definition_color_address['RGB']
    allLandSeaLakeTypeInLst = definition_color_address['land_sea_lake']
    allIsCoastTypeInLst = definition_color_address['coast']
    allTerrainTypeInLst = definition_color_address['terrain']
    allContinentTypeInLst = definition_color_address['continent']
    newProvincesListFull = []
    
    for i in range(len(all_painting_area_dict_small)):
        defaultOriginalColor = all_painting_area_dict_small[i][0]
        originalIndex = allRGBInLst.index(defaultOriginalColor)
        
        newProvincesListFull.append([0,[]])
        newProvincesListFull[i][0] = originalIndex
        newProvincesListPart = []

        for j in range(1, len(all_painting_area_dict_small[i])):
            writeIndex = len(all_text_str)
            writeRGB = str(all_painting_area_dict_small[i][j][0]) + ';' + str(all_painting_area_dict_small[i][j][1]) + ';' + str(all_painting_area_dict_small[i][j][2])
            writeLandSeaLakeType = allLandSeaLakeTypeInLst[originalIndex]
            writeCoastType = is_this_province_coast(all_painting_area_dict_small[i][j], allIsCoastTypeInLst[originalIndex], allRGBInLst, allLandSeaLakeTypeInLst)
            
            writeTerrain = allTerrainTypeInLst[originalIndex]
            writeContinent = allContinentTypeInLst[originalIndex]
            writeLine = str(writeIndex) + ";" + writeRGB + ';' + str(writeLandSeaLakeType) + ';' + str(writeCoastType) + ';' + str(writeTerrain) + ';' + str(writeContinent) + '\n'
            all_text_str.append(writeLine)
            newProvincesListPart.append(writeIndex)

        newProvincesListFull[i][1] = newProvincesListPart


    save_file = filedialog.asksaveasfilename(title = "save definition.csv")
    f = open(save_file,'w')
    for element in all_text_str:
        f.write(element)
    f.close()

    return newProvincesListFull

def write_state_files(exportFolderLocation, newProvincesListFull, all_painting_area_dict_small):
    root = tkinter.Tk()
    stateFolderLocation = filedialog.askdirectory(title = "Select State Folder Location")
    stateFileList = []
    for file in os.listdir(stateFolderLocation):
        if file.endswith(".txt"):
            stateFileList.append(file)

    for bbk in range(len(stateFileList)):
        originalStateFileName = stateFileList[bbk]
        print('exporting states file: '+ str(bbk) + ' / ' + str(len(stateFileList)))

        #read original file
        temp = stateFolderLocation + "/" + originalStateFileName
        stateFileLocationIndex = open(temp)
        allTextInList = stateFileLocationIndex.readlines()
        stateFileLocationIndex.close()
        allTextInSrtNoComment = remove_Comment(allTextInList)

        #get province index
        original_provinces_ID = find_inhalt_in_bracket_fcn(allTextInSrtNoComment, "provinces", "{", "}")
        original_provinces_ID = original_provinces_ID[0].replace("\n","")
        original_provinces_ID = original_provinces_ID.replace("\t","")  

        original_provinces_ID_firstID = original_provinces_ID.split(' ')[1]
        originalProvinceID = int(original_provinces_ID_firstID)
        
        for i in range(len(all_painting_area_dict_small)):
            newFileString = allTextInSrtNoComment
            if newProvincesListFull[i][0] == originalProvinceID:
                addNewProvinceString = ''
                for j in range(len(newProvincesListFull[i][1])):
                    addNewProvinceString = addNewProvinceString + ' ' + str(newProvincesListFull[i][1][j])
                find_text_position1 = [m.start() for m in re.finditer("provinces", allTextInSrtNoComment)]

                provincedIDStartPosition = find_text_position1[0]
                shortText = allTextInSrtNoComment[int(provincedIDStartPosition):]
                find_text_position2 = [m.start() for m in re.finditer(str(originalProvinceID), shortText)]
                nearstPosition = int(find_text_position2[0]) + len(str(originalProvinceID))
                newFileString = allTextInSrtNoComment[:(provincedIDStartPosition + nearstPosition)] + addNewProvinceString + allTextInSrtNoComment[(provincedIDStartPosition + nearstPosition):]

                text_file = open(exportFolderLocation + "/export/states/" + originalStateFileName, "w")
                text_file.write(newFileString)
                text_file.close()


def write_strategicregions_files(exportFolderLocation, newProvincesListFull, all_painting_area_dict_small):
    root = tkinter.Tk()
    strategicregionsFolderLocation = filedialog.askdirectory(title = "Select strategicregions Folder Location")
    strategicregionsFileList = []
    for file in os.listdir(strategicregionsFolderLocation):
        if file.endswith(".txt"):
            strategicregionsFileList.append(file)

    for bbk in range(len(strategicregionsFileList)):
        originalStateFileName = strategicregionsFileList[bbk]
        print('exporting strategicregions file: '+ str(bbk) + ' / ' + str(len(strategicregionsFileList)))

        #debug
        if str(bbk) == '123':
            a = 1

        #read original file
        temp = strategicregionsFolderLocation + "/" + originalStateFileName
        strategicregionsFileLocationIndex = open(temp)
        allTextInList = strategicregionsFileLocationIndex.readlines()
        strategicregionsFileLocationIndex.close()
        allTextInSrtNoComment = remove_Comment(allTextInList)

        #get provinces index
        original_provinces_ID = find_inhalt_in_bracket_fcn(allTextInSrtNoComment, "provinces", "{", "}")
        provinces_IDs_list = original_provinces_ID.copy()
        provinces_IDs_list = provinces_IDs_list[0].split()
        for i in range(len(provinces_IDs_list)):
            if i == 0:
                province_ID_position = allTextInSrtNoComment.find('\t' + provinces_IDs_list[i] + ' ')
            else:
                province_ID_position = allTextInSrtNoComment.find(' ' + provinces_IDs_list[i] + ' ')
            for j in range(len(newProvincesListFull)):
                if str(newProvincesListFull[j][0]) == provinces_IDs_list[i]:
                    text_begin = allTextInSrtNoComment[0:(province_ID_position + len(provinces_IDs_list[i]) + 1)]
                    text_end = allTextInSrtNoComment[(province_ID_position + len(provinces_IDs_list[i]) + 1):len(allTextInSrtNoComment)]
                    text_middle = ''
                    for k in range(len(newProvincesListFull[j][1])):
                        text_middle = text_middle + ' ' + str(newProvincesListFull[j][1][k])
                    allTextInSrtNoComment = text_begin + text_middle + text_end



        text_file = open(exportFolderLocation + "/export/strategicregions/" + originalStateFileName, "w")
        text_file.write(allTextInSrtNoComment)
        text_file.close()


def remove_Comment(textInList):
    # remove comment
    for i in range(len(textInList)):
        if "#" in textInList[i]:
            textInList[i] = textInList[i].split("#",1)[0]
            textInList[i] = textInList[i] + "\n"
    all_text_in_str_initialized = "".join(textInList)
    return all_text_in_str_initialized

def is_this_province_coast(painging_area_RGB, painging_area_coast_type, allRGBInLst, allIsCoastTypeInLst):
    if painging_area_coast_type == 'false':
        return 'false'
    else:
        return 'true'

    #return writeCoastType

def find_inhalt_in_bracket_fcn(all_text_in_str, find_str, start_mark, end_mark):
    #all_text_in_str_initialized = all_text_in_str.replace("\t","")
    #all_text_in_str_initialized = all_text_in_str_initialized.replace("\n","") 
    find_text_position = [m.start() for m in re.finditer(find_str,all_text_in_str)]
    open_bracket_position = [m.start() for m in re.finditer(start_mark,all_text_in_str)]
    close_bracket_position = [m.start() for m in re.finditer(end_mark,all_text_in_str)]
    find_text_info = []
    #for i in range(len(find_text_position)):
    #    for j in reversed(open_bracket_position):
    ##        if j > find_text_position[i]:
    #           temp1 = j
    #           for k in reversed(close_bracket_position):
    #               if k > temp1:
    #                   temp2 = k
    #   find_text_info.append(all_text_in_str[temp1+1:temp2])


    for i in range(len(find_text_position)):
        j = 0
        while find_text_position[i] > open_bracket_position[j]:
            j = j + 1
        temp1 = open_bracket_position[j]
        k = 0
        while temp1 > close_bracket_position[k]:
            k = k + 1
        temp2 = close_bracket_position[k]
        find_text_info.append(all_text_in_str[temp1+1:temp2])
    return find_text_info