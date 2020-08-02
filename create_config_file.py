from configparser import ConfigParser

config = ConfigParser()

config['macros'] = {
    'key.caps_lock' : 'macMacros_togle',
    'm': 'macMove',
    'c': 'macCopy',
    'g': 'macGrid_view_togle',
    'h': 'macGrid_onoff_togle'
}

config['settings'] = {
    'threshold': '0.75',
    'disable_macros': '0'
}

with open('./macros.ini', 'w') as f:
      config.write(f)