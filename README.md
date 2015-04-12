FRC1418 2015 Image Processing Code
==================================

* Code: [Robot](https://github.com/frc1418/2015-robot) | [UI](https://github.com/frc1418/2015-ui) | **Image Processing** | [Oculus Rift](https://github.com/frc1418/2015-oculus)
* Factsheet: [Google Doc](https://docs.google.com/document/d/1irbUm-Qfxz_Ua2XiB5KzYWG2Ec5Xhr038NqL-k4FveA)

We're really excited to release our image processing code for 2015! Due to
mechanical restrictions we did not use any image processing during competition.
However we developed some cool features that we as a team are really proud of.

Details
================

How we get images
------------

To get images from the roboRIO we used a prorgram called 'mjpg-streamer' that 
was compiled by a third party for the roboRIO. This program allowed us to stream
images to the driver station while staying within the bandwidth limitations of
FRC. We can run our image processing on the roboRIO, reading from that same
stream.
	
What we do with image processing
-----------------------------

We use image processing to center the robot on yellow totes as well as tipped over 
containers. We created functions that can be called by our main program to use these
different functionalities

More on our features:

* Detection of fallen over containers
  * Finds the black from a camera pointing at the hole of a fallen containers
  * Used to center the robot during autonomous mode and teleop on containers
  * Detection code can be found in robot-vision/detectBlack.py
* Detection of yellow totes
  * Finds the yellow and finds the center of the tote
  * Used to center the robot on yellow totes during autonomous
  * Detection code can be found in robot-vision/detectYellow.py

Other developed ideas/features
----------------------------

We played around with a lot of features this year. All of our scrapped code can be
found in scratchpad/

Authors
=======

Students

* Ben Rice
* Carter Fendley

Dustin Spicuzza, mentor

