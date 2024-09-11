from PyQt5.QtWidgets import QMainWindow, QApplication,QMessageBox
from PyQt5.uic import loadUi
import sys
from PyQt5.QtCore import QTimer

import warnings
warnings.filterwarnings("ignore")

from header import *
from hand_tracking_g import handtracking
#
# from hnd_testing import handtracking

import senddata as ser 

class MainUI(QMainWindow): 
    def __init__(self):
        super(MainUI,self).__init__()
        loadUi("main_ui.ui",self)
        
        self.homec = [0,130,-130,0,0]
        self.thetas = self.homec.copy()
        self.xyz = fk(self.thetas)
        
        ser.push(self.thetas)

        #print(self.xyz)
        #self.counter = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timeout)
        self.button = self.px

        self.Joint_Slider_1.setRange(-90,90)
        self.Joint_Slider_2.setRange(0,180)
        self.Joint_Slider_3.setRange(-130,50)
        self.Joint_Slider_4.setRange(-90,90)
        self.Joint_Slider_5.setRange(-90,90)
        self.Joint_Slider_1.setValue(self.thetas[0])
        self.Joint_Slider_2.setValue(self.thetas[1])
        self.Joint_Slider_3.setValue(self.thetas[2])
        self.Joint_Slider_4.setValue(self.thetas[3])
        self.Joint_Slider_5.setValue(self.thetas[4])

        self.x_coordinate.display(self.xyz[0])
        self.y_coordinate.display(self.xyz[1])
        self.z_coordinate.display(self.xyz[2])

        """
        self.Joint_Slider_1.valueChanged.connect(self.receive)
        self.Joint_Slider_2.valueChanged.connect(self.receive)
        self.Joint_Slider_3.valueChanged.connect(self.receive)
        self.Joint_Slider_4.valueChanged.connect(self.receive)
        self.Joint_Slider_5.valueChanged.connect(self.receive)
        """

        self.Joint_Slider_1.sliderMoved.connect(self.sliderrecieve)
        self.Joint_Slider_2.sliderMoved.connect(self.sliderrecieve)
        self.Joint_Slider_3.sliderMoved.connect(self.sliderrecieve)
        self.Joint_Slider_4.sliderMoved.connect(self.sliderrecieve)
        self.Joint_Slider_5.sliderMoved.connect(self.sliderrecieve)
        """
        self.px.clicked.connect(self.send)
        self.nx.clicked.connect(self.send)
        self.py.clicked.connect(self.send)
        self.ny.clicked.connect(self.send)
        self.pz.clicked.connect(self.send)
        self.nz.clicked.connect(self.send)
        """
        self.px.pressed.connect(self.press)
        self.nx.pressed.connect(self.press)
        self.py.pressed.connect(self.press)
        self.ny.pressed.connect(self.press)
        self.pz.pressed.connect(self.press)
        self.nz.pressed.connect(self.press)
        self.px.released.connect(self.releas)
        self.nx.released.connect(self.releas)
        self.py.released.connect(self.releas)
        self.ny.released.connect(self.releas)
        self.pz.released.connect(self.releas)
        self.nz.released.connect(self.releas)

        self.visioncontrol.clicked.connect(self.opencamera)

        self.homeconfig.clicked.connect(self.sethome)


    #def receive(self,value):
    #print("s")
    def sethome(self):
        self.thetas = self.homec.copy()
        self.xyz = fk(self.thetas)
        
        self.Joint_Slider_1.setValue(self.thetas[0])
        self.Joint_Slider_2.setValue(self.thetas[1])
        self.Joint_Slider_3.setValue(self.thetas[2])
        self.Joint_Slider_4.setValue(self.thetas[3])
        self.Joint_Slider_5.setValue(self.thetas[4])

        self.x_coordinate.display(self.xyz[0])
        self.y_coordinate.display(self.xyz[1])
        self.z_coordinate.display(self.xyz[2])

        ser.push(self.thetas)
        #print(self.thetas)
        #print(self.homec)

    def sliderrecieve(self,value):
        #global xyz
        #global thetas
        slider = self.sender()
        if slider == self.Joint_Slider_1:
            self.thetas[0] = value
            #print(self.thetas[0])
        elif slider == self.Joint_Slider_2:
            self.thetas[1] = value
            #print(self.thetas[1])
        elif slider == self.Joint_Slider_3:
            self.thetas[2] = value
            #print(self.thetas[2])
        elif slider == self.Joint_Slider_4:
            self.thetas[3] = value
            #print(self.thetas[3])
        elif slider == self.Joint_Slider_5:
            self.thetas[4] = value
            #print(self.thetas[4])
        
        #print(self.thetas)
        ser.push(self.thetas)
        self.xyz = fk(self.thetas)
        
        self.x_coordinate.display(self.xyz[0])
        self.y_coordinate.display(self.xyz[1])
        self.z_coordinate.display(self.xyz[2])
        
    def press(self):
        #self.progress.setValue(0)
        #self.counter = 0
        self.button = self.sender()
        self.timer.start(50)

    def releas(self):
        self.timer.stop()
    
    """
    def on_timeout(self):
        #self.counter += 1
        self.progress.setValue(self.counter)
    """

    def on_timeout(self):
        #global xyz
        #global self.thetas
        
        if self.button == self.px:
            self.xyz[0] += 1
            #print(self.thetas[0])
            radius = (square(self.xyz[0])+square(self.xyz[1])+square(self.xyz[2]))
            print(radius)
            if( radius >=500 or radius <=100):
                #set label
                QMessageBox.about(self, "error", "out of reach")
                self.xyz[0] -= 1

        elif self.button == self.nx:
            self.xyz[0] -= 1
            #print(self.thetas[1])
            radius = (square(self.xyz[0])+square(self.xyz[1])+square(self.xyz[2]))
            #print(radius)
            if( radius >=500 or radius <=100):
                QMessageBox.about(self, "error", "out of reach")
                self.xyz[0] += 1

        elif self.button == self.py:
            self.xyz[1] += 1
            #print(self.thetas[2])
            radius = (square(self.xyz[0])+square(self.xyz[1])+square(self.xyz[2]))
            #print(radius)
            if( radius >=500 or radius <=100):
                #set label
                QMessageBox.about(self, "error", "out of reach")
                self.xyz[1] -= 1

        elif self.button == self.ny:
            self.xyz[1] -= 1
            #print(self.thetas[3])
            radius = (square(self.xyz[0])+square(self.xyz[1])+square(self.xyz[2]))
            #print(radius)
            if( radius >=500 or radius <=100):
                #set label
                QMessageBox.about(self, "error", "out of reach")
                self.xyz[1] += 1

        elif self.button == self.pz:
            self.xyz[2] += 1
            #print(self.thetas[2])
            radius = (square(self.xyz[0])+square(self.xyz[1])+square(self.xyz[2]))
            #print(radius)
            if( radius >=500 or radius <=100):
                #set label
                QMessageBox.about(self, "error", "out of reach")
                self.xyz[2] -= 1

        elif self.button == self.nz:
            self.xyz[2] -= 1
            radius = (square(self.xyz[0])+square(self.xyz[1])+square(self.xyz[2]))
            #print(radius)
            if( radius >=500 or  radius <=100):
                #set label
                QMessageBox.about(self, "error", "out of reach")
                self.xyz[2] += 1

        #check if in bound

        #print(self.xyz)
        self.x_coordinate.display(round(self.xyz[0]))
        self.y_coordinate.display(round(self.xyz[1]))
        self.z_coordinate.display(round(self.xyz[2]))

        ikth = ik(self.xyz)
        #print(ikth)
        for i in range(3):
            self.thetas[i] = ikth[i]
        
        
        self.Joint_Slider_1.setValue(round(self.thetas[0]))
        self.Joint_Slider_2.setValue(round(self.thetas[1]))
        self.Joint_Slider_3.setValue(round(self.thetas[2]))
        self.Joint_Slider_5.setValue(round(self.thetas[2]+self.thetas[1]))
        self.thetas[4] = self.thetas[1] + self.thetas[2]
        #print(self.thetas)
        ser.push(self.thetas)

    def opencamera(self):
        handtracking()
        print("tracking closed")





if __name__=="__main__":
    app = QApplication(sys.argv)
    ui = MainUI()
    ui.show()
    app.exec_()
    ser.close()

