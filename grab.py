# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import sys
import datetime

import cv2
import PIL.Image
import PIL.ImageDraw


def get_images(base_filename):
    """
    Step through cameras, capturing images.
    """
    camCounter = 0
    frame = capture_frame(camCounter)
    if frame is False:
        print('Could not capture frame. Is a webcam connected?')
        sys.exit(1)

    while frame is not False:

        # Convert to a PIL image
        img = cv_to_pil(frame)

        # Add timestamp
        add_timestamp(img)

        # Save image
        filename = '%s_%d.jpg' % (base_filename, camCounter)
        img.save(filename)

        # Next camera...
        camCounter += 1
        frame = capture_frame(camCounter)


def capture_frame(cam_num):
    """
    Capture an image from the given camera. Return a numpy ndarray with
    the image data.
    """
    cam = cv2.VideoCapture(cam_num)
    retval, image = cam.read()
    cam.release()
    if retval is False:
        return False
    else:
        return image


def cv_to_pil(img):
    """
    Convert a OpenCV image to a PIL image.
    """
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return PIL.Image.fromarray(rgb)


def add_timestamp(img):
    """
    Add the timestamp to the image. This works in-place.
    """
    draw = PIL.ImageDraw.Draw(img)
    timestamp = datetime.datetime.now().isoformat().replace('T', ' ').split('.')[0]
    draw.text((10, img.size[1] - 20), timestamp, (255, 255, 255))

if __name__ == '__main__':

    # Parse args
    if len(sys.argv) != 2:
        print('Usage: %s <webcamname>' % sys.argv[0])
        sys.exit(1)

    # Remove existing images (in case camera was removed we don't want
    # its old image hanging around).
    for i in range(10):
        filename = '%s_%d.jpg' % (sys.argv[1], i)
        if os.path.isfile(filename):
            os.remove(filename)

    # Go!
    get_images(sys.argv[1])
