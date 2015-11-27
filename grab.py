# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import datetime

import cv2
import PIL.Image
import PIL.ImageDraw


def capture_frame():
    """
    Capture an image from the camera. Return a numpy ndarray with the image
    data.
    """
    cam = cv2.VideoCapture(0)
    retval, image = cam.read()
    cam.release()
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

    # Get a pygame surface
    frame = capture_frame()
    if frame is None:
        print('Could not capture frame. Is a webcam connected?')
        sys.exit(1)

    # Convert to a PIL image
    img = cv_to_pil(frame)

    # Add timestamp
    add_timestamp(img)

    # Save image
    filename = '%s.jpg' % sys.argv[1]
    img.save(filename)
