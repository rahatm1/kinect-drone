#!/usr/bin/env python

from SimpleCV import *
from libardrone import libardrone
import time


def takeoff(drone):
    print "Taking off"
    drone.takeoff()
    drone.hover()
    drone.speed = 0.1
    bat = drone.navdata.get(0, dict()).get('battery', 0)
    print bat


def main():
    display = SimpleCV.Display()
    cam = Kinect()
    ts = []
    bb = None
    drone = libardrone.ARDrone()
    drone.reset()
    #img = cam.getDepth().flipHorizontal()
    time.sleep(2)
    takeoff(drone)
    flying = True
    while display.isNotDone():
        if display.mouseLeft:
            if flying:
                print "Landing"
                flying = False
                drone.land()
                drone.halt()
            else:
                takeoff(drone)
                flying = True

        depth = cam.getDepth().flipHorizontal()
        filtered = depth.stretch(0, 180).binarize().dilate(4)

        # if bb is None:
        blobs = filtered.findBlobs()
        if blobs:
            hand = blobs.filter(abs(7000 - blobs.area()) < 500)
            print hand
            if hand:
                bb = hand[0].boundingBox()
                print bb
        if bb is not None:
            ts = filtered.track("mftrack", ts, filtered, bb)
            if ts:
                ts.drawBB(color=Color.RED)
                #use +x/-y from velocity for drone direction
                ts.showPixelVelocityRT()
                if ts[-1].vel[0] > 5:
                    print ts[-1].vel
                    print "GO RIGHT"
                    drone.move_right()
                elif ts[-1].vel[0] < -5:
                    print ts[-1].vel
                    print "GO LEFT"
                    drone.move_left()
                elif ts[-1].vel[1] > 5:
                    print ts[-1].vel
                    print "GO BACKWARD"
                    drone.move_backward()
                elif ts[-1].vel[1] < -5:
                    print ts[-1].vel
                    print "GO FORWARD"
                    drone.move_forward()
                ts.drawPath()
        filtered.show()

if __name__ == '__main__':
    main()
