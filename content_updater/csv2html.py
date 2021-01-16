from csv import DictReader
import re
import json
from os import path

CONFIG_FILENAME = "config.json"

#loading config data
def load_config(filename):
    try:
        config = open(filename,encoding='utf-8')
        return json.load(config)
    except:
        print("your config file is malformed")

def wrap_tag(content, tag='p'):
    if tag=="a":
        return f"<{tag} href={content}> more info </{tag}>"
    return f"<{tag}> {content} </{tag}>\n"


def generate_html_list(filename):  
    generated_list=""
    config_data = load_config(CONFIG_FILENAME)

    with open('../data/'+filename+".csv", 'r', encoding='utf-8') as read_obj:
        #read csv file
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            formated_string = ""
            row = dict(row)
            #extract field names
            fieldnames = list(config_data[filename].keys())
            for field in fieldnames:
                #check for non empty values
                if row[field].strip() != "":
                    #add value to single block (wrapping with tag if exists)
                    formated_string += "{}, ".format(wrap_tag(row[field],config_data[filename][field]) if config_data[filename][field] != "" else row[field])
            #wrap list by li tag
            if formated_string.strip() != "": generated_list += wrap_tag(formated_string[:-2], "li")
    return generated_list


def write_generated_list(filename, generated_list):
    with open('../'+filename+".html", 'r', encoding='utf-8') as file :
        filedata = file.read()
    with open('../'+filename+".html", 'w', encoding='utf-8') as file :
            #find ul tag and replace it with the generated list
            injected_list=re.sub("(?is)<ul[^>]*>(.*?)<\/ul>", wrap_tag(generate_html_list(filename),"ul"), filedata)
            file.write(injected_list)

def verify_config_files_fields():
    config_data = load_config(CONFIG_FILENAME)
    #extract file names
    files_list = config_data.keys()

    for filename in files_list:
        filename='../data/'+filename+".csv"
        #check if file exists
        if path.exists(filename):
            with open(filename, "r", encoding='utf-8') as f:
                csv_dict_reader = DictReader(f)
                #extract file headers
                headers = csv_dict_reader.fieldnames
            #compare if config fields exists in headers
            fieldname_compare = set(config_data[filename.split("/")[2].split('.')[0]].keys() - set(headers))
            if len(fieldname_compare) > 0:
                print(f"{str(fieldname_compare)} not found")
                return False
        else:
            print(f'{filename} does not exist')
            return False
    return True

if __name__ == "__main__":
    check_config = verify_config_files_fields()
    if check_config:
        config_data = load_config(CONFIG_FILENAME)
        files_list = config_data.keys()
        for filename in files_list:
            generated_list = generate_html_list(filename)
            write_generated_list(filename, generated_list)