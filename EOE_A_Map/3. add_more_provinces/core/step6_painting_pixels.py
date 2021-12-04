from core import read_write_files
from tkinter import filedialog
from PIL import Image #pip install Pillow


def painting_pixels():
    print('Part 6')
    all_painting_area_dict = read_write_files.read_dict('all_painting_area_dict')
    #PYTHON_FILE_LOCATION = os.path.abspath('.')
    #temp_folder_location = PYTHON_FILE_LOCATION + "\\" + 'temp'
    #full_file_name = temp_folder_location + "\\all_painting_area_dict.txt"
    #file = open(temp_folder_location + "\\all_painting_area_dict.txt", 'rb')
    #all_painting_area_dict = joblib.load(full_file_name)
    all_painting_pixels_position = all_painting_area_dict['Painting area position']
    all_painting_pixels_color = all_painting_area_dict['Painting area color']
    #read image
    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (provinces.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()
    image_width, image_height = im.size

    for i in range(len(all_painting_pixels_position)):
        for j in range(len(all_painting_pixels_position[i])):
            x = all_painting_pixels_position[i][j][0]
            y = all_painting_pixels_position[i][j][1]
            rgb = all_painting_pixels_color[i][j]
            pixels[x,y] = tuple(rgb)



    save_file = filedialog.asksaveasfilename(title = "save provinces.bmp")
    im.save(save_file)
    print('Part 6 finished')
