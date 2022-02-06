from tkinter import filedialog

def main():
    country_tags_serier = 'U'
    country_names = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

    text_list = []
    for index, item in enumerate(country_names):
        text_list.append(' ' + country_tags_serier + str(index+1) + '_fascism:0 "' + item + ' Reich"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_fascism_DEF:0 "the ' + item + ' Reich"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_democratic:0 "' + item + ' Republic"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_democratic:0 "the ' + item + ' Republic"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_neutrality:1 "' + item + ' Empire"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_neutrality_DEF:1 "the ' + item + ' Empire"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_communism:0 "Socialist Republic of ' + item + '"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_communism_DEF:0 "the Socialist Republic of ' + item + '"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_fascism_ADJ:0 "' + item + '"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_democratic_ADJ:0 "' + item + '"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_neutrality_ADJ:0 "' + item + '"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_communism_ADJ:0 "' + item + '"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + ':0 "' + item + '"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_DEF:0 "' + item + '"\n')
        text_list.append(' ' + country_tags_serier + str(index+1) + '_ADJ:0 "' + item + '"\n')



    textfile = open("a_file.txt", "w")
    for element in text_list:
        textfile.write(element)
    textfile.close()








if __name__ == '__main__':
    main()