from PIL import Image
import tkinter as Tkinter
from tkinter import filedialog
import cv2 as cv
import numpy as np

def main():
    root = Tkinter.Tk()
    root.filename = filedialog.askopenfilename(title = "Choose Province Map File (province.bmp)", filetypes={("HOI Map file", ".bmp"),("All files", "*.*")})
    file_path = root.filename
    source_image = cv.imread(file_path)
    source_image_rows, source_image_cows = source_image.shape[:2]


    srcTri = np.float32([[0,0],[0,100],[100,0]])
    dstTri = np.float32([[0,0],[0,200],[100,0]])
    
    warp_mat = cv.getAffineTransform(srcTri, dstTri)
    export_image = cv.warpAffine(source_image, warp_mat, (source_image_cows, 2304), flags=cv.INTER_NEAREST)
    save_file = filedialog.asksaveasfilename(title = "save provinces.bmp")
    cv.imwrite(save_file, export_image)



if __name__ == "__main__":
    main()