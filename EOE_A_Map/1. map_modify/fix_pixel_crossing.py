from tkinter import filedialog
from PIL import Image

def get_crossing_position():
    full_filename = filedialog.askopenfilename(title = "Choose error.log file", filetypes={("log file", ".log .txt")})
    file_str_original = open(full_filename)
    all_text_str = file_str_original.readlines()
    file_str_original.close()

    text_list = []
    for i in range(len(all_text_str)):
        if 'Map invalid X crossing' in all_text_str[i]:
            text_list.append(all_text_str[i])

    crossing_position_list = []
    for i in range(len(text_list)):
        text_list[i] = text_list[i].split(':')
        x, y = text_list[i][5].split(',')
        x = int(x)
        y = int(y)
        crossing_position_list.append([x,y])

    return crossing_position_list

def fix_pixels_crossing():
    crossing_position_list = get_crossing_position()
    full_filename = filedialog.askopenfilename(title = "Choose Province Map File (province.bmp)", filetypes={("HOI Map file", ".bmp")})
    im = Image.open(full_filename)
    pixels = im.load()

    for i in range(len(crossing_position_list)):
        x = crossing_position_list[i][0]
        y = crossing_position_list[i][1]
        pixels[x,y-2] = pixels[x,y-1]

    save_file = filedialog.asksaveasfilename(title = "save province.bmp")
    im.save(save_file)

def main():
    fix_pixels_crossing()

if __name__ == "__main__":
    main()
