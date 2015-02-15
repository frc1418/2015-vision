#!/usr/bin/env python3

#import ... cannot import wpilib, will die
# .. maybe not. but, don't want to deal with GIL

import cv2

import socket
import struct
import threading
import time

import logging
logger = logging.getLogger('cvserver')

class CameraServer:
    kPort = 1180
    kMagicNumber = bytes([0x01, 0x00, 0x00, 0x00])
    kSize640x480 = 0
    kSize320x240 = 1
    kSize160x120 = 2
    kHardwareCompression = -1
    kMaxImageSize = 200000

    intStruct = struct.Struct("!i")


    def __init__(self):
        pass
        
    def start(self):
        self.serverThread = threading.Thread(target=self._serve, name="CameraServer")
        self.serverThread.daemon = True
        self.serverThread.start()
    
    def _serve(self):
        """Run the M-JPEG server.

        This function listens for a connection from the dashboard in a
        background thread, then sends back the M-JPEG stream.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.kPort))
        sock.listen(1)
        
        while True:
            
            conn = None
            
            try:
                conn, addr = sock.accept()
                
                s = conn.makefile('rwb')
                self._write_imgs(s)
            
            except IOError:
                logger.exception("error in conn")
                continue
            finally:
                if conn is not None:
                    try:
                        conn.close()
                    except:
                        pass
    
    def _write_imgs(self, s):
        
        
        fps = self.intStruct.unpack(s.read(4))[0]
        compression = self.intStruct.unpack(s.read(4))[0]
        size = self.intStruct.unpack(s.read(4))[0]
        logger.info("Client connected: %d fps, %d compression, %d size"
                    % (fps, compression, size))
        
        vc = cv2.VideoCapture(0)
        
        vc.set(cv2.CAP_PROP_FPS, int(fps))
        
        if size == self.kSize160x120:
            w, h = 160, 120
        elif size == self.kSize320x240:
            w, h = 320, 240
        elif size == self.kSize640x480:
            w, h = 640, 480
        else:
            s.close()
            return
        
        #vc.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        #vc.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        
        #params = (cv2.IMWRITE_JPEG_QUALITY, 100 - compression)
        
        try:
        
            while True:
                
                print("Reading")
                
                # TODO: inefficient
                retval, img = vc.read()
                if not retval:
                    # Not sure what to do here
                    logger.warning("Error reading from camera")
                    break
                
                retval, data = cv2.imencode('.jpg', img)
                size = len(data)
                print(size)
                
                s.write(self.kMagicNumber)
                s.write(self.intStruct.pack(size))
                s.write(data)
                
                s.flush()
                
                # TODO: period
                
        finally:
            vc.release()
    

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)
    
    server = CameraServer()
    server._serve()
    
    while True:
        time.sleep(1)
    
