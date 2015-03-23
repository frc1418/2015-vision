#!/usr/bin/env python3

import cv2
import numpy
import argparse
import detectBlack
from networktables import NetworkTable


class NoOpProcessor:
    
    def should_process(self):
        return True
    
    def process(self, img):
        cv2.imshow('Image', img)
        cv2.waitKey(1)


class ImageProcessor:
    
    def __init__(self, networked, verbose):
        self.networked = networked
        self.verbose = verbose
        
        if networked:
            self.sd = NetworkTable.getTable("SmartDashboard")
    
    def should_process(self):
        if self.networked:
            return self.sd.getBoolean("findBin", False)
        else:
            return True
    
    def process(self, img):
        
        bin_position, coordinates = detectBlack.detect_black(img)
        if self.networked:
            self.sd.putDouble("binPosition", bin_position)
            self.sd.putValue("rectanglePoints", coordinates)
        else:
            print("Bin Position: %s" % bin_position)
        
        if self.verbose:
            cv2.imshow('Image', img)
            cv2.waitKey(1)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--networked", action="store_true", default=False,
                        help="Use network tables to activate finder")
    
    parser.add_argument("--capture", action="store_true", default=False,
                        help="Capture from first local camera")
    
    parser.add_argument("--url", default=None,
                        help="Capture from mjpg-streamer URL (like http://10.14.18.2:5800/?action=stream)")
    
    parser.add_argument("-v", '--verbose', action="store_true", default=False,
                        help="Show image")
    
    
    args = parser.parse_args()
    
    if args.networked:
        NetworkTable.setIPAddress("localhost")
        NetworkTable.setClientMode()
        NetworkTable.initialize()
        
    processor = ImageProcessor(args.networked, 
                               args.verbose)
        
    if args.url is not None:
        import mjpg_client
        mjpg_client.process_stream(args.url, processor)
    
    elif args.capture:
        import cv_client
        cv_client.process_stream(processor)
        
    else:
        parser.error("Must specified --url or --capture")
    