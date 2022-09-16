from os import remove, getcwd, system
from os.path import join
from webbrowser import open as open_url
from requests import get

download_url = 'https://github.com/belongtothenight/CYCU-Grade-Exporter/releases/latest/download/CYCU_Grade_Exporter.exe'

print("start executing updater")
exporter_path = join(getcwd(), "CYCU_Grade_Exporter.exe")
try:
    print("found exporter, removing it")
    # remove(exporter_path) # commented for testing
    print('opening download page')
    # can't download from github directly, so this file is abandoned
    try:
        # remove(getcwd()) # commented for testing
        pass
    except:
        print('failed to remove updater')
except:
    print("exporter not found, skip removing")
