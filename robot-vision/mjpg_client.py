#!/usr/bin/env python3
#
# Streams jpeg data from mjpg-streamer on the robot
#

import re
import sys
import time
from urllib.request import urlopen

import cv2
import numpy as np

def process_stream(url, processor):
    
    connected = False
    
    while True:
        
        if connected:
            print("Disconnected from", url)
            connected = False
        
        stream = None
        try:
            stream = urlopen(url)
        except:
            time.sleep(0.5)
            continue
        
        connected = True
        print("Connected to", url)
        
        try:
            _read_stream(stream, processor)
        except Exception as e:
            print("Exception:", e)
        
        if stream is not None:
            try:
                stream.close()
            except:
                pass

def _read_stream(stream, processor):
    # Read the boundary message and discard
    stream.readline()
    
    sz = 0
    rdbuffer = None
    
    clen_re = re.compile(b'Content-Length: (\d+)\\r\\n')
    
    # Read each frame
    # TODO: This is hardcoded to mjpg-streamer's behavior
    while True:
          
        stream.readline()                    # content type
        
        try:                                 # content length
            m = clen_re.match(stream.readline()) 
            clen = int(m.group(1))
        except:
            return
        
        stream.readline()                    # timestamp
        stream.readline()                    # empty line
        
        # Reallocate buffer if necessary
        if clen > sz:
            sz = clen*2
            rdbuffer = bytearray(sz)
            rdview = memoryview(rdbuffer)
        
        # Read frame into the preallocated buffer
        stream.readinto(rdview[:clen])
        
        stream.readline() # endline
        stream.readline() # boundary
        
        # Do something with the image if required, else discard
        if processor.should_process():
        
            img = cv2.imdecode(np.frombuffer(rdbuffer, count=clen, dtype=np.byte), flags=cv2.IMREAD_COLOR)
            processor.process(img)



if __name__ == '__main__':
    from main import NoOpProcessor
    process_stream(sys.argv[1], NoOpProcessor())
