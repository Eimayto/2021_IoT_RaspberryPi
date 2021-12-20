import picamera
import time

path = '/home/pi/src3/06_multimedia'

camera = picamera.PiCamera()

try:
    camera.resolution = (600, 400)
    camera.start_preview()
    time.sleep(3)   # 카메라 촬영 시 준비시간 필요

    # camera.capture('%s/photo.jpg' % path)
    
    # camera.rotation = 180
    camera.start_recording('%s/video.h264' % path)
    input('press enter to stop recording')
    camera.stop_recording()

finally:
    camera.stop_preview()