import math
from tkinter import filedialog
from PIL import Image #pip install Pillow
from core import read_files
## PART 2 ##


def step_get_RGB_area_for_every_color():
    #read image
    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (provinces.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_width, image_height = im.size

    ##get all RGB Area
    all_RGB_and_Area_list = []
    used_RGB_list = []
    #all_RGB_and_Area_list.append([(0,0,0),[(0,0),(0,0),(0,0),0]]) #[RGB, [_startPoint, PointOfGravity, NearestPointOfGravity, Count]]
    for count_image_height in range(image_height):
        print("Part2: get PaintArea for every color | line = " + str(count_image_height) +' / '+str(image_height))
        for count_image_width in range(image_width):
            #print("Modifying Part1: x = " + str(count_image_width) + ' / ' + str(image_width) + ', y = ' + str(count_image_height) +' / '+str(image_height))

            pixel_old_RGB = pixels[count_image_width, count_image_height]

            if pixel_old_RGB != (0,0,0):
                rgb_area_info_list = []
                if pixel_old_RGB in used_RGB_list:
                    
                    _startPoint = (count_image_width, count_image_height)
                    rgb_area_p = []
                    rgb_area_p, pixels = floodfill(pixels, pixel_old_RGB, (0,0,0), image_width, image_height, count_image_width, count_image_height)

                    rgb_area_POG = calculate_point_of_gravity(rgb_area_p)
                    rgb_area_nearest_POG = get_nearest_POG(rgb_area_POG, rgb_area_p)
                    rgb_area_info_list.append(_startPoint)
                    rgb_area_info_list.append(rgb_area_POG)
                    rgb_area_info_list.append(rgb_area_nearest_POG)
                    rgb_area_info_list.append(len(rgb_area_p))
                    rgb_area_info_list.append(rgb_area_p)

                    tempIndex = used_RGB_list.index(pixel_old_RGB)
                    all_RGB_and_Area_list[tempIndex].append(rgb_area_info_list)
                    
                else:
                    #first time of meeting this color
                    _startPoint = (count_image_width, count_image_height)
                    rgb_area_p = []
                    rgb_area_p, pixels = floodfill(pixels, pixel_old_RGB, (0,0,0), image_width, image_height, count_image_width, count_image_height)
                    rgb_area_POG = calculate_point_of_gravity(rgb_area_p)
                    rgb_area_nearest_POG = get_nearest_POG(rgb_area_POG, rgb_area_p)
                    rgb_area_info_list.append(_startPoint)
                    rgb_area_info_list.append(rgb_area_POG)
                    rgb_area_info_list.append(rgb_area_nearest_POG)
                    rgb_area_info_list.append(len(rgb_area_p))
                    rgb_area_info_list.append(rgb_area_p)
                    
                    tempRGB = []
                    tempRGB.append(pixel_old_RGB)
                    temp = []
                    temp.append(rgb_area_info_list)
                    all_RGB_and_Area_list.append(temp)
                    used_RGB_list.append(pixel_old_RGB)
    all_RGB_and_Area_dict = {
        'RGB':used_RGB_list,
        'Seeds Info':all_RGB_and_Area_list
    }

    read_files.save_dict(all_RGB_and_Area_dict, 'all_RGB_and_Area_dict')

    print('Part 2 finished')



def floodfill(pixels, oldColor, newColor, xMax, yMax, defaultX, defaultY):
    # assume surface is a 2D image and surface[x][y] is the color at x, y.
    #(pixels, pixel_RGB, image_width, image_height, count_image_width, count_image_height, (0,0,0))
    x = defaultX
    y = defaultY
    theStack = [ (x, y) ]
    theArea = []
    while len(theStack) > 0:
        x, y = theStack.pop()
        if (x < 0) or (x >= xMax) or (y < 0) or (y >= yMax):
        #if x >= xMax or y >= yMax:
            arront = (0,0,0)
        else:
            arront = list(pixels[x,y])
        if arront == list(oldColor):
            pixels[x,y] = newColor
            theArea.append([x,y])
            theStack.append( (x + 1, y) )  # right
            theStack.append( (x - 1, y) )  # left
            theStack.append( (x, y + 1) )  # down
            theStack.append( (x, y - 1) )  # up
    return theArea, pixels

def calculate_point_of_gravity(RGBAreaPointOfGravityList):
    avgX = 0
    avgY = 0
    for item in range(len(RGBAreaPointOfGravityList)):
        avgX = RGBAreaPointOfGravityList[item][0] + 0.5 + avgX
        avgY = RGBAreaPointOfGravityList[item][1] + 0.5 + avgY
    avgX = avgX/len(RGBAreaPointOfGravityList) - 0.001 #0.5 >> 0
    avgY = avgY/len(RGBAreaPointOfGravityList) - 0.001 #2.5 >> 2
    return [avgX, avgY]

def get_nearest_POG(rgb_area_POG, rgb_area_p):
    distanceList = []
    for item in rgb_area_p:
        p2pDistance = calculate_P2P_distance(rgb_area_POG, get_real_POG(item))
        distanceList.append(p2pDistance)
    minPos = distanceList.index(min(distanceList))
    rgb_area_nearest_POG = rgb_area_p[minPos]
    return rgb_area_nearest_POG



def calculate_P2P_distance(Point1, Point2):
    #Point1 = get_real_POG(Point1)
    
    #x1 = Point1[0]
    #x2 = Point2[0]
    #y1 = Point1[1]
    #y2 = Point2[1]
    distance = math.pow((Point1[0]-Point2[0]),2) + math.pow((Point1[1]-Point2[1]),2)
    if distance == 0:
        return 0
    else:
        distance = math.pow(distance,0.5)
    return distance

def calculate_P2P_energy(Point1, Point2):
    #x1 = Point1[0]
    #x2 = Point2[0]
    #y1 = Point1[1]
    #y2 = Point2[1]

    distance = math.pow((Point1[0]-Point2[0]),2) + math.pow((Point1[1]-Point2[1]),2)

    if distance == 0:
        return 10000000000 #float('inf') + float('inf') = inf
    else:
        energy = 1 / distance
        return energy
    
def get_real_POG(Point):
    x = Point[0] + 0.5
    y = Point[1] + 0.5
    return [x,y]


