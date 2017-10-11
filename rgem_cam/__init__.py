# MIT License
#
# Copyright (c) 2017 Julian Sanin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import pygame
import pygame.camera
import picamera
from pathlib import Path
from shutil import copyfile

def TakePicture(picWidth = 1024, picHeight = 768, picFlip = False):
  lib_dir = str(Path(os.path.dirname(__file__)))
  app_dir = str(Path(os.path.dirname(__file__)).parent)
  noPicFile = os.path.join(lib_dir, "not-available.jpg")
  picFile = os.path.join(app_dir, "image.jpg")
  
  pygame.init()
  pygame.camera.init()
  pyCam = pygame.camera.Camera("/dev/video0", (picWidth, picHeight))
  try:
    pyCam.start()
  except SystemError:
    print("Cannot identify '/dev/video0': 2, No webcam attached.")
  else:
    #pyCam.set_controls(hflip = picFlip, vflip = False)
    pygame.image.save(pyCam.get_image(), picFile)
    return picFile
  
  try:
    piCam = picamera.PiCamera()
  except picamera.PiCameraError as ex:
    print("Camera is not enabled. Attach the camera cable and try running 'sudo raspi-config' and ensure that the camera has been enabled.")
  else:
    piCam.resolution = (picWidth, picHeight)
    piCam.hflip = picFlip
    piCam.capture(picFile)
    return picFile
  
  # Copy image not available file
  try:
    copyfile(noPicFile, picFile)
  except:
    pass
  else:
    return picFile
  # If everything fails...
  return noPicFile
