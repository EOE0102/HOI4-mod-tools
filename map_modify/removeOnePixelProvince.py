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
    imageWidth, imageHeight = im.size
    intOnePixelProvince = 0
    for pixelCoordinateHeight in range(0, imageHeight-1): 
        for pixelCoordinateWidth in range(0, imageWidth-1):
            bolOnePixel = checkSurrendingPixel(pixels, imageHeight, imageWidth,pixelCoordinateWidth, pixelCoordinateHeight)
            if bolOnePixel == True:
                intOnePixelProvince = intOnePixelProvince + 1
                if pixelCoordinateHeight == 0:
                    randomInt = random.randint(0, 2)
                    if randomInt == 0:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getBelowPixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    elif randomInt == 1:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getLeftPixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    elif randomInt == 2:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getRightPixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    pixels[pixelRandomWidthCo, pixelRandomHeightCo] = pixels[pixelCoordinateWidth, pixelCoordinateHeight]
                
                elif pixelCoordinateHeight == imageHeight-1:
                    randomInt = random.randint(0, 2)
                    if randomInt == 0:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getAbovePixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    elif randomInt == 1:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getLeftPixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    elif randomInt == 2:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getRightPixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    pixels[pixelRandomWidthCo, pixelRandomHeightCo] = pixels[pixelCoordinateWidth, pixelCoordinateHeight]
                else:
                    randomInt = random.randint(0, 3)
                    if randomInt == 0:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getAbovePixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    elif randomInt == 1:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getLeftPixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    elif randomInt == 2:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getRightPixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    elif randomInt == 3:
                        pixelRandomWidthCo, pixelRandomHeightCo = __getBelowPixelCo(imageWidth, imageHeight, pixelCoordinateWidth, pixelCoordinateHeight)
                    pixels[pixelRandomWidthCo, pixelRandomHeightCo] = pixels[pixelCoordinateWidth, pixelCoordinateHeight]

        print(str(pixelCoordinateHeight) + "/" + str(imageHeight))

    im.save("pixel_grid.bmp")
    print("Modify " + str(intOnePixelProvince) + " One-pixel province(s)")


def __getAbovePixelCo(_imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo):
    if _pixelHeightCo == 0:
        pixelAboveWidthCo = _pixelWidthCo
        pixelAboveHeightCo = 0
    else:
        pixelAboveWidthCo = _pixelWidthCo
        pixelAboveHeightCo = _pixelHeightCo-1
    return pixelAboveWidthCo, pixelAboveHeightCo

def __getBelowPixelCo(_imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo):
    if _pixelHeightCo == _imageHeight-1:
        pixelBelowWidthCo = _pixelWidthCo
        pixelBelowHeightCo = _imageHeight-1
    else:
        pixelBelowWidthCo = _pixelWidthCo
        pixelBelowHeightCo = _pixelHeightCo+1
    return pixelBelowWidthCo, pixelBelowHeightCo

def __getLeftPixelCo(_imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo):
    if _pixelWidthCo == 0:
        pixelLeftWidthCo = _imageWidth-1
        pixelLeftHeightCo = _pixelHeightCo
    else:
        pixelLeftWidthCo = _pixelWidthCo-1
        pixelLeftHeightCo = _pixelHeightCo
    return pixelLeftWidthCo, pixelLeftHeightCo

def __getRightPixelCo(_imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo):
    if _pixelWidthCo == _imageWidth-1:
        pixelRightWidthCo = 0
        pixelRightHeightCo = _pixelHeightCo
    else:
        pixelRightWidthCo = _pixelWidthCo+1
        pixelRightHeightCo = _pixelHeightCo
    return pixelRightWidthCo, pixelRightHeightCo

def checkSurrendingPixel(_pixels, _imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo):
    pixelAboveWidthCo, pixelAboveHeightCo = __getAbovePixelCo(_imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo)
    pixelBelowWidthCo, pixelBelowHeightCo = __getBelowPixelCo(_imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo)
    pixelLeftWidthCo,  pixelLeftHeightCo  = __getLeftPixelCo(_imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo)
    pixelRightWidthCo, pixelRightHeightCo = __getRightPixelCo(_imageWidth, _imageHeight, _pixelWidthCo, _pixelHeightCo)
    if _pixels[_pixelWidthCo, _pixelHeightCo] == _pixels[pixelAboveWidthCo, pixelAboveHeightCo]:
        return False
    elif _pixels[_pixelWidthCo, _pixelHeightCo] == _pixels[pixelBelowWidthCo, pixelBelowHeightCo]:
        return False
    elif _pixels[_pixelWidthCo, _pixelHeightCo] == _pixels[pixelLeftWidthCo,  pixelLeftHeightCo]:
        return False
    elif _pixels[_pixelWidthCo, _pixelHeightCo] == _pixels[pixelRightWidthCo, pixelRightHeightCo]:
        return False
    else:
        return True


if __name__ == "__main__":
    main()
