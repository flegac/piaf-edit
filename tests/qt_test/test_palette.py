from PyQt5.QtWidgets import QColorDialog

from piafedit.ui_utils import gui_app

if __name__ == "__main__":
    with gui_app():
        window = QColorDialog()
        window.show()
