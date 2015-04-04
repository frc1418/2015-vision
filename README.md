FRC1418 2015 Image Processing Code
================================

We're really excited to release our image processing code for 2015! Due to
mechanical restrictions we did not use any image processing during compitition.
However we devoloped some cool features that we as a team are really proud of.

Details
================

How we get images
------------

To get images from the roborio we used a mjpg stream compiled by a third party
for the roborio. This program allowed us to stream over images while staying within 
the bandwith limitations of FRC.
	
What we do with image prosessing
-----------------------------

We use image processing to center the robot on yellow totes as well as tiped over 
contaners. We created functions that can be callen by our main program to use these
different functionalities

More on our features:

* Detection of fallen over contaners
  * Finds the black from a camera pointing at the hole of a fallen contaners
  * Used to center the robot during atonomus mode and teleop on cans
  * Detection code can be found in robot-vision/detectBlack.py
* Detection of yellow totes
  * Finds the yellow and finds the center of the tote
  * Used to center the robot on yellow totes during autonomus
  * Detection code can be found in robot-vision/detectYellow.py

Other developed ideas/features
----------------------------

We played around with alot of features this year. All of our scrapped code can be
found in scratchpad/ . 

Authors
=======

Students

* Ben Rice
* Carter Fendley

Dustin Spicuzza, mentor

