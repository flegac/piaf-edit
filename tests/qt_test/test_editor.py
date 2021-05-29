from qutepart import Qutepart

from piafedit.ui_utils import gui_app

if __name__ == '__main__':
    with gui_app():
        editor = Qutepart()
        editor.completionEnabled = True
        with open(__file__) as _:
            editor.text = _.read()
        editor.show()

        editor.detectSyntax(xmlFileName='python.xml')
