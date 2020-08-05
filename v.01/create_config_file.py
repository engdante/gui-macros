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
    'threshold': '0.95',
    'disable_macros': '0',
    'disable_macros_text_0' : 'Running',
    'disable_macros_text_1' : 'Suspend',
    'disable_macros_color_0' : 'blue',
    'disable_macros_color_1' : 'red',
    'disable_gridSnap' : '0',
    'disable_gridSnap_color_0' : 'green',
    'disable_gridSnap_color_1' : 'red',
    'disable_gridSnap_text_0' : 'Grid ON',
    'disable_gridSnap_text_1' : 'Grid OFF',
    'last_key' : '_'
}

with open('./macros.ini', 'w') as f:
      config.write(f)