
delivery:
	pyinstaller piafedit/main.py

qt_designer:
	pyqt5-tools designer

install:
	pip install .

uninstall:
	pip uninstall -y piaf-edit
