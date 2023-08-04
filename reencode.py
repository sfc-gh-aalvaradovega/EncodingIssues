import re
import os
import fnmatch
import io
import argparse
import chardet
from pathlib import Path

arguments_parser = argparse.ArgumentParser(description="General file re-encoder to UTF-8")
arguments_parser.add_argument('--inputdir',required=True, help='This is the directory where your files are')
arguments_parser.add_argument('--ext',required=False,  nargs='?', default=".*", help='OPTIONAL, Filter files using an specific file extension')
arguments_parser.add_argument('--encoding',required=False, nargs='?', help='OPTIONAL, Add any number of encodings needed, separate them by ",". ')
arguments_parser.add_argument('--auto', required=False, nargs='?', default=True, help='OPTIONAL, True/False, Force automatic detection of encoding.')
arguments = arguments_parser.parse_args()

input_directory = arguments.inputdir
filext =  arguments.ext
otherencodes = [] if arguments.encoding is None else  arguments.encoding.split(",")
auto = arguments.auto

path = Path(input_directory)
par_dir = path.parent.absolute()
encodings_list = ['utf-8'] + otherencodes     
error_report = ''
log = '';


write_dir =  os.path.join(par_dir, "reencode_out")
print(write_dir)
filePattern = "*" + filext

if not os.path.exists(write_dir):
    os.makedirs(write_dir)    
for path, dirs, files in os.walk(os.path.abspath(input_directory)):
    rel_pat = os.path.relpath(path, par_dir)
    print (path)
    writepath = os.path.join(write_dir, rel_pat)
    if not os.path.exists(writepath):
        os.makedirs(writepath)  
    for filename in fnmatch.filter(files, filePattern):
        filepath = os.path.join(path, filename)
        print("Reading..." + filename)
        encoding = None
        counter = 0
        while encoding is None and counter < len(encodings_list):   
            try:
                with io.open(filepath, mode='r', encoding=encodings_list[counter]) as file:
                    lines = file.read()
            except UnicodeDecodeError: 
                print (encodings_list[counter] + " failed. Trying a different encoding.")
            except :
                print("Unexpected Error")
                encoding = "Error"
            else :
                encoding = encodings_list[counter]
            finally:
                counter = counter + 1
        
        if auto == 'True' and encoding is None and encoding != "Error"  :
            lines = open(filepath, 'rb').read()
            result = chardet.detect(lines)
            confidence = result['confidence']
            chardet_enc = result['encoding']
            if confidence > 0.9:
                try:
                    with io.open(filepath, mode='r', encoding= chardet_enc ) as file:
                        lines = file.read()
                except UnicodeDecodeError: 
                    print (encodings_list[counter] + "failed. Trying a different encoding.")
                except :
                    print("Unexpected Error")
                    encoding = "Error"
                else :
                    encoding = chardet_enc
              
        if encoding is not None and encoding != "Error":
            print (f"Writing file with original {encoding} encoding to UTF-8...")
            filename = filename.replace(filext, ".sql")
            writefilepath = os.path.join(writepath, filename)
            with io.open(writefilepath, mode='w', encoding="utf-8") as file:
                for line in lines:
                    file.write(line)
            if encoding != "utf-8":
                log = log + filepath + " encoded to : " + encoding + ".\n"
        else :
            error_report = error_report + filepath +  ", Encoding could not be determined, try using --encoding to especify the encoding\n"
            

filepath = os.path.join(write_dir, "Error_report.txt")
with io.open(filepath, mode='w', encoding="utf-8") as file:
    file.write(error_report)
    

filepath = os.path.join(write_dir, "log.txt")
with io.open(filepath, mode='w', encoding="utf-8") as file:
    file.write(log)
    
print ("______________________________________________________")
