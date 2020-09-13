import keyboard


def print_key(key):
    print (key.name)

def mainApp():
    time.sleep(1)
    keyboard.hook(print_key, suppress=False)
    # keyboard.on_release(print_key, suppress=False)

import concurrent.futures
with concurrent.futures.ThreadPoolExecutor() as executor:
    thread = executor.submit(mainApp)