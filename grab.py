# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import datetime

import pygame
import pygame.camera
import pygame.image
import PIL.Image
import PIL.ImageDraw


def get_cam(size, print_info=True):
    """
    List all cams, return the first cam found.
    """
    cams = pygame.camera.list_cameras()
    print('%d cam(s) found:' % len(cams))
    for cam in cams:
        print('- %s' % cam)
    cam = pygame.camera.Camera(cams[0], size)
    return cam


def capture_surface(cam):
    """
    Capture an image from the camera. Return a pygame surface.
    """
    cam.start()
    return cam.get_image()


def pygame_to_pil(surface, size):
    """
    Convert a pygame surface to a PIL image.
    """
    stringimg = pygame.image.tostring(surface, 'RGBA')
    return PIL.Image.frombytes('RGBA', size, stringimg)


def add_timestamp(img, size):
    """
    Add the timestamp to the image. This works in-place.
    """
    draw = PIL.ImageDraw.Draw(img)
    timestamp = datetime.datetime.now().isoformat().replace('T', ' ').split('.')[0]
    draw.text((10, size[1] - 20), timestamp, (255, 255, 255))


if __name__ == '__main__':

    # Parse args
    if len(sys.argv) != 4:
        print('Usage: %s <width> <height> <webcamname>' % sys.argv[0])
        sys.exit(1)

    # Initialize camera
    pygame.camera.init()

    # Get size
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    size = (width, height)

    # Get the camera
    cam = get_cam(size)

    # Get a pygame surface
    surface = capture_surface(cam)

    # Convert to a PIL image
    img = pygame_to_pil(surface, size)

    # Add timestamp
    add_timestamp(img, size)

    # Save image
    filename = '%s.jpg' % sys.argv[1]
    img.save(filename)
