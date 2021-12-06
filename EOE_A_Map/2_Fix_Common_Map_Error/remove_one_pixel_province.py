from PIL import Image
import tkinter as Tkinter
from tkinter import filedialog
import random


def main():
    root = Tkinter.Tk()
    root.filename = filedialog.askopenfilename(title = "Choose Province Map File (province.bmp)", filetypes={("HOI Map file", ".bmp"),("All files", "*.*")})
    file_path = root.filename
    im = Image.open(file_path)
    pixels = im.load()
    image_width, image_height = im.size
    intOnePixelProvince = 0
    for pixel_coordinate_height in range(0, image_height-1): 
        for pixel_coordinate_width in range(0, image_width-1):
            bolOnePixel = checkSurrendingPixel(pixels, image_height, image_width,pixel_coordinate_width, pixel_coordinate_height)
            if bolOnePixel == True:
                intOnePixelProvince = intOnePixelProvince + 1
                if pixel_coordinate_height == 0:
                    randomInt = random.randint(0, 2)
                    if randomInt == 0:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getBelowPixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    elif randomInt == 1:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getLeftPixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    elif randomInt == 2:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getRightPixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    pixels[pixelRandomWidthCo, pixelRandomHeightCo] = pixels[pixel_coordinate_width, pixel_coordinate_height]
                
                elif pixel_coordinate_height == image_height-1:
                    randomInt = random.randint(0, 2)
                    if randomInt == 0:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getAbovePixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    elif randomInt == 1:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getLeftPixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    elif randomInt == 2:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getRightPixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    pixels[pixelRandomWidthCo, pixelRandomHeightCo] = pixels[pixel_coordinate_width, pixel_coordinate_height]
                else:
                    randomInt = random.randint(0, 3)
                    if randomInt == 0:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getAbovePixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    elif randomInt == 1:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getLeftPixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    elif randomInt == 2:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getRightPixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    elif randomInt == 3:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getBelowPixelCo(image_width, image_height, pixel_coordinate_width, pixel_coordinate_height)
                    pixels[pixelRandomWidthCo, pixelRandomHeightCo] = pixels[pixel_coordinate_width, pixel_coordinate_height]

        print(str(pixel_coordinate_height) + "/" + str(image_height))

    im.save("pixel_grid.bmp")
    print("Modify " + str(intOnePixelProvince) + " One-pixel province(s)")


def __getAbovePixelCo(_image_width, _image_height, _pixel_width_co, _pixel_height_co):
    if _pixel_height_co == 0:
        pixel_above_width_co = _pixel_width_co
        pixel_above_height_co = 0
    else:
        pixel_above_width_co = _pixel_width_co
        pixel_above_height_co = _pixel_height_co-1
    return pixel_above_width_co, pixel_above_height_co

def __getBelowPixelCo(_image_width, _image_height, _pixel_width_co, _pixel_height_co):
    if _pixel_height_co == _image_height-1:
        pixel_below_width_co = _pixel_width_co
        pixel_below_height_co = _image_height-1
    else:
        pixel_below_width_co = _pixel_width_co
        pixel_below_height_co = _pixel_height_co+1
    return pixel_below_width_co, pixel_below_height_co

def __getLeftPixelCo(_image_width, _image_height, _pixel_width_co, _pixel_height_co):
    if _pixel_width_co == 0:
        pixel_left_width_co = _image_width-1
        pixel_left_height_co = _pixel_height_co
    else:
        pixel_left_width_co = _pixel_width_co-1
        pixel_left_height_co = _pixel_height_co
    return pixel_left_width_co, pixel_left_height_co

def __getRightPixelCo(_image_width, _image_height, _pixel_width_co, _pixel_height_co):
    if _pixel_width_co == _image_width-1:
        pixel_right_width_co = 0
        pixel_right_height_co = _pixel_height_co
    else:
        pixel_right_width_co = _pixel_width_co+1
        pixel_right_height_co = _pixel_height_co
    return pixel_right_width_co, pixel_right_height_co

def checkSurrendingPixel(_pixels, _image_width, _image_height, _pixel_width_co, _pixel_height_co):
    pixel_above_width_co, pixel_above_height_co = __getAbovePixelCo(_image_width, _image_height, _pixel_width_co, _pixel_height_co)
    pixel_below_width_co, pixel_below_height_co = __getBelowPixelCo(_image_width, _image_height, _pixel_width_co, _pixel_height_co)
    pixel_left_width_co,  pixel_left_height_co  = __getLeftPixelCo(_image_width, _image_height, _pixel_width_co, _pixel_height_co)
    pixel_right_width_co, pixel_right_height_co = __getRightPixelCo(_image_width, _image_height, _pixel_width_co, _pixel_height_co)
    if _pixels[_pixel_width_co, _pixel_height_co] == _pixels[pixel_above_width_co, pixel_above_height_co]:
        return False
    elif _pixels[_pixel_width_co, _pixel_height_co] == _pixels[pixel_below_width_co, pixel_below_height_co]:
        return False
    elif _pixels[_pixel_width_co, _pixel_height_co] == _pixels[pixel_left_width_co,  pixel_left_height_co]:
        return False
    elif _pixels[_pixel_width_co, _pixel_height_co] == _pixels[pixel_right_width_co, pixel_right_height_co]:
        return False
    else:
        return True


if __name__ == "__main__":
    main()
