import re
import subprocess
import cv2
import os
def index_value():
    device_re = re.compile("Bus\s+(?P<bus>\d+)\s+Device\s+(?P<device>\d+).+ID\s(?P<id>\w+:\w+)\s(?P<tag>.+)$", re.I)
    df = subprocess.check_output("lsusb", shell=True)
    for i in df.split('\n'):
        if i:
            info = device_re.match(i)
            if info:
                dinfo = info.groupdict()
                print "info",dinfo
                if "Microdia Defender G-Lens 2577 HD720p Camera" in dinfo['tag']:
                    print "Camera found."
                    bus = dinfo['bus']
                    device = dinfo['device']
                    break

    device_index = None
    print"sdfgsf"
    for file in os.listdir("/sys/class/video4linux"):
        print "file",file
        real_file = os.path.realpath("/sys/class/video4linux/" + file)
        print "real", real_file
        print "/" + str(bus[-1]) + "-" + str(device[-1]) + "/"
        if "/" + str(bus[-1]) + "-" + str(device[-1]) + "/" in real_file:
            device_index = real_file[-1]
            print "Hurray, device index is " + str(device_index)
        else:
            print "no device index matching found"
    # if device_index == None:
    #     device_index = 0

    # camera = cv2.VideoCapture(int(device_index))

    # while True:
    #     (grabbed, frame) = camera.read() # Grab the first frame
    #     cv2.imshow("Camera", frame)
    #     key = cv2.waitKey(1) & 0xFF
    return str(device_index)
# print index_value()