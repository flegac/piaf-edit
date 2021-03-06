from PyQt5.QtCore import QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileIconProvider, QFileSystemModel, QTreeView

from piafedit.ui_utils import gui_app


class IconProvider(QFileIconProvider):
    def icon(self, fileInfo):
        if fileInfo.isDir():
            return QIcon("folder.png")
        return QFileIconProvider.icon(self, fileInfo)


if __name__ == "__main__":
    with gui_app():
        file_model = QFileSystemModel()
        file_model.setIconProvider(IconProvider())
        file_model.setRootPath(QDir.currentPath())
        browse_tree = QTreeView()
        browse_tree.setModel(file_model)
        browse_tree.show()
