from ui.ui import * #Import star bad, but need it to make it work w/ cmu graphics4
from data.datamanager import DataManager

def main():
    dm = DataManager()
    run_ui(datamanager=dm) #From ui.ui

if __name__ == '__main__':
    main()