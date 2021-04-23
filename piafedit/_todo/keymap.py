from piafedit._todo.actions import ShorcutMapping, Shortcut, Actions

KEYMAP = ShorcutMapping()
for _ in [
    Shortcut("CTRL+Q", Actions.exit),
]:
    KEYMAP.register(_)
