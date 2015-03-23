#!/usr/bin/env python

import wpilib

class MyRobot(wpilib.IterativeRobot):
    
    def robotInit(self):

        self.camera = wpilib.USBCamera()
        self.camera.startCapture()
        self.camera.setExposureAuto()
        self.cameraServer = wpilib.CameraServer()
        self.cameraServer.startAutomaticCapture(self.camera)
        

if __name__ == '__main__':
    wpilib.run(MyRobot)

