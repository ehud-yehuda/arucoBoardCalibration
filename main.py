# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PIL import Image
import select
import v4l2capture
import numpy as np
import cv2
import time
import signal


def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # -- Finish Video
    out_uvc.release()
    video.close()
    cv2.destroyAllWindows()


# Open the video device.
video = v4l2capture.Video_device("/dev/video0")

# Suggest an image size to the device. The device may choose and
# return another size if it doesn't support the suggested one.
# size_x, size_y = video.set_format(1280, 1024)
size_x, size_y = video.set_format(1200, 800)
print (size_x)
print(size_y)
# Create a buffer to store image data in. This must be done before
# calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
# raises IOError.
video.create_buffers(1)

# Send the buffer to the device. Some devices require this to be done
# before calling 'start'.
video.queue_all_buffers()

# Start the device. This lights the LED if it's a camera that has one.
video.start()

# Wait for the device to fill the buffer.
select.select((video,), (), ())

fourcc_uvc = cv2.VideoWriter_fourcc('M','J','P','G')
uvc_fn = "uvc_test.avi"
fps = 15.0
out_uvc = cv2.VideoWriter(uvc_fn, fourcc_uvc, fps, (size_x, size_y), True)

signal.signal(signal.SIGINT, signal_handler)

# The rest is easy :-)
while True:
    try:
        time.sleep(1/fps)
        select.select((video,), (), ())
        image_data = video.read_and_queue()
        image = np.array(Image.frombytes("RGB", (size_x, size_y), image_data))
        out_uvc.write(image)
        cv2.imshow('frame', image)
        cv2.waitKey(1)
    except Exception as e:
        print(e)
        break

out_uvc.release()
video.close()

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
