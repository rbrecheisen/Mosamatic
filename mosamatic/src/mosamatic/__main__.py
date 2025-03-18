import webbrowser
import threading
import time

from mosamatic.app import main


def open_browser():
    print('Waiting 5 seconds before opening webbrowser...')
    for i in range(5):
        time.sleep(1)
        print(i)
    webbrowser.open('http://localhost:8000')


if __name__ == "__main__":
    # threading.Thread(target=open_browser).start()
    main()
