import warnings

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QLineEdit


class KeySequenceEdit(QLineEdit):
    """
    This class is mainly inspired by
    http://stackoverflow.com/a/6665017
https://stackoverflow.com/questions/6647970/how-can-i-capture-qkeysequence-from-qkeyevent-depending-on-current-keyboard-layo
    """

    def __init__(self, *args):
        super(KeySequenceEdit, self).__init__(*args)

        self.keySequence = QKeySequence()

    def setKeySequence(self, keySequence):
        self.keySequence = keySequence
        self.setText(self.keySequence.toString(QtGui.QKeySequence.NativeText))

    def keyPressEvent(self, e):
        if e.type() == QtCore.QEvent.KeyPress:
            key = e.key()

            if key == QtCore.Qt.Key_unknown:
                warnings.warn("Unknown key from a macro probably")
                return

            # the user have clicked just and only the special keys Ctrl, Shift, Alt, Meta.
            if (key == QtCore.Qt.Key_Control or
                    key == QtCore.Qt.Key_Shift or
                    key == QtCore.Qt.Key_Alt or
                    key == QtCore.Qt.Key_Meta):
                print("Single click of special key: Ctrl, Shift, Alt or Meta")
                print("New KeySequence:", QtGui.QKeySequence(key).toString(QtGui.QKeySequence.NativeText))
                return

            # check for a combination of user clicks
            modifiers = e.modifiers()
            keyText = e.text()
            # if the keyText is empty than it's a special key like F1, F5, ...
            print("Pressed Key:", keyText)

            if modifiers & QtCore.Qt.ShiftModifier:
                key += QtCore.Qt.SHIFT
            if modifiers & QtCore.Qt.ControlModifier:
                key += QtCore.Qt.CTRL
            if modifiers & QtCore.Qt.AltModifier:
                key += QtCore.Qt.ALT
            if modifiers & QtCore.Qt.MetaModifier:
                key += QtCore.Qt.META

            print("New KeySequence:", QtGui.QKeySequence(key).toString(QtGui.QKeySequence.NativeText))

            self.setKeySequence(QtGui.QKeySequence(key))
