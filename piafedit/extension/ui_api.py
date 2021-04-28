from dataclasses import dataclass
from typing import Callable, Any, Dict, Set

from PyQt5 import QtCore
from PyQt5.QtGui import QKeyEvent, QKeySequence

from piafedit.gui.common.handler.keyboard_handler import KeyboardHandler


@dataclass
class UIAction:
    name: str
    tooltip: str
    shortcut: str
    action: Callable[[], Any]


class _Actions:
    def __init__(self):
        self.by_name: Dict[str, UIAction] = dict()
        self.by_shortcut: Dict[str, UIAction] = dict()
        self.shortcuts: Set[str] = set()

    def action(self, name: str, tooltip: str = None, shortcut: str = None):
        def decorator(fn: Callable[[], Any]):
            print('register:', name, fn)
            action = UIAction(name, tooltip, shortcut, fn)
            self.by_name[name] = action
            self.by_shortcut[shortcut] = action
            return action

        return decorator

    def handler(self):
        return MyKeyboardHandler(self)


class MyKeyboardHandler(KeyboardHandler):
    def __init__(self, actions: _Actions):
        self.actions = actions

    def keyPressEvent(self, ev: QKeyEvent):
        from piafedit.editor_api import P

        modifiers = ev.modifiers()
        if modifiers == QtCore.Qt.ShiftModifier:
            print('Shift+Click')
        elif modifiers == QtCore.Qt.ControlModifier:
            print('Control+Click')
        elif modifiers == (QtCore.Qt.ControlModifier | QtCore.Qt.ShiftModifier):
            print('Control+Shift+Click')
        else:
            print('Click')

        key = QKeySequence(ev.modifiers() | ev.key())

        print('-----', key.toString() )

        for shortcut, action in self.actions.by_shortcut.items():
            sequence = QKeySequence(shortcut)
            print(sequence.toString())
            P.log.debug(sequence)
            if key.matches(sequence):
                action.action()


class Ui:
    actions = _Actions()

    @staticmethod
    def action(name: str, tooltip: str = None, shortcut: str = None):
        return Ui.actions.action(name, tooltip, shortcut)
