#!/usr/bin/env python3

from networktables import NetworkTable
from optparse import OptionParser

import time

import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    
    parser = OptionParser()
    
    parser.add_option('--on', action='store_true', default=False)
    parser.add_option('--off', action='store_true', default=False)
    
    options, args = parser.parse_args()
    
    if len(args) == 0:
        parser.error("Specify robot IP")
        
    NetworkTable.setIPAddress(args[0])
    NetworkTable.setClientMode()
    NetworkTable.initialize()
    
    sd = NetworkTable.getTable('SmartDashboard')
    
    time.sleep(2)
    
    if options.on:
        sd.putBoolean('findBin', True)
    elif options.off:
        sd.putBoolean('findBin', False)
    else:
        parser.error("Specify either --on or --off")
    
    time.sleep(1)
    
    
    