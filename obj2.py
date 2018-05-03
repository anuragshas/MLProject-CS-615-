# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from yolo_model import *
import time
import datetime

class Ui_MainWindow(object):
    def load_model(self):
        model = model_yolo()
        #model.summary()
        model.load_weights("weights_coco.h5")
        return model
    
    def image_pred(self, MainWindow):
        model = self.load_model()
        file_path = self.label.text()
        frame = cv2.imread(file_path)
        image = self.predict_image(self,image=frame,model=model)
        while True:
            cv2.imshow('image', np.uint8(image))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cv2.destroyAllWindows()

    def video_pred(self, MainWindow):
        model = self.load_model()
        file_path = self.label.text()
        capture = cv2.VideoCapture(file_path)
        size = (
            int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        output = cv2.VideoWriter('result_videos/result'+datetime.datetime.now().strftime("%y-%m-%d-%H-%M")+'.avi', codec, 30.0, size)

        i = 0
        frame_rate_divider = 10
        while(capture.isOpened()):
            ret, frame = capture.read()
            if ret:
                if i % frame_rate_divider == 0:
                    image = self.predict_image(self,image=frame,model=model)
                    output.write(np.uint8(image))
                    cv2.imshow('video', np.uint8(image))
                    i += 1
                else:
                    i += 1
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

        capture.release()
        output.release()
        cv2.destroyAllWindows()

    def ip_camera(self):
        self.web_camera(ip_camera=True)

    def web_camera(self,ip_camera=False):
        model = self.load_model()

        if(ip_camera):
            try:
                capture = cv2.VideoCapture('http://'+self.ip_txtfield.text()+'/video?dummy=param.mjpg')
                self.label.setText(self.ip_txtfield.text())
            except:
                sys.exit(0)
        else:
            capture = cv2.VideoCapture(0)
        
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

        while True:
            stime = time.time()
            ret, frame = capture.read()
            if ret:
                image = self.predict_image(self,image=frame,model=model)

                cv2.imshow('camera', np.uint8(image))
                print('FPS {:.1f}'.format(1 / (time.time() - stime)))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        capture.release()
        cv2.destroyAllWindows()
    
    def predict_image(self, MainWindow,image,model):
        dummy_array = np.zeros((1,1,1,1,TRUE_BOX_BUFFER,4))

        input_image = cv2.resize(image, (416, 416))
        input_image = input_image / 255.
        input_image = input_image[:,:,::-1]
        input_image = np.expand_dims(input_image, 0)

        netout = model.predict([input_image, dummy_array])

        boxes = decode_netout(netout[0], 
                      obj_threshold=OBJ_THRESHOLD,
                      nms_threshold=NMS_THRESHOLD,
                      anchors=ANCHORS, 
                      nb_class=CLASS)
            
        image = draw_boxes(image, boxes, labels=LABELS)
        return image

    def file_open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            self.label.setText(fileName)

    def reset_label(self):
        self.label.setText("")

    def check_txt(self):
        if(self.ip_txtfield.text()!=""):
            self.view_ipcamera.setVisible(True)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.upload_image = QtWidgets.QPushButton(self.centralwidget)
        self.upload_image.setGeometry(QtCore.QRect(320, 180, 93, 28))
        self.upload_image.setObjectName("upload_image")
        self.upload_video = QtWidgets.QPushButton(self.centralwidget)
        self.upload_video.setEnabled(True)
        self.upload_video.setGeometry(QtCore.QRect(320, 180, 93, 28))
        self.upload_video.setObjectName("upload_video")
        self.view_camera = QtWidgets.QPushButton(self.centralwidget)
        self.view_camera.setGeometry(QtCore.QRect(290, 330, 171, 71))
        self.view_camera.setObjectName("view_camera")
        self.ip_txtfield = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_txtfield.setGeometry(QtCore.QRect(230, 180, 171, 22))
        self.ip_txtfield.setObjectName("ip_txtfield")
        self.ok = QtWidgets.QPushButton(self.centralwidget)
        self.ok.setGeometry(QtCore.QRect(440, 180, 93, 28))
        self.ok.setObjectName("ok")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(270, 240, 400, 51))
        self.label.setText("")
        self.label.setObjectName("label")
        self.view_image = QtWidgets.QPushButton(self.centralwidget)
        self.view_image.setGeometry(QtCore.QRect(290, 330, 171, 71))
        self.view_image.setObjectName("view_image")
        self.view_ipcamera = QtWidgets.QPushButton(self.centralwidget)
        self.view_ipcamera.setGeometry(QtCore.QRect(290, 330, 171, 71))
        self.view_ipcamera.setObjectName("view_ipcamera")
        self.view_video = QtWidgets.QPushButton(self.centralwidget)
        self.view_video.setGeometry(QtCore.QRect(290, 330, 171, 71))
        self.view_video.setObjectName("view_video")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(40, 70, 304, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Image = QtWidgets.QRadioButton(self.widget)
        self.Image.setChecked(True)
        self.Image.setObjectName("Image")
        self.horizontalLayout.addWidget(self.Image)
        self.Video = QtWidgets.QRadioButton(self.widget)
        self.Video.setObjectName("Video")
        self.horizontalLayout.addWidget(self.Video)
        self.Camera = QtWidgets.QRadioButton(self.widget)
        self.Camera.setObjectName("Camera")
        self.horizontalLayout.addWidget(self.Camera)
        self.IPCamera = QtWidgets.QRadioButton(self.widget)
        self.IPCamera.setObjectName("IPCamera")
        self.horizontalLayout.addWidget(self.IPCamera)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.upload_video.setVisible(False)
        self.ip_txtfield.setVisible(False)
        self.ok.setVisible(False)
        self.view_image.setVisible(False)
        self.view_video.setVisible(False)
        self.view_camera.setVisible(False)
        self.view_ipcamera.setVisible(False)
        self.Image.clicked.connect(self.upload_image.show)
        self.Video.clicked.connect(self.upload_video.show)
        self.IPCamera.clicked.connect(self.ip_txtfield.show)
        self.IPCamera.clicked.connect(self.ok.show)
        self.IPCamera.clicked.connect(self.reset_label)
        self.Video.clicked.connect(self.upload_image.hide)
        self.Video.clicked.connect(self.ip_txtfield.hide)
        self.Video.clicked.connect(self.ok.hide)
        self.Video.clicked.connect(self.reset_label)
        self.Image.clicked.connect(self.reset_label)
        self.Image.clicked.connect(self.upload_video.hide)
        self.Image.clicked.connect(self.ip_txtfield.hide)
        self.Image.clicked.connect(self.ok.hide)
        self.Camera.clicked.connect(self.reset_label)
        self.Camera.clicked.connect(self.upload_image.hide)
        self.Camera.clicked.connect(self.upload_video.hide)
        self.Camera.clicked.connect(self.ip_txtfield.hide)
        self.Camera.clicked.connect(self.ok.hide)
        self.Camera.clicked.connect(self.view_camera.show)
        self.Camera.clicked.connect(self.view_image.hide)
        self.Camera.clicked.connect(self.view_video.hide)
        self.Camera.clicked.connect(self.view_ipcamera.hide)
        
        self.Image.clicked.connect(self.view_camera.hide)
        self.Image.clicked.connect(self.view_ipcamera.hide)
        self.Image.clicked.connect(self.view_video.hide)
        
        self.Video.clicked.connect(self.view_image.hide)
        self.Video.clicked.connect(self.view_camera.hide)
        self.Video.clicked.connect(self.view_ipcamera.hide)
        
        self.ok.clicked.connect(self.check_txt)

        self.IPCamera.clicked.connect(self.view_image.hide)
        self.IPCamera.clicked.connect(self.view_camera.hide)
        self.IPCamera.clicked.connect(self.view_video.hide)
        self.IPCamera.clicked.connect(self.view_ipcamera.hide)
        
        self.IPCamera.clicked.connect(self.upload_video.hide)
        self.IPCamera.clicked.connect(self.upload_image.hide)

        
        self.upload_image.clicked.connect(self.view_image.show)
        self.upload_video.clicked.connect(self.view_video.show)

        self.upload_image.clicked.connect(self.file_open)
        self.upload_video.clicked.connect(self.file_open)
        self.view_image.clicked.connect(self.image_pred)
        self.view_video.clicked.connect(self.video_pred)
        self.view_camera.clicked.connect(self.web_camera)
        self.view_ipcamera.clicked.connect(self.ip_camera)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Object Detection"))
        self.upload_image.setText(_translate("MainWindow", "Upload Image"))
        self.upload_video.setText(_translate("MainWindow", "Upload Video"))
        self.view_camera.setText(_translate("MainWindow", "View"))
        self.ip_txtfield.setPlaceholderText(_translate("MainWindow", "Enter IP of Camera"))
        self.ok.setText(_translate("MainWindow", "OK"))
        self.view_image.setText(_translate("MainWindow", "View"))
        self.view_ipcamera.setText(_translate("MainWindow", "View"))
        self.view_video.setText(_translate("MainWindow", "View"))
        self.Image.setText(_translate("MainWindow", "Image"))
        self.Video.setText(_translate("MainWindow", "Video"))
        self.Camera.setText(_translate("MainWindow", "Camera"))
        self.IPCamera.setText(_translate("MainWindow", "IP Camera"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

