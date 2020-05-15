import numpy


arr1 = [[1,1],[1,2],[1,3]]

arr_var = numpy.var(arr1)

def fact(n):
    if n==1:
        return 1
    else:
        x = n * fact(n - 1)
    return x

def floodfill(x, y, oldColor, newColor):
    # assume surface is a 2D image and surface[x][y] is the color at x, y.
    theStack = [ (x, y) ]
    while len(theStack) > 0:
        x, y = theStack.pop()
        if surface[x][y] != oldColor:
            continue
        
        surface[x][y] = newColor
        theStack.append( (x + 1, y) )  # right
        theStack.append( (x - 1, y) )  # left
        theStack.append( (x, y + 1) )  # down
        theStack.append( (x, y - 1) )  # up


def floodfill(surface, oldColor, xMax, yMax, x, y, newColor):
    # assume surface is a 2D image and surface[x][y] is the color at x, y.
    #(pixels, pixelRGB, imageWidth, imageHeight, countImageWidth, countImageHeight, (0,0,0))
    theStack = [ (x, y) ]
    theArea = []
    while len(theStack) > 0:
        x, y = theStack.pop()

        
        if x == xMax or y == yMax:
            arront = (0,0,0)
        else:
            arront = surface[x,y]

        if arront != oldColor:
            a = 1
        else:
            surface[x,y] = newColor
            theArea.append([x,y])
            theStack.append( (x + 1, y) )  # right
            theStack.append( (x - 1, y) )  # left
            theStack.append( (x, y + 1) )  # down
            theStack.append( (x, y - 1) )  # up

    return theArea, surface


def main():
    F(6)

main()