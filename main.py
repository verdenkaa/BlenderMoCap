import sys
import os
import json
import shutil
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)

        self.bool_funk = lambda b: 1 if b.isChecked() else 0

        self.Start.clicked.connect(self.run)
        self.way_button.clicked.connect(self.get_way)
        self.export_button.clicked.connect(self.get_export_way)

        with open('config/ways.json', "r") as f:
            self.ways = json.load(f)

        self.way.setText(self.ways["blender_way"])
        self.export_2.setText(self.ways["export"])
        self.static_image_mode.setChecked(self.ways["static_image_mode"])
        self.smooth_landmarks.setChecked(self.ways["smooth_landmarks"])
        self.new_file_status.setChecked(self.ways["new_file_status"])
        self.min_detection_confidence.setValue(self.ways["min_detection_confidence"])
        self.min_tracking_confidence.setValue(self.ways["min_tracking_confidence"])


        self.static_image_mode.toggled.connect(lambda: self.commit_bool(text="static_image_mode.toggled", check=self.static_image_mode))
        self.smooth_landmarks.toggled.connect(lambda: self.commit_bool(text="smooth_landmarks", check=self.smooth_landmarks))
        self.new_file_status.toggled.connect(lambda: self.commit_bool(text="new_file_status", check=self.new_file_status))
        self.min_detection_confidence.valueChanged.connect(lambda: self.commit_number(text="min_detection_confidence", num=self.min_detection_confidence.value()))
        self.min_tracking_confidence.valueChanged.connect(lambda: self.commit_number(text="min_tracking_confidence", num=self.min_tracking_confidence.value()))


    def run(self):
        i = 0
        if not self.ways["new_file_status"]:
            while os.path.isfile(self.ways["export"] + f"/pose_{i}.blend"):
                i += 1
            shutil.copyfile("blend/pose.blend", self.ways["export"] + f"/pose_{i}.blend")
        else:
            shutil.copyfile("blend/pose.blend", self.ways["export"] + f"/pose_{i}.blend")
        shutil.copyfile("blend/pose_tracking_full_body_landmarks.png", self.ways["export"] + "/pose_tracking_full_body_landmarks.png")

        os.system("D:/Programs/steam/steamapps/common/Blender/blender.exe " + str(self.ways["export"] + f"/pose_{i}.blend") + " --python work.py")

    def get_way(self):
        dir = QFileDialog.getOpenFileName(None, 'Укажите blender.exe', './', "*.exe")
        self.way.setText(dir[0])
        self.ways["blender_way"] = dir[0]
        self.commit()

    def get_export_way(self):
        dir = QFileDialog.getExistingDirectory(None, 'Укажите папку экспорта')
        self.export_2.setText(dir)
        self.ways["export"] = dir
        self.commit()

    def commit_bool(self, text, check):
        self.ways[text] = self.bool_funk(check)
        self.commit()

    def commit_number(self, text, num):
        self.ways[text] = num
        self.commit()

    def commit(self):
        with open('config/ways.json', "w") as f:
            json.dump(self.ways, f, indent=2)




def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
