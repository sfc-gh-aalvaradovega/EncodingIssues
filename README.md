Usage

You will need to validate if you have Chardet installed on your pc, if not please use this command to install:
pip install chardet
Use in order to convert from encodings not supported by the SnowConvert tool,  files under the input directory are converted to UTF-8, for the SnowConvert tool to use. 

Syntax reencode.py [-h] --inputdir INPUTDIR [--ext [EXT]] [--encoding [ENCODING]] [--auto [AUTO]]

General file re-encoder to UTF-8

Arguments:
  -h, --help      Show help message and exit
  --inputdir     This is the directory where your files are
  --ext             OPTIONAL, Filter files using an specific file extension
                       For example, if you want to use slq files use --ext ".sql" 
  --encoding   OPTIONAL, Add any number of encodings needed, separate them by ",".
                       Use this if you know what encoding is being used in the files.
                       For example 
  --auto           OPTIONAL, True/False, Force automatic detection of encoding.
  
  
  Support
  
  For any issues or feedback please contact Alejandro Alvarado ( a.alvaradovega@snowflake.com)
