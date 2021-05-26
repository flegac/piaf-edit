"""An example of embedding a RichJupyterWidget in a PyQT Application.

This uses a normal kernel launched as a subprocess. It shows how to shutdown
the kernel cleanly when the application quits.

To run:

    python3 embed_qtconsole.py
"""
import sys

from qtpy import QtWidgets

from piafedit.gui.notebook import Notebook

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Notebook()
    window.show()
    sys.exit(app.exec_())
