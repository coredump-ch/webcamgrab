# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import datetime

import pygame
import pygame.camera
import pygame.image
import PIL.Image
import PIL.ImageDraw


WIDTH = 640
HEIGHT = 480


def get_cam(print_info=True):
    """
    List all cams, return the first cam found.
    """
    cams = pygame.camera.list_cameras()
    print('%d cam(s) found:' % len(cams))
    for cam in cams:
        print('- %s' % cam)
    cam = pygame.camera.Camera(cams[0], (WIDTH, HEIGHT))
    return cam


def capture_surface(cam):
    """
    Capture an image from the camera. Return a pygame surface.
    """
    cam.start()
    return cam.get_image()


def pygame_to_pil(surface):
    """
    Convert a pygame surface to a PIL image.
    """
    stringimg = pygame.image.tostring(surface, 'RGBA')
    return PIL.Image.frombytes('RGBA', (WIDTH, HEIGHT), stringimg)


def add_timestamp(img):
    """
    Add the timestamp to the image. This works in-place.
    """
    draw = PIL.ImageDraw.Draw(img)
    timestamp = datetime.datetime.now().isoformat().replace('T', ' ').split('.')[0]
    draw.text((10, HEIGHT - 20), timestamp, (255, 255, 255))


if __name__ == '__main__':

    # Parse args
    if len(sys.argv) != 2:
        print('Usage: %s <webcamname>' % sys.argv[0])
        sys.exit(1)

    # Initialize camera
    pygame.camera.init()

    # Get the camera
    cam = get_cam()

    # Get a pygame surface
    surface = capture_surface(cam)

    # Convert to a PIL image
    img = pygame_to_pil(surface)

    # Add timestamp
    add_timestamp(img)

    # Save image
    filename = '%s.jpg' % sys.argv[1]
    img.save(filename)
