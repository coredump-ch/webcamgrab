# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import os
import sys
import datetime

import cv2
import PIL.Image
import PIL.ImageDraw


def get_images(image_dir, base_filename):
    """
    Step through cameras, capturing images. This should work for any
    number of cameras.
    """
    cam_counter = 0
    frame = capture_frame(cam_counter)
    if frame is False:
        print('Could not capture frame. Is a webcam connected?')
        sys.exit(1)

    while frame is not False:

        # Convert to a PIL image
        img = cv_to_pil(frame)

        # Add timestamp
        add_timestamp(img)

        # Save image
        filename = '%s_%d.jpg' % (base_filename, cam_counter)
        filename = os.path.join(image_dir, filename)
        img.save(filename)

        # Next camera...
        cam_counter += 1
        frame = capture_frame(cam_counter)


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

    # Hardcoded directory for storing image(s)
    image_dir = "webcam_images"
    if os.path.exists(image_dir):
        if os.path.isdir(image_dir):
            for f in os.listdir(image_dir):
                f_with_dir = os.path.join(image_dir, f)
                os.remove(f_with_dir)
        else:
            print('Error: required directory %s already exists but is '
                  'not a directory!\nPlease delete it and try again.'
                  % image_dir)
            sys.exit(1)
    else:
        os.mkdir(image_dir)

    # Go!
    get_images(image_dir, sys.argv[1])
