import time
from pathlib import Path
from typing import Optional

from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtWidgets import *

from piafedit.ui_utils import gui_app


class CameraManager:

    def __init__(self):
        self.available_cameras = QCameraInfo.availableCameras()
        self.save_seq = 0
        self.capture: Optional[QCameraImageCapture] = None
        self.camera: Optional[QCamera] = None
        self.current_camera_name: str = ''
        self.tool_bar = self.create_toolbar()
        self.view_finder = QCameraViewfinder()
        self.select_camera(0)

    def select_camera(self, i):
        self.camera = QCamera(self.available_cameras[i])
        self.camera.setViewfinder(self.view_finder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.error.connect(lambda: print(self.camera.errorString()))
        self.camera.start()
        self.capture = QCameraImageCapture(self.camera)
        self.capture.error.connect(lambda error_msg, error, msg: print(msg))
        self.capture.imageCaptured.connect(lambda d, i: print(f'Image captured : {self.save_seq}'))
        self.current_camera_name = self.available_cameras[i].description()
        self.save_seq = 0

    def click_photo(self):
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        path = Path.cwd() / f'{self.current_camera_name}-{timestamp}.{self.save_seq}.jpg'
        print(path)
        self.capture.capture(str(path))
        self.save_seq += 1

    def create_toolbar(self):
        toolbar = QToolBar("Camera Tool Bar")
        click_action = QAction("Photo!", toolbar)
        click_action.triggered.connect(self.click_photo)
        toolbar.addAction(click_action)
        camera_selector = QComboBox()
        camera_selector.addItems([camera.description() for camera in self.available_cameras])
        camera_selector.currentIndexChanged.connect(self.select_camera)
        toolbar.addWidget(camera_selector)
        return toolbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 800, 600)

        self.manager = CameraManager()

        self.setCentralWidget(self.manager.view_finder)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage('tata')
        self.status.setStatusTip('toto')

        self.addToolBar(self.manager.tool_bar)

    def alert(self, msg):
        error = QErrorMessage(self)
        error.showMessage(msg)


if __name__ == "__main__":
    with gui_app():
        window = MainWindow()
        window.show()
