import time
from auth_me.menu_me import Menu

if __name__ == '__main__':
    m = Menu()

    while True:
        option = m.display_options()

        if not option:
            time.sleep(2)
            break
        else:
            time.sleep(2)
            continue
