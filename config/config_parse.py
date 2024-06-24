from configparser import ConfigParser

import os
from pathlib import Path

path_config = Path(__file__).resolve().parent / 'yandex.ini'

def yandex_mail(file=path_config, section='yandex'):
    parser = ConfigParser()
    parser.read(file)
    result_parse = {}
    
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            result_parse[param[0]] = param[1]
            
    else:
        raise Exception(f'Section {section} is not found in the {file} file.')
    
    return result_parse
