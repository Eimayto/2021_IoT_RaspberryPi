import picamera
import time
import sys

path = '/home/pi/src3/06_multimedia'

camera = picamera.PiCamera()


camera.start_preview()


try:
    while True:
        _input = input('photo:1, video:2, exit:9 > ')
        if _input == '9':
            camera.stop_preview()
            sys.exit()

        elif _input == '1' or _input == '2':
            camera.resolution = (600, 400)
            time.sleep(3)

            now_str = time.strftime("%Y%m%d_%H%M%S")
            if _input == '1':
                print('사진 촬영')
                camera.capture('%s/photo_%s.jpg' % (path, now_str))
            elif _input == '2':
                camera.start_recording('%s/video_%s.h264' % (path, now_str))
                input('press enter to stop recording')
                camera.stop_recording()
        else:
            print('incorrect command')
    

finally:
    camera.stop_preview()