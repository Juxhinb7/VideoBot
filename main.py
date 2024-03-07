import logging
from gui import start_gui_app


def main():
    logging.basicConfig(filename="logs/program.log", encoding="utf-8", level=logging.DEBUG, filemode="w")
    start_gui_app()


if __name__ == "__main__":
    main()
