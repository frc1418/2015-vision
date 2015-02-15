#!/usr/bin/env python3

import cv2
import numpy as np

from optparse import OptionParser
import socket
import struct
import threading
import time

import logging
logger = logging.getLogger('cvclient')


class CaptureClient:
    '''
        This probably isn't terribly efficient.. 
    '''
    kPort = 1180
    kMagicNumber = bytes([0x01, 0x00, 0x00, 0x00])
    kSize640x480 = 0
    kSize320x240 = 1
    kSize160x120 = 2
    
    intStruct = struct.Struct("!i")
    
    def __init__(self, options):
        self.host = options.host
        self.port = options.port
        
        self.running = True
        self.sock = None
        self.on_img = None
        
        self.fps = 10
        self.compression = 30
        self.size = self.kSize160x120
        
        self.thread = threading.Thread(target=self._capture_thread)
        
    def start(self):
        
        if self.on_img is None:
            raise ValueError("No capture function set")
        
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.sock is not None:
            self.sock.close()
            
        self.thread.join()
    
    def set_on_img(self, fn):
        self.on_img = fn
    
    def _capture_thread(self):
        
        address = (self.host, self.port)

        while self.running:
        
            self.sock = None
        
            try:
                self.sock = socket.create_connection(address, timeout=1)
                
                self.sock.settimeout(5)
                
                s = self.sock.makefile('rwb')
                self._do_capture(s)
                
            except IOError:
                
                logger.exception("Error reading data")
                
                try:
                    if self.sock is not None:
                        self.sock.close()
                except:
                    pass
                
                if self.sock is None:
                    time.sleep(1)

    def _read(self, s, size):
        data = s.read(size)
        if len(data) != size:
            raise IOError("EOF")
        return data

    def _do_capture(self, s):
        
        # TODO: Add metrics
        
        s.write(self.intStruct.pack(self.fps))
        s.write(self.intStruct.pack(self.compression))
        s.write(self.intStruct.pack(self.size))
        s.flush()
        
        while True:
            
            # read an int
            print("read")
            magic = self._read(s, 4)
            sz = self.intStruct.unpack(self._read(s, 4))[0]
            print("readsz", sz)
            # read the image buffer
            
            img_bytes = self._read(s, sz)
            
            img_bytes = np.fromstring(img_bytes, np.uint8)
            
            # decode it
            img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)
            
            # write to a buffer
            # - TODO: use two buffers to save memory allocations
            self.on_img(img)
    


if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG)
    
    parser = OptionParser()
    parser.add_option('--host', default='localhost')
    parser.add_option('--port', type='int', default=1180)

    options, args = parser.parse_args()

    capture = CaptureClient(options)
    
    img_lock = threading.Lock()
    
    imgs = [None]
    
    def _on_img(img):
        with img_lock:
            imgs[0] = img

    capture.set_on_img(_on_img)
    capture.start()

    while True:
        
        time.sleep(0.1)
        
        with img_lock:
            if imgs[0] == None:
                continue
            
            cv2.imshow("img", imgs[0])
        
        if cv2.waitKey(1)  & 0xFF == ord('q'):
            break
